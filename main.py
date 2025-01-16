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


def ensure_module(module_name):
    """Check if a module is installed; if not, ask the user to install it."""
    try:
        __import__(module_name)
    except ModuleNotFoundError:
        print(f"Module '{module_name}' is not installed.")
        choice = input(f"Do you want to set up a virtual environment and install '{module_name}'? (y/n): ").strip().lower()
        if choice == 'y':
            setup_virtual_environment_and_install(module_name)
        else:
            print(f"Cannot proceed without '{module_name}'. Exiting...")
            sys.exit(1)


def setup_virtual_environment_and_install(module_name):
    """Create a virtual environment and install the module."""
    venv_path = "venv"
    try:
        print("Setting up a virtual environment...")
        subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
        pip_executable = os.path.join(venv_path, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'pip')
        print(f"Installing '{module_name}' in the virtual environment...")
        subprocess.check_call([pip_executable, 'install', module_name])
        print(f"Module '{module_name}' installed successfully in the virtual environment.")
        print(f"To activate the environment, run:")
        if os.name == 'nt':
            print(f"  {venv_path}\\Scripts\\activate")
        else:
            print(f"  source {venv_path}/bin/activate")
        print(f"Re-run the program within the activated environment.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Failed to set up the virtual environment or install '{module_name}'. Error: {e}")
        sys.exit(1)


def is_xmrig_active():
    """Check if xmrig is currently active."""
    for proc in psutil.process_iter(['name']):
        if 'xmrig' in proc.info['name'].lower():
            return True
    return False


def start_xmrig():
    """Attempt to start xmrig."""
    try:
        print(f"{ORANGE}Starting xmrig...{RESET}")
        subprocess.Popen(['./xmrig'], cwd=os.path.dirname(os.path.abspath(__file__)))
        print(f"{GREEN}xmrig started successfully.{RESET}")
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
    required_modules = ['psutil', 'schedule', 'requests']
    for module in required_modules:
        ensure_module(module)

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    main()
