from datetime import datetime, timedelta

def generate_key(prefix="PLATINUM2025", expiration_days=30):
    """Generate a new access key with customizable prefix and expiration."""
    expiration_date = (datetime.now() + timedelta(days=expiration_days)).strftime("%Y-%m-%d")
    key = f"{prefix}-{expiration_date}"
    print(f"Generated Key: {key}")
    print(f"Add to VALID_KEYS: (\"{key}\", \"{expiration_date}\")")
    return key, expiration_date

if __name__ == "__main__":
    # Example: python generate_key.py
    generate_key()
    # For custom: generate_key("CUSTOM", 60)