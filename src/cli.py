#!/usr/bin/env python3
"""
Platinum-tool: A minimalistic time calculator CLI.

This tool provides a simple command-line interface for time calculations.
"""
from calculations import Calculations
from astro import Ephemeris

def show_welcome():
    print("Welcome to Platinum-tool!")
    print("Author: Awuah Baffour")  # Replace with actual author name
    print("A simple time calculator for your needs.\n")
    from license import prompt_for_key
    return prompt_for_key()

def show_menu():
    print("Menu:")
    print("1. Time calculation")
    print("2. Astro calculation")
    print("3. Help")
    print("4. Exit")
    print()

def handle_help():
    print("Help:")
    print("- This is a time calculator tool.")
    print("- Choose options from the menu.")
    print("- More features coming soon.")
    print("- Contact: awuahbj@gmail.com\n")

def handle_time_calculation():
    while True:
        print("Time Calculation Menu:")
        print("1. Calculate time difference between two dates")
        print("2. Calculate exact date from offset")
        print("3. Exit to main menu")
        print()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            Calculations.time_difference()
        elif choice == "2":
            Calculations.locate_exact_date()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.\n")

def handle_astro_calculation():
    while True:
        print("Astro Calculation Menu:")
        print("1. Sidereal calculations")
        print("2. Synodic calculation")
        print("3. Get planet position")
        print("4. Exit to main menu")
        print()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            # Sidereal calculations: calculate longitudes
            start = input("Enter start date (YYYY-MM-DD): ")
            end = input("Enter end date (YYYY-MM-DD): ")
            bodies_input = input("Enter planet names separated by commas (e.g., mars,venus): ")
            bodies = [b.strip() for b in bodies_input.split(',')]
            step = float(input("Enter step in days (default 7): ") or 7)
            eph = Ephemeris()
            df = eph.calculate_longitudes_and_synodic_angles(start, end, bodies, step)
            print(df.head())
            save_dir = input("Enter directory path to save results: ")
            if save_dir:
                import os
                os.makedirs(save_dir, exist_ok=True)
                filepath = os.path.join(save_dir, "sidereal_longitudes.csv")
                df.to_csv(filepath)
                print(f"Results saved to {filepath}")
        elif choice == "2":
            # Synodic calculation
            start = input("Enter start date (YYYY-MM-DD): ")
            end = input("Enter end date (YYYY-MM-DD): ")
            bodies_input = input("Enter planet names separated by commas (e.g., mars,venus): ")
            bodies = [b.strip() for b in bodies_input.split(',')]
            step = float(input("Enter step in days (default 7): ") or 7)
            eph = Ephemeris()
            df = eph.calculate_synodic_period(start, end, bodies=bodies, step=step)
            print(df.head())
            save_dir = input("Enter directory path to save results: ")
            if save_dir:
                import os
                os.makedirs(save_dir, exist_ok=True)
                filepath = os.path.join(save_dir, "synodic_angles.csv")
                df.to_csv(filepath)
                print(f"Results saved to {filepath}")
        elif choice == "3":
            # Get planet positions
            date = input("Enter date (YYYY-MM-DD): ")
            bodies = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
            eph = Ephemeris()
            # For a single date, calculate longitudes and synodic angles
            df = eph.calculate_longitudes_and_synodic_angles(date, date, bodies, step=1)
            print("Planetary Positions on", date)
            print(df.T)  # Transpose for better view
            save_dir = input("Enter directory path to save results: ")
            if save_dir:
                import os
                os.makedirs(save_dir, exist_ok=True)
                filepath = os.path.join(save_dir, f"planetary_positions_{date}.csv")
                df.to_csv(filepath)
                print(f"Results saved to {filepath}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.\n")

def main():
    if not show_welcome():
        return
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            handle_time_calculation()
        elif choice == "2":
            handle_astro_calculation()
        elif choice == "3":
            handle_help()
        elif choice == "4":
            print("Exiting Platinum-tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()