"""
License validation for Platinum-tool.
"""

import hashlib
from datetime import datetime

# Predefined valid keys with expiration (format: key-expiration_date)
VALID_KEYS = [
    ("PLATINUM2025-2025-10-30", "2025-10-30"),  # Expires Oct 30, 2025
    ("PLATINUM2025-2025-10-30", "2025-10-30"),  # Generated key
    # Add more as needed
]

def validate_key(key: str) -> bool:
    """Validate the provided access key and check expiration."""
    for valid_key, exp_date_str in VALID_KEYS:
        if key == valid_key:
            try:
                exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
                current_date = datetime.now().date()
                if current_date <= exp_date:
                    return True
                else:
                    print("Access key has expired.")
                    return False
            except ValueError:
                continue
    return False

def prompt_for_key():
    """Prompt user for access key and validate."""
    print("Platinum-tool requires an access key for proprietary use.")
    key = input("Enter your access key: ").strip()
    if validate_key(key):
        print("Access granted.\n")
        return True
    else:
        print("Invalid or expired access key. Exiting.")
        return False