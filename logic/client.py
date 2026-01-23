# vpn_core.py
import time
import sys
from typing import Optional, Callable

from net_config import resolve_host
from wintun import create_adapter, start_session, close_adapter, end_session


class VPNCore:
    def __init__(self):
        self.adapter = None
        self.session = None
        self.is_running = False
        self.log_callback: Optional[Callable[[str], None]] = None
        self.client_ip: Optional[str] = None

    def set_log_callback(self, callback: Callable[[str], None]):
        self.log_callback = callback

    def log(self, message: str):
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def connect(self) -> bool:
        if self.is_running:
            self.log("[!] Already connected.")
            return False

        try:
            SERVER_IP = resolve_host("server.vpn.lab")
            # PHYSICAL_GW = resolve_host("gw.vpn.lab")     # currently unused
            CLIENT_IP = resolve_host("client.tun.vpn.lab")
            SERVER_TUN_IP = resolve_host("server.tun.vpn.lab")

            self.log(f"[*] Creating Wintun adapter 'AllenVPN'...")
            self.adapter = create_adapter("AllenVPN")

            self.log(f"[*] Starting session (Persist=True)...")
            self.session = start_session(self.adapter)

            self.log("[+] VPN Interface is active.")
            self.is_running = True
            self.client_ip = CLIENT_IP
            return True

        except Exception as e:
            self.log(f"[!] Failed to connect: {e}")
            self.cleanup()
            return False

    def disconnect(self):
        self.log("[*] Disconnecting...")
        self.cleanup()
        self.log("[+] Disconnected.")

    def cleanup(self):
        if self.session:
            try:
                end_session(self.session)
            except Exception as e:
                self.log(f"[!] Error ending session: {e}")
            self.session = None

        if self.adapter:
            try:
                close_adapter(self.adapter)
            except Exception as e:
                self.log(f"[!] Error closing adapter: {e}")
            self.adapter = None

        self.is_running = False


# For running standalone (optional)
if __name__ == "__main__":
    vpn = VPNCore()
    try:
        vpn.connect()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        vpn.disconnect()
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        vpn.cleanup()
        sys.exit(0)