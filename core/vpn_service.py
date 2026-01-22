import time
import threading
from .net_config import resolve_host
from .wintun import create_adapter, start_session

class VPNService:
    def __init__(self):
        self.connected = False
        self.start_time = None
        self.adapter = None
        self.session = None
        self.log_callback = None
        self.status_callback = None

    def set_callbacks(self, log_cb=None, status_cb=None):
        self.log_callback = log_cb
        self.status_callback = status_cb

    def log(self, msg):
        if self.log_callback:
            self.log_callback(msg)

    def update_status(self, status):
        if self.status_callback:
            self.status_callback(status)

    def connect(self):
        def run():
            try:
                self.log("Resolving VPN server...")
                server_ip = resolve_host("vpn.vpn.lab")

                self.log(f"Server resolved: {server_ip}")
                self.log("Creating VPN adapter...")

                self.adapter = create_adapter("LabVPN", "VPN")
                self.session = start_session(self.adapter)

                self.connected = True
                self.start_time = time.time()

                self.update_status("Connected")
                self.log("VPN connected successfully")

                while self.connected:
                    time.sleep(1)

            except Exception as e:
                self.log(f"Error: {e}")
                self.update_status("Error")

        threading.Thread(target=run, daemon=True).start()

    def disconnect(self):
        self.connected = False
        self.update_status("Disconnected")
        self.log("VPN disconnected")

    def get_duration(self):
        if not self.connected:
            return "00:00:00"
        elapsed = int(time.time() - self.start_time)
        h, rem = divmod(elapsed, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02}:{m:02}:{s:02}"
