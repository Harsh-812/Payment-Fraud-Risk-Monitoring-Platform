# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
KAFKA_TOPIC = "payment-transactions-raw"

# Generator settings
EVENTS_PER_SECOND = 2
CURRENCY = "USD"

COUNTRIES = ["US", "CA", "GB", "IN"]
PAYMENT_METHODS = ["credit_card", "debit_card", "upi", "paypal"]

# User behavior distribution
NORMAL_USER_PERCENTAGE = 0.85
RISKY_USER_PERCENTAGE = 0.10
FRAUD_USER_PERCENTAGE = 0.05

# Fraud behavior parameters
HIGH_VELOCITY_SLEEP_SECONDS = 0.1
NORMAL_SLEEP_SECONDS = 1.0

BASE_AMOUNT_MIN = 5
BASE_AMOUNT_MAX = 300

AMOUNT_SPIKE_MULTIPLIER = 6
