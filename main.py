import subprocess
import sys
import threading

def ensure_module(module_name):
    """Check if a module is installed; if not, ask the user to install it."""
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        print(f"Module '{module_name}' is not installed.")
        choice = input(f"Do you want to install '{module_name}' now? (y/n): ").strip().lower()
        if choice == 'y':
            try:
                # Try user-level installation
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', module_name])
                print(f"Module '{module_name}' has been installed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to install '{module_name}'. Attempting to guide you with virtual environment setup.")
                setup_virtual_environment(module_name)
        else:
            print(f"Cannot proceed without '{module_name}'. Exiting...")
            sys.exit(1)


def setup_virtual_environment(module_name):
    """Guide the user to set up a virtual environment and install the required module."""
    print("It seems your environment is externally managed. Let's set up a virtual environment.")
    venv_path = "venv"
    try:
        # Create and activate a virtual environment
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        print("Virtual environment created. Please activate it and rerun this program:")
        print(f"\n  source {venv_path}/bin/activate   # On Linux/macOS")
        print(f"  {venv_path}\\Scripts\\activate    # On Windows")
        print(f"\nOnce activated, install '{module_name}' manually:")
        print(f"\n  pip install {module_name}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create a virtual environment. Error: {e}")
        sys.exit(1)

# Ensure required modules
required_modules = ['psutil', 'schedule', 'requests']
for module in required_modules:
    ensure_module(module)

# Import after ensuring all modules are available
from core.config_manager import load_config
from core.pool_manager import show_pools, set_pool_on_top
from core.scheduler import schedule_pool, view_schedules, run_scheduler
from utils.helpers import MONERO_LOGO, ORANGE, RESET, RED, BOLD
from utils.monero_data import get_monero_data


def show_commands_menu():
    """Display the commands menu."""
    print(f"\n{BOLD}Commands:{RESET}")
    print(f"0. Show this menu again")
    print(f"1. Show all pools")
    print(f"2. Set a pool on top of the list")
    print(f"3. Schedule a pool to move to the top between hours")
    print(f"4. View active schedules")
    print(f"{ORANGE}5. Get Monero market data{RESET}")
    print(f"{BOLD}6. Exit{RESET}")


def main():
    """Main function to handle user input and commands."""
    print(MONERO_LOGO)

    # Load the configuration file
    config = load_config()
    if config is None:
        return

    # Display the commands menu
    show_commands_menu()

    while True:
        command = input("Enter a command: ").strip()

        if command == "0":
            show_commands_menu()
        elif command == "1":
            show_pools(config)
        elif command == "2":
            show_pools(config)
            try:
                pool_index = int(input("\nEnter the pool number to move to the top: "))
                set_pool_on_top(config, pool_index)
            except ValueError:
                print(f"{RED}Invalid input. Please enter a valid number.{RESET}")
        elif command == "3":
            show_pools(config)
            try:
                pool_index = int(input("\nEnter the pool number to schedule: "))
                start_time = input("Enter start time (HH:MM, 24-hour format): ").strip()
                end_time = input("Enter end time (HH:MM, 24-hour format): ").strip()
                schedule_pool(config, pool_index, start_time, end_time)
            except ValueError:
                print(f"{RED}Invalid input. Please try again.{RESET}")
        elif command == "4":
            view_schedules()
        elif command == "5":
            get_monero_data()
        elif command == "6":
            print(f"{ORANGE}Exiting...{RESET}")
            break
        else:
            print(f"{RED}Invalid command. Please try again.{RESET}")
            show_commands_menu()


if __name__ == "__main__":
    # Start the scheduler in a background thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Run the main application
    main()
