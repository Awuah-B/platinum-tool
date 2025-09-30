#! /usr/bin/env python
"""Calculations.py performs all user-choice calculations."""
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from valid import Valid


class Calculations:
    @staticmethod
    def calculate_time_difference(start, end, scale):
        """
        Calculate the time difference between two dates based on the specified scale.

        Args:
            start (datetime): The start date.
            end (datetime): The end date.
            scale (str): The scale for the calculation (years, months, weeks, days, hours).

        Returns:
            tuple: The time difference in the specified scale.
        """
        if start > end:
            start, end = end, start

        delta = relativedelta(end, start)
        total_seconds = (end - start).total_seconds()

        if scale == "years":
            return delta.years, delta.months, delta.days
        elif scale == "months":
            total_months = delta.years * 12 + delta.months
            return total_months, delta.days
        elif scale == "weeks":
            total_days = total_seconds // (24 * 3600)
            weeks = int(total_days // 7)
            remaining_days = int(total_days % 7)
            return weeks, remaining_days
        elif scale == "days":
            total_days = total_seconds // (24 * 3600)
            remaining_hours = (total_seconds % (24 * 3600)) // 3600
            return int(total_days), int(remaining_hours)
        elif scale == "hours":
            return int(total_seconds // 3600)
        return None

    @staticmethod
    def calculate_delta(scale, duration, operation):
        """
        Calculate a time delta based on the specified scale, duration, and operation.

        Args:
            scale (str): The scale for the calculation (years, months, weeks, days, hours).
            duration (float): The duration to apply.
            operation (str): The operation to perform (+ or -).

        Returns:
            timedelta or relativedelta: The calculated time delta.
        """
        if operation not in ["+", "-"]:
            raise ValueError("Invalid operation. Use '+' or '-'.")

        if operation == "-":
            duration = -duration

        if scale == "years":
            return relativedelta(years=int(duration))
        elif scale == "months":
            return relativedelta(months=int(duration))
        elif scale == "weeks":
            return timedelta(weeks=duration)
        elif scale == "days":
            return timedelta(days=duration)
        elif scale == "hours":
            return timedelta(hours=duration)

    @staticmethod
    def time_difference():
        """Calculate the time difference between two dates."""
        print("\nStarting time calculator...")
        start_date = Valid.get_valid_date("Enter date of origin")
        end_date = Valid.get_valid_date("Enter end date")
        time_scale = Valid.get_valid_scale()

        result = Calculations.calculate_time_difference(start_date, end_date, time_scale)

        if result is None:
            print("Error calculating time difference")
            return None, None

        if time_scale == "years":
            print(f"\nTime difference: {result[0]} years, {result[1]} months, {result[2]} days")
        elif time_scale == "months":
            print(f"\nTime difference: {result[0]} months, {result[1]} days")
        elif time_scale == "weeks":
            print(f"\nTime difference: {result[0]} weeks, {result[1]} days")
        elif time_scale == "days":
            print(f"\nTime difference: {result[0]} days, {result[1]} hours")
        elif time_scale == "hours":
            print(f"\nTime difference: {result} hours")

        return result[0], time_scale

    @staticmethod
    def locate_exact_date():
        """Calculate an exact date based on an offset from a given date."""
        print("\nStarting time machine...")
        scale = Valid.get_valid_scale()
        operation = Valid.get_valid_operation()
        duration = Valid.get_valid_duration(scale)

        delta = Calculations.calculate_delta(scale, duration, operation)
        start_date = Valid.get_valid_date("Enter date of origin")
        new_date = start_date + delta

        print(f"\nExact date: {new_date.strftime('%Y-%m-%d %H:%M')}")
        return new_date, scale, duration
