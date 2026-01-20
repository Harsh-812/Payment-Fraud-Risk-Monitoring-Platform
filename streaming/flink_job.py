from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.common.time import Duration

from pyflink.datastream.window import SlidingEventTimeWindows
from pyflink.common.time import Time

import json
from datetime import datetime, timezone, timedelta


# Helper: parse ISO event_time to epoch ms
def extract_event_timestamp(event: dict) -> int:
    event_time_str = event.get("event_time")
    event_time = datetime.fromisoformat(event_time_str)
    return int(event_time.timestamp() * 1000)


# Simple callable class for timestamp assignment
class TimestampAssignerFunction:
    """Simple callable class that PyFlink can use for timestamp assignment."""
    
    def extract_timestamp(self, element, record_timestamp):
        """Extract timestamp from event element."""
        return extract_event_timestamp(element)
    
    def __call__(self, element, record_timestamp):
        """Make it callable as a function."""
        return self.extract_timestamp(element, record_timestamp)


# Main Flink Job
def main():
    env = StreamExecutionEnvironment.get_execution_environment()

    # Enable event-time processing
    env.set_parallelism(1)

    # Kafka Source
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("kafka:9092") \
        .set_topics("payment-transactions-raw") \
        .set_group_id("flink-fraud-consumer") \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()
    
    # JSON parsing first
    raw_stream = env.from_source(
        source=kafka_source,
        watermark_strategy=WatermarkStrategy.no_watermarks(),
        source_name="KafkaSource"
    )

    # Parse JSON
    parsed_stream = raw_stream.map(
        lambda value: json.loads(value)
    )

    # Create watermark strategy with timestamp assigner
    # Note: Using monotonic_watermarks() instead of for_bounded_out_of_orderness()
    # to avoid known PyFlink bug with int + Time arithmetic in window operations
    watermark_strategy = WatermarkStrategy \
        .for_monotonous_timestamps() \
        .with_timestamp_assigner(TimestampAssignerFunction())

    # Apply watermark strategy to assign event times
    event_time_stream = parsed_stream.assign_timestamps_and_watermarks(
        watermark_strategy
    )

   # Key by user_id
    keyed_stream = event_time_stream.key_by(
        lambda event: event["user_id"]
    )

    # Sliding event-time window
    # Note: Removed allowed_lateness() due to known PyFlink bug:
    # TypeError: unsupported operand type(s) for +: 'int' and 'Time'
    # This is a limitation of PyFlink's Beam-based runtime
    windowed_stream = (
        keyed_stream
        .window(
            SlidingEventTimeWindows.of(
                Time.minutes(5),   # window size
                Time.minutes(1)    # slide
            )
        )
        .reduce(
            lambda a, b: {
                "user_id": a["user_id"],
                "transaction_count": int(a.get("transaction_count", 1)) + 1,
                "window_last_event_time": max(
                    a.get("window_last_event_time", a.get("event_time", "")),
                    b.get("event_time", "")
                )
            }
        )
    )

    # Main output: windowed aggregates
    windowed_stream.print("WINDOW")


    env.execute("Payment Fraud – Event Time Ingestion")


if __name__ == "__main__":
    main()
