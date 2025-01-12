# Monero Pool Manager

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