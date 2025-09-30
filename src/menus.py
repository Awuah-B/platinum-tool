"""Menus.py handles menu selections for scaling modes."""

class Menus:
    @staticmethod
    def choose_scaling_mode():
        """Prompt the user to choose a scaling mode."""
        modes = ["internal_division", "extension", "custom"]
        print("\nChoose scaling mode:")
        for i, mode in enumerate(modes):
            print(f"{i}. {mode}")
        while True:
            try:
                choice = int(input("Enter choice: "))
                if 0 <= choice < len(modes):
                    return modes[choice]
                print(f"Invalid choice. Enter 0-{len(modes)-1}")
            except ValueError:
                print("Invalid input. Enter a number.")