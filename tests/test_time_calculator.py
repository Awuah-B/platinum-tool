import pytest
from datetime import datetime
from src.calculations import Calculations
from src.license import validate_key

def test_calculate_time_difference_years():
    start = datetime(2020, 1, 1)
    end = datetime(2022, 3, 15)
    result = Calculations.calculate_time_difference(start, end, "years")
    assert result == (2, 2, 14)

def test_calculate_time_difference_days():
    start = datetime(2020, 1, 1)
    end = datetime(2020, 1, 10)
    result = Calculations.calculate_time_difference(start, end, "days")
    assert result == (9, 0)

def test_validate_key_valid():
    # Assuming a valid key for current date
    key = "PLATINUM2025-2025-10-30"  # Example, adjust as needed
    assert validate_key(key) == True

def test_validate_key_expired():
    key = "PLATINUM2025-2025-09-29"  # Expired
    assert validate_key(key) == False