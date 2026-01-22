import customtkinter as ctk
from client import VPNService
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VPNApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.vpn = VPNService()
        self.vpn.set_callbacks(log_cb=self.add_log, status_cb=self.update_status_ui)

        self.show_ip = False

        self.title("LabVPN")
        self.geometry("900x550")
        self.minsize(850, 520)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ─── Sidebar ─────────────────────────────────────────
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar,
            text="LabVPN",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(40, 10))

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="Disconnected",
            text_color="#E74C3C",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=10)

        self.timer_label = ctk.CTkLabel(
            self.sidebar,
            text="00:00:00",
            font=ctk.CTkFont(family="Courier", size=18)
        )
        self.timer_label.pack(pady=5)

        # ─── Main Area ───────────────────────────────────────
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Connection Card
        self.card = ctk.CTkFrame(self.main, corner_radius=16)
        self.card.pack(fill="x", pady=(0, 20))

        self.conn_button = ctk.CTkButton(
            self.card,
            text="CONNECT",
            height=55,
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.toggle_vpn
        )
        self.conn_button.pack(pady=20)

        # Stats Row
        self.stats = ctk.CTkFrame(self.card, fg_color="transparent")
        self.stats.pack(fill="x", padx=20, pady=(0, 20))

        self.speed_label = ctk.CTkLabel(self.stats, text="↓ 0 KB/s   ↑ 0 KB/s")
        self.speed_label.pack(side="left")

        self.ip_label = ctk.CTkLabel(self.stats, text="IP: ***.***.***.***")
        self.ip_label.pack(side="right")

        self.ip_toggle = ctk.CTkButton(
            self.card,
            text="👁 Show IP",
            width=120,
            command=self.toggle_ip
        )
        self.ip_toggle.pack(pady=(0, 15))

        # ─── Terminal ────────────────────────────────────────
        self.log_view = ctk.CTkTextbox(
            self.main,
            corner_radius=12,
            fg_color="#0f0f0f",
            text_color="#33FF33",
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.log_view.pack(fill="both", expand=True)

        self.add_log("System initialized. Awaiting connection.")

        self.update_clock()
        self.update_speed()

    # ─── Actions ───────────────────────────────────────────
    def toggle_vpn(self):
        if not self.vpn.connected:
            self.vpn.connect()
        else:
            self.vpn.disconnect()

    def toggle_ip(self):
        self.show_ip = not self.show_ip
        if self.show_ip:
            self.ip_label.configure(text=f"IP: {self.vpn.get_ip()}")
            self.ip_toggle.configure(text="🙈 Hide IP")
        else:
            self.ip_label.configure(text="IP: ***.***.***.***")
            self.ip_toggle.configure(text="👁 Show IP")

    def update_status_ui(self, status):
        self.status_label.configure(text=status)

        if status == "Connected":
            self.status_label.configure(text_color="#2ECC71")
            self.conn_button.configure(text="DISCONNECT", fg_color="#C0392B")
        elif status == "Connecting":
            self.status_label.configure(text_color="#F1C40F")
        else:
            self.status_label.configure(text_color="#E74C3C")
            self.conn_button.configure(text="CONNECT", fg_color="#1F6AA5")

    def add_log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log_view.insert("end", f"[{ts}] {msg}\n")
        self.log_view.see("end")

    def update_clock(self):
        self.timer_label.configure(text=self.vpn.get_duration())
        self.after(1000, self.update_clock)

    def update_speed(self):
        if self.vpn.connected:
            down, up = self.vpn.get_speed()
            self.speed_label.configure(text=f"↓ {down} KB/s   ↑ {up} KB/s")
        self.after(1000, self.update_speed)


if __name__ == "__main__":
    VPNApp().mainloop()
