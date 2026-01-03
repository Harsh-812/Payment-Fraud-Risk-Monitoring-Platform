# Payment-Fraud-Risk-Monitoring-Platform

A real-time streaming data platform that ingests payment transactions, evaluates fraud and risk signals using stateful stream processing, and provides live operational dashboards.

## Business Problem

Modern digital payment systems process thousands of transactions per second across multiple regions, merchants, and payment methods.  
Traditional batch-based fraud and risk detection systems introduce delays that prevent timely intervention, allowing suspicious transactions to complete before detection.

Operational teams also lack real-time visibility into transaction patterns, risk signals, and system health, relying instead on delayed reports and manual investigations.

## Business Objective

The objective of this project is to build a real-time streaming analytics platform that:

- Continuously ingests payment transactions
- Detects suspicious activity within seconds
- Computes live risk and velocity metrics
- Provides real-time dashboards for monitoring and investigation
- Scales horizontally with increasing transaction volume

## Data Strategy

Production payment data is highly sensitive and not publicly accessible.  
To simulate realistic real-time workloads, this project uses a synthetic event generator that continuously produces payment transactions with controlled variability.

The synthetic data simulates:
- Normal transaction traffic
- High-velocity user behavior
- Sudden spikes in transaction amounts
- Geographic anomalies
- Out-of-order and delayed events

This approach mirrors industry-standard testing practices used to validate streaming systems under realistic conditions.


## High-Level Architecture

1. A synthetic event generator continuously produces payment transactions
2. Events are ingested into a streaming backbone
3. Stateful stream processing evaluates transaction patterns and risk signals
4. Enriched results are written to analytical storage
5. Dashboards update in near real time to support monitoring and investigation


## Technology Stack

- Streaming Backbone: Apache Kafka
- Stream Processing: Apache Flink
- Storage: Amazon S3, Amazon DynamoDB
- Observability: Grafana, Prometheus
- Infrastructure: Docker
- CI/CD: GitHub Actions

