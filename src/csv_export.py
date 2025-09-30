"""Csv.py handles display of scaled data in tabular format."""
import csv
import os
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Csv:
    @staticmethod
    def calculate_delta(scale, duration, operation):
        """
        Calculate a time delta based on the specified scale, duration, and operation.
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
    def prepare_and_export_data(scaled_values, scaling_ratios, scale, time_diff, scaling_mode, start_date, end_date):
        """Display the scaled data in a tabular format on the command line."""
        # Assume operation is '+' for adding to start_date
        operation = "+"
        scaled_dates = [start_date + Csv.calculate_delta(scale, value, operation) for value in scaled_values]

        print(f"\nStart Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"End Date: {end_date.strftime('%Y-%m-%d')}")
        print(f"Original Time Difference: {time_diff} {scale}")
        print(f"Scaling Mode: {scaling_mode}")
        print("\nCycle Date | Duration | Scaling Factor")
        print("-" * 50)
        for scaled_date, duration, ratio in zip(scaled_dates, scaled_values, scaling_ratios):
            cycle_date = f"{start_date.strftime('%Y-%m-%d')} - {scaled_date.strftime('%Y-%m-%d')}"
            print(f"{cycle_date} | {int(round(duration))} | {ratio}")
        print("\nData displayed successfully.")