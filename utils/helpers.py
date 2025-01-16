from urllib.parse import urlparse
import psutil
import os

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
ORANGE = "\033[38;2;255;102;0m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"

MONERO_LOGO = fMONERO_LOGO = f"""
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

def check_xmrig_active():
    """Check if xmrig miner is running."""
    for proc in psutil.process_iter(['name']):
        if 'xmrig' in (proc.info['name'] or '').lower():
            print(f"{GREEN}xmrig miner is currently running.{RESET}")
            return True
    print(f"{RED}xmrig miner is not running.{RESET}")
    return False

def start_xmrig():
    """Start the xmrig miner."""
    try:
        os.system("nohup ./xmrig > xmrig.log 2>&1 &")
        print(f"{GREEN}xmrig miner started successfully.{RESET}")
    except Exception as e:
        print(f"{RED}Failed to start xmrig miner: {e}{RESET}")
        
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
    except Exception:
        return f"{RED}Error parsing URL{RESET}"
