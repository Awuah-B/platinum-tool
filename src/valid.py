#! /usr/bin/env python
"""Valid ensures user inputs are in the correct programmable form."""
from datetime import datetime
from scales import scaling_configurations


class Valid:
    @staticmethod
    def get_valid_date(prompt):
        """Prompt the user for a valid date and return it."""
        prompt += "\n(YYYY-MM-DD, MM/DD/YYYY, or DD-MM-YYYY): "
        while True:
            date_str = input(prompt)
            if date_str.lower() == "cancel":
                return None
            try:
                date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y"]
                for fmt in date_formats:
                    try:
                        date = datetime.strptime(date_str, fmt)
                        return datetime.combine(date.date(), datetime.min.time())
                    except ValueError:
                        continue
                raise ValueError
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD, MM/DD/YYYY, or DD-MM-YYYY\nType 'cancel' to go back")

    @staticmethod
    def get_valid_scale():
        """Prompt the user for a valid time scale and return it."""
        valid_scales = ["years", "months", "weeks", "days", "hours"]
        while True:
            scale = input(f"Choose time-scale ({', '.join(valid_scales)}): ").lower()
            if scale in valid_scales:
                return scale
            print(f"Invalid scale. Please choose from {', '.join(valid_scales)}")

    @staticmethod
    def get_valid_duration(scale):
        """Prompt the user for a valid duration and return it."""
        while True:
            try:
                duration = float(input(f"Enter duration in {scale}: "))
                if duration >= 0:
                    return duration
                print("Please enter a positive number")
            except ValueError:
                print("Invalid input. Please enter a number")

    @staticmethod
    def get_valid_operation():
        """Prompt the user for a valid operation (+ or -) and return it."""
        valid_ops = ["+", "-"]
        while True:
            op = input("Choose operation (+ or -): ")
            if op in valid_ops:
                return op
            print("Invalid operation. Please choose + or -")

    @staticmethod
    def get_scaling_configuration(mode):
        """Retrieve the scaling configuration based on the selected mode."""
        if mode not in scaling_configurations:
            raise ValueError(f"Invalid scaling mode: {mode}")

        print(f"\nAvailable {mode.title()} Scaling Options:")
        config_dict = scaling_configurations[mode]

        for idx, (key, value) in enumerate(config_dict.items()):
            print(f"{idx}. {key}: {value}")

        while True:
            try:
                choice = int(input(f"\nChoose scaling option (0-{len(config_dict) - 1}): "))
                if 0 <= choice < len(config_dict):
                    return list(config_dict.values())[choice]
                print(f"Invalid choice. Please enter 0-{len(config_dict) - 1}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
