import subprocess
import sys
import threading
import os
from core.config_manager import load_config, save_config
from core.pool_manager import show_pools, set_pool_on_top
from core.scheduler import schedule_pool, view_schedules, run_scheduler
from utils.helpers import MONERO_LOGO, ORANGE, RESET, RED, GREEN, BOLD
from utils.monero_data import get_monero_data
import psutil
import json


def create_and_setup_virtualenv(required_modules):
    """Create a virtual environment and install required modules."""
    venv_path = "venv"

    try:
        # Check if the virtual environment already exists
        if not os.path.exists(venv_path):
            print("Setting up a virtual environment...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            print("Virtual environment created successfully.")

        # Activate the virtual environment
        pip_executable = os.path.join(venv_path, "bin", "pip") if os.name != "nt" else os.path.join(venv_path, "Scripts", "pip")

        # Install required modules
        print("Installing required modules...")
        subprocess.check_call([pip_executable, "install", "--upgrade", "pip"])  # Upgrade pip in venv
        for module in required_modules:
            subprocess.check_call([pip_executable, "install", module])
        print("All required modules installed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to set up the virtual environment or install modules. Error: {e}")
        sys.exit(1)


def ensure_environment():
    """Ensure the virtual environment and required modules are available."""
    venv_path = "venv"

    # If virtual environment exists, ensure we're using it
    if os.path.exists(venv_path):
        venv_python = os.path.join(venv_path, "bin", "python") if os.name != "nt" else os.path.join(venv_path, "Scripts", "python")

        # Check if the current Python executable is the one in the venv
        if sys.executable != os.path.abspath(venv_python):
            print("Activating virtual environment...")
            os.execl(venv_python, venv_python, *sys.argv)
    else:
        # Create and set up the virtual environment
        required_modules = ["psutil", "schedule", "requests"]
        create_and_setup_virtualenv(required_modules)


def is_xmrig_active():
    """Check if xmrig is currently active."""
    for proc in psutil.process_iter(['name']):
        if 'xmrig' in proc.info['name'].lower():
            return True
    return False

def update_background_in_config():
    """Ensure the 'background' parameter in config.json is set to true."""
    try:
        # Resolve the parent directory and locate config.json
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(parent_dir, 'config.json')

        # Load the existing config.json
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"config.json not found at {config_path}")

        with open(config_path, 'r') as file:
            config = json.load(file)

        # Update the 'background' parameter
        if config.get("background") != True:
            config["background"] = True
            with open(config_path, 'w') as file:
                json.dump(config, file, indent=4)
            print(f"{ORANGE}'background' parameter set to true in config.json.{RESET}")
        else:
            print(f"{GREEN}'background' parameter is already set to true in config.json.{RESET}")
        return config_path
    except Exception as e:
        print(f"{RED}Failed to update 'background' parameter in config.json. Error: {e}{RESET}")
        raise

def start_xmrig():
    """Attempt to start xmrig with the 'background' parameter enabled."""
    try:
        # Update the config.json background parameter
        config_path = update_background_in_config()

        # Resolve the parent directory
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        xmrig_path = os.path.join(parent_dir, 'xmrig')

        # Check if the xmrig binary exists
        if not os.path.isfile(xmrig_path):
            raise FileNotFoundError(f"'xmrig' not found at {xmrig_path}")

        print(f"{ORANGE}Starting xmrig from {xmrig_path}...{RESET}")

        # Start xmrig
        subprocess.Popen([xmrig_path], cwd=parent_dir)
        print(f"{GREEN}xmrig started successfully. It is running in the background as configured in config.json.{RESET}")
    except Exception as e:
        print(f"{RED}Failed to start xmrig. Error: {e}{RESET}")


def set_cores(config):
    """Set the number of cores for mining."""
    max_cores = psutil.cpu_count(logical=True)
    print(f"\n{ORANGE}Your system has {max_cores} logical CPU cores.{RESET}")
    try:
        cores = int(input(f"Enter the number of cores to use (1-{max_cores}): "))
        if cores < 1 or cores > max_cores:
            raise ValueError("Invalid core count.")
        threads = [{"low_power_mode": False, "affine_to_cpu": i} for i in range(cores)]
        config["cpu"] = {
            "enabled": True,
            "huge-pages": True,
            "threads": threads
        }
        save_config(config)
        print(f"{GREEN}Configuration updated to use {cores} cores.{RESET}")
    except ValueError as e:
        print(f"{RED}Error: {e}. Please enter a valid number.{RESET}")

def show_commands_menu():
    """Display the commands menu."""
    print(f"\n{BOLD}Commands:{RESET}")
    print(f"0. Show this menu again")
    print(f"1. Show all pools")
    print(f"2. Set a pool on top of the list")
    print(f"3. Schedule a pool to move to the top between hours")
    print(f"4. View active schedules")
    print(f"{ORANGE}5. Get Monero market data{RESET}")
    print(f"6. Set number of cores for mining")
    print(f"{BOLD}7. Exit{RESET}")

def main():
    """Main function to handle user input and commands."""
    print(MONERO_LOGO)

    # Check if xmrig is active
    if is_xmrig_active():
        print(f"{GREEN}xmrig is active and running.{RESET}")
    else:
        print(f"{RED}Warning: xmrig is not currently running.{RESET}")
        choice = input("Do you want to start xmrig now? (y/n): ").strip().lower()
        if choice == 'y':
            start_xmrig()

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
            set_cores(config)
        elif command == "7":
            print(f"{ORANGE}Exiting...{RESET}")
            break
        else:
            print(f"{RED}Invalid command. Please try again.{RESET}")
            show_commands_menu()


if __name__ == "__main__":
    ensure_environment()

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    main()
