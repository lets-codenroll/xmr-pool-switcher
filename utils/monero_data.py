import requests
from utils.helpers import CYAN, GREEN, ORANGE, RED, RESET

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/monero"

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
        print(f"  Circulating Supply: {data['market_data']['circulating_supply']:,.2f} XMR{RESET}")
    except requests.RequestException as e:
        print(f"{RED}Error fetching Monero data: {e}{RESET}")
    except KeyError as e:
        print(f"{RED}Unexpected response structure: {e}{RESET}")
