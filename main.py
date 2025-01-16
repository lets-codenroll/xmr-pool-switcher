import threading
from core.config_manager import load_config
from core.pool_manager import show_pools, set_pool_on_top, configure_cores
from core.scheduler import schedule_pool, view_schedules, run_scheduler
from core.monero_data import get_monero_data
from utils.helpers import MONERO_LOGO, ORANGE, RESET, RED, BOLD, check_xmrig_active, start_xmrig

def show_commands_menu():
    """Display the commands menu."""
    print(f"\n{BOLD}Commands:{RESET}")
    print(f"0. Show this menu again")
    print(f"1. Show all pools")
    print(f"2. Set a pool on top of the list")
    print(f"3. Schedule a pool to move to the top between hours")
    print(f"4. View active schedules")
    print(f"{ORANGE}5. Get Monero market data{RESET}")
    print(f"6. Configure CPU cores for mining")
    print(f"{BOLD}7. Exit{RESET}")

def main():
    """Main function to handle user input and commands."""
    print(MONERO_LOGO)
    print(f"{ORANGE}Welcome to XMRig Pool Switcher!{RESET}")
    # Check if xmrig is active
    if not check_xmrig_active():
        choice = input("xmrig miner is not running. Would you like to start it? (y/n): ").strip().lower()
        if choice == 'y':
            start_xmrig()
        else:
            print(f"{RED}xmrig miner was not started. Some features may not work properly.{RESET}")


    config = load_config()
    if config is None:
        return

    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    show_commands_menu()

    while True:
        command = input("\nEnter a command: ").strip()

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
            configure_cores(config)
        elif command == "7":
            print(f"{ORANGE}Exiting...{RESET}")
            break
        else:
            print(f"{RED}Invalid command! Please try again.{RESET}")
            show_commands_menu()


if __name__ == "__main__":
    main()
