from datetime import datetime
import schedule
import time
from core.pool_manager import set_pool_on_top
from utils.helpers import CYAN, RESET, MAGENTA

schedules = []  # To store active schedules

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
        print(f"{CYAN}No active schedules.{RESET}")
    else:
        print(f"{CYAN}Active Schedules:{RESET}")
        for idx, sched in enumerate(schedules, start=1):
            print(f"  {idx}. Pool {sched['pool_index']} from {sched['start_time']} to {sched['end_time']}.")

def run_scheduler():
    """Run the scheduler continuously."""
    print(f"{CYAN}Scheduler is running in the background...{RESET}")
    while True:
        schedule.run_pending()
        time.sleep(1)
