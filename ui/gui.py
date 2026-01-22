import customtkinter as ctk
#from core.vpn_service import VPNService
from core.stats import VPNStats
from ui.widgets import StatusBadge
from ui.animated_button import AnimatedConnectButton


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class VPNApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LabVPN")
        self.geometry("520x600")
        self.resizable(False, False)

        self.vpn = VPNService()
        self.stats = VPNStats()

        self.vpn.set_callbacks(
            log_cb=self.add_log,
            status_cb=self.update_status
        )

        self.create_ui()
        self.update_ui_loop()

    def create_ui(self):
        self.status = StatusBadge(self)
        self.status.pack(pady=20)

        self.connect_btn = AnimatedConnectButton(
            self,
            command=self.toggle_connection
        )
        self.connect_btn.pack(pady=20)

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", padx=20, pady=10)

        self.ip_label = ctk.CTkLabel(self.info_frame, text="IP: Hidden")
        self.ip_label.pack(anchor="w", padx=15, pady=5)

        self.speed_label = ctk.CTkLabel(self.info_frame, text="Speed: --")
        self.speed_label.pack(anchor="w", padx=15, pady=5)

        self.time_label = ctk.CTkLabel(self.info_frame, text="Duration: 00:00:00")
        self.time_label.pack(anchor="w", padx=15, pady=5)

        self.log_box = ctk.CTkTextbox(self, height=200)
        self.log_box.pack(fill="both", padx=20, pady=10)

    def toggle_connection(self):
        if not self.vpn.connected:
            self.update_status("Connecting")
            self.vpn.connect()
        else:
            self.vpn.disconnect()

    def update_status(self, status):
        self.status.set_status(status)
        self.connect_btn.set_status(status)

    def add_log(self, msg):
        self.log_box.insert("end", f"{msg}\n")
        self.log_box.see("end")

    def update_ui_loop(self):
        self.ip_label.configure(text=f"IP: {self.stats.get_ip()}")
        self.speed_label.configure(text=f"Speed: {self.stats.get_speed()}")
        self.time_label.configure(text=f"Duration: {self.vpn.get_duration()}")
        self.after(1000, self.update_ui_loop)
