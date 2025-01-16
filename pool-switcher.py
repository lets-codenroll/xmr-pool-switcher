import json
import os
from datetime import datetime
from urllib.parse import urlparse
import schedule
import time
import requests


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(os.path.dirname(BASE_DIR), "config.json") 
print(f"Looking for config.json at: {CONFIG_FILE}")

schedules = []
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/monero"

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
ORANGE = "\033[38;2;255;102;0m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"

MONERO_LOGO = f"""
{ORANGE}                  -===========-
             -=====================-        
          -===========================-
        -===============================-
      -===================================-
    -=======================================-
   -=====+=============================+=====-
  -======   -=======================-   ======-
 -=======     -===================-     =======-
 ========       -===============-       ========
-========         -===========-         ========-
=========           -=======-           =========
========={RESET}     .       {ORANGE}-===-{RESET}       .     {ORANGE}=========
-========{RESET}     ::.       {ORANGE}+{RESET}       .::     {ORANGE}========-
 ========{RESET}     ::::.           .::::     {ORANGE}========{RESET}
              ::::::.       .::::::
              ::::::::.   .::::::::
              ::::::::::.::::::::::
   ...........:::::::::::::::::::::...........
    *:::::::::::::::::::::::::::::::::::::::*
      *:::::::::::::::::::::::::::::::::::*
        *:::::::::::::::::::::::::::::::*
          *:::::::::::::::::::::::::::*
              *:::::::::::::::::::*
                    *********
"""

def load_config():
    """Load the configuration from the config.json file."""
    if not os.path.exists(CONFIG_FILE):
        print(f"{RED}Error: {CONFIG_FILE} not found.{RESET}")
        return None
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    """Save the updated configuration to the config.json file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    print(f"{GREEN}Configuration saved to {CONFIG_FILE}.{RESET}")


def show_pools(config):
    """List all pools in the config.json."""
    pools = config.get("pools", [])
    if not pools:
        print(f"{RED}No pools found in the configuration.{RESET}")
        return
    print(f"{CYAN}Current Pools:{RESET}")
    for idx, pool in enumerate(pools, start=1):
        domain = get_domain(pool.get("url", "N/A"))
        print(f"  {BOLD}{idx}. Domain:{RESET} {domain}")


def set_pool_on_top(config, pool_index):
    """Move a specific pool to the top of the list."""
    pools = config.get("pools", [])
    if not pools:
        print(f"{RED}No pools found in the configuration.{RESET}")
        return False
    if 1 <= pool_index <= len(pools):
        pool = pools.pop(pool_index - 1)
        pools.insert(0, pool)
        config["pools"] = pools
        print(f"{GREEN}Moved pool with domain {get_domain(pool['url'])} to the top of the list.{RESET}")
        save_config(config)
        return True
    else:
        print(f"{RED}Invalid number. Enter a number between 1 and {len(pools)}.{RESET}")
        return False


def schedule_pool(config, pool_index, start_time, end_time):
    """Schedule a pool to move to the top between specific hours."""
    def job():
        now = datetime.now().time()
        start = datetime.strptime(start_time, "%H:%M").time()
        end = datetime.strptime(end_time, "%H:%M").time()

        # Handle overnight ranges (e.g., 21:00 to 03:00)
        if start > end:
            if now >= start or now < end:
                set_pool_on_top(config, pool_index)
        else:
            if start <= now < end:
                set_pool_on_top(config, pool_index)

    schedule.every(1).minute.do(job)
    schedules.append({"pool_index": pool_index, "start_time": start_time, "end_time": end_time})
    print(f"{MAGENTA}Scheduled pool {pool_index} to be moved to the top between {start_time} and {end_time}.{RESET}")


def view_schedules():
    """View all active schedules."""
    if not schedules:
        print(f"{RED}No active schedules.{RESET}")
    else:
        print(f"{CYAN}Active Schedules:{RESET}")
        for idx, sched in enumerate(schedules, start=1):
            print(f"  {BOLD}{idx}. Pool {sched['pool_index']} from {sched['start_time']} to {sched['end_time']}.{RESET}")


def get_monero_data():
    """Fetch Monero data from the CoinGecko API."""
    try:
        response = requests.get(COINGECKO_URL)
        response.raise_for_status()
        data = response.json()
        
        current_price = data['market_data']['current_price']['usd']
        market_cap = data['market_data']['market_cap']['usd']
        volume = data['market_data']['total_volume']['usd']

        print(f"\n{CYAN}Monero Market Data:{RESET}")
        print(f"{GREEN}  Price (USD): ${current_price:,.2f}{RESET}")
        print(f"{ORANGE}  Market Cap (USD): ${market_cap:,.2f}{RESET}")
        print(f"  24h Volume (USD): ${volume:,.2f}")
        print(f"{BOLD}  Circulating Supply: {data['market_data']['circulating_supply']:,.2f} XMR{RESET}")
    except requests.RequestException as e:
        print(f"{RED}Error fetching Monero data: {e}{RESET}")
    except KeyError as e:
        print(f"{RED}Unexpected response structure: {e}{RESET}")


def get_domain(url):
    """Extract the domain from a URL (excluding subdomains)."""
    try:
        parsed_url = urlparse(url if url.startswith("http") else f"http://{url}")
        if parsed_url.hostname:
            domain_parts = parsed_url.hostname.split('.')
            if len(domain_parts) > 2:
                return '.'.join(domain_parts[-2:])  # Keep only the main domain and TLD
            return parsed_url.hostname
        else:
            return f"{RED}Invalid URL{RESET}"
    except Exception as e:
        return f"{RED}Error parsing URL{RESET}"


def run_scheduler():
    """Run the scheduler continuously."""
    print(f"{CYAN}Scheduler is running in the background...{RESET}")
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    """Main function to handle user input and commands."""
    print(MONERO_LOGO)
    config = load_config()
    if config is None:
        return

    while True:
        print(f"\n{BOLD}Commands:{RESET}")
        print(f"1. Show all pools")
        print(f"2. Set a pool on top of the list")
        print(f"3. Schedule a pool to move to the top between hours")
        print(f"4. View active schedules")
        print(f"{ORANGE}5. Get Monero market data{RESET}")
        print(f"{BOLD}6. Exit{RESET}")
        command = input("Enter a command: ").strip()

        if command == "1":
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


if __name__ == "__main__":
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    main()