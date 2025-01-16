import os
from core.config_manager import save_config
from utils.helpers import BOLD, RESET, CYAN, RED, GREEN
from utils.helpers import get_domain

def configure_cores(config):
    """Allow the user to configure the number of cores for mining."""
    total_cores = os.cpu_count()
    if total_cores is None:
        print(f"{RED}Error: Unable to detect the number of CPU cores.{RESET}")
        return

    print(f"Your device has {total_cores} CPU cores available.")
    while True:
        try:
            num_cores = int(input(f"Enter the number of cores to use (1-{total_cores}): "))
            if 1 <= num_cores <= total_cores:
                # Update the config.json file
                config["cpu"] = {"enabled": True, "huge-pages": True, "pools": config.get("pools", [])}
                config["cpu"]["threads"] = [{"low_power_mode": False, "affine_to_cpu": i} for i in range(num_cores)]

                save_config(config)
                print(f"{GREEN}Configuration updated: Using {num_cores} cores for mining.{RESET}")
                break
            else:
                print(f"{RED}Invalid input. Please enter a number between 1 and {total_cores}.{RESET}")
        except ValueError:
            print(f"{RED}Invalid input. Please enter a valid number.{RESET}")

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
