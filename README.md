# XMR (Monero) Pool Manager

A command-line tool to manage Monero mining pools with features to:
- View all configured mining pools.
- Move a specific pool to the top of the list.
- Schedule a pool to be prioritized at specific times.
- Retrieve real-time Monero market data, including price, market cap, and 24-hour volume.

This project is designed to simplify Monero pool management for miners using XMRig and includes an interactive interface with a visually appealing Monero ASCII art logo.

---

## Features

- **View Pools**: Display all configured mining pools in the `config.json` file.
- **Prioritize Pools**: Move a specific pool to the top of the priority list.
- **Schedule Pools**: Automatically prioritize a pool during specific hours.
- **Market Data**: Fetch live Monero market data from the CoinGecko API.
- **Background Scheduler**: Run tasks in the background for scheduled pool prioritization.

---

## Requirements

- **Python**: Version 3.7 or higher
- **Dependencies**:
  - `schedule`
  - `requests`

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/monero-pool-manager.git
   cd monero-pool-manager
   ```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the config.json file is in the same directory as the script, containing your mining pools. Example:
```bash
{
    "pools": [
        {
            "url": "pool.supportxmr.com:443",
            "user": "YourMoneroAddress",
            "pass": "worker_name",
            "rig-id": "rig_id",
            "tls": true
        }
    ]
}
```

4. Run the script:
```bash
python3 pool-switcher.py
```

## Commands
1. Show All Pools: Displays all configured pools from config.json.
2. Set a Pool on Top: Move a specific pool to the top of the priority list.
3. Schedule a Pool: Schedule a pool to be automatically prioritized between specific hours.
4. View Active Schedules: View all active pool prioritization schedules.
5. Fetch Monero Market Data: Retrieve the current price, market cap, 24-hour trading volume, and circulating supply.
6. Exit: Exit the application.

## License

This project is licensed under the GNU General Public License (GPL).  
You are free to use, modify, and distribute this software under the terms of the GPL license.  

For more details, see the [LICENSE](LICENSE) file or visit the [GNU website](https://www.gnu.org/licenses/gpl-3.0.en.html).