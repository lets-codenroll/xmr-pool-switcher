from datetime import datetime
from urllib.parse import urlparse
import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/monero"
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
ORANGE = "\033[38;2;255;102;0m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"

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

