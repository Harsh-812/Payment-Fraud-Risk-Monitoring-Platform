import random
import time
import uuid
from faker import Faker

from config import (
    COUNTRIES,
    PAYMENT_METHODS,
    CURRENCY,
    NORMAL_USER_PERCENTAGE,
    RISKY_USER_PERCENTAGE,
    FRAUD_USER_PERCENTAGE,
    BASE_AMOUNT_MIN,
    BASE_AMOUNT_MAX,
    AMOUNT_SPIKE_MULTIPLIER,
    HIGH_VELOCITY_SLEEP_SECONDS,
    NORMAL_SLEEP_SECONDS,
)
from event_schema import build_payment_event

fake = Faker()

# -----------------------------
# In-memory user state
# -----------------------------
user_profiles = {}


def initialize_user(user_id: str):
    """Initialize baseline behavior for a user."""
    persona = random.choices(
        population=["normal", "risky", "fraud"],
        weights=[
            NORMAL_USER_PERCENTAGE,
            RISKY_USER_PERCENTAGE,
            FRAUD_USER_PERCENTAGE,
        ],
    )[0]

    user_profiles[user_id] = {
        "persona": persona,
        "home_country": random.choice(COUNTRIES),
        "base_amount": random.uniform(20, 80),
        "last_tx_time": 0,
    }


def generate_payment_event():
    # Pick a user
    user_id = f"user_{random.randint(1, 100)}"

    if user_id not in user_profiles:
        initialize_user(user_id)

    profile = user_profiles[user_id]
    persona = profile["persona"]

    transaction_id = f"txn_{uuid.uuid4().hex[:12]}"
    merchant_id = f"merchant_{random.randint(1, 20)}"

    # -----------------------------
    # Amount logic
    # -----------------------------
    if persona == "fraud" and random.random() < 0.5:
        amount = profile["base_amount"] * AMOUNT_SPIKE_MULTIPLIER
    else:
        amount = random.uniform(BASE_AMOUNT_MIN, BASE_AMOUNT_MAX)

    # -----------------------------
    # Status logic
    # -----------------------------
    if persona == "risky":
        status = random.choice(["SUCCESS", "FAILED", "FAILED"])
    else:
        status = "SUCCESS"

    country = profile["home_country"]

    metadata = {
        "device_type": random.choice(["mobile", "desktop"]),
        "ip_address": fake.ipv4_public(),
        "is_international": country != "US",
        "user_persona": persona,
    }

    event = build_payment_event(
        transaction_id=transaction_id,
        user_id=user_id,
        merchant_id=merchant_id,
        amount=amount,
        currency=CURRENCY,
        payment_method=random.choice(PAYMENT_METHODS),
        country=country,
        status=status,
        metadata=metadata,
    )

    # -----------------------------
    # Velocity behavior
    # -----------------------------
    if persona == "fraud":
        time.sleep(HIGH_VELOCITY_SLEEP_SECONDS)
    else:
        time.sleep(NORMAL_SLEEP_SECONDS)

    return event
