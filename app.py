import customtkinter as ctk
import time
from datetime import datetime

# Set theme and color palette
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class AllenVPN(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Allen VPN - Secure Connection")
        self.geometry("900x600")

        # --- STATE ---
        self.is_connected = False
        self.start_time = 0
        self.ip_hidden = True
        self.mock_ip = "192.168.1.105"

        # --- LAYOUT GRID ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ======================================================
        # SIDEBAR
        # ======================================================
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="ALLEN VPN", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(30, 20))

        self.home_btn = ctk.CTkButton(self.sidebar_frame, text="Dashboard", fg_color="transparent", anchor="w")
        self.home_btn.pack(fill="x", padx=20, pady=5)

        self.server_btn = ctk.CTkButton(self.sidebar_frame, text="Server List", fg_color="transparent", anchor="w")
        self.server_btn.pack(fill="x", padx=20, pady=5)

        self.settings_btn = ctk.CTkButton(self.sidebar_frame, text="Settings", fg_color="transparent", anchor="w")
        self.settings_btn.pack(fill="x", padx=20, pady=5)

        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="v1.0.2", font=ctk.CTkFont(size=10))
        self.version_label.pack(side="bottom", pady=20)

        # ======================================================
        # MAIN DASHBOARD
        # ======================================================
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # --- Status Header ---
        self.status_card = ctk.CTkFrame(self.main_container, height=150)
        self.status_card.pack(fill="x", pady=(0, 20))

        self.status_title = ctk.CTkLabel(self.status_card, text="PROTECTION DISABLED", font=ctk.CTkFont(size=14, weight="bold"), text_color="#E74C3C")
        self.status_title.pack(pady=(20, 0))

        self.time_label = ctk.CTkLabel(self.status_card, text="00:00:00", font=ctk.CTkFont(size=48, weight="bold"))
        self.time_label.pack(pady=10)

        # --- Stats Row (IP, Speed, Location) ---
        self.stats_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=10)
        self.stats_frame.grid_columnconfigure((0,1,2), weight=1)

        # IP Address Card
        self.ip_card = ctk.CTkFrame(self.stats_frame)
        self.ip_card.grid(row=0, column=0, padx=5, sticky="nsew")
        ctk.CTkLabel(self.ip_card, text="YOUR IP").pack(pady=(10, 0))
        self.ip_display = ctk.CTkLabel(self.ip_card, text="***.***.***.***", font=ctk.CTkFont(weight="bold"))
        self.ip_display.pack()
        self.toggle_ip_btn = ctk.CTkButton(self.ip_card, text="Show", width=60, height=20, font=ctk.CTkFont(size=10), command=self.toggle_ip)
        self.toggle_ip_btn.pack(pady=(0, 10))

        # Speed Card
        self.speed_card = ctk.CTkFrame(self.stats_frame)
        self.speed_card.grid(row=0, column=1, padx=5, sticky="nsew")
        ctk.CTkLabel(self.speed_card, text="SPEED").pack(pady=(10, 0))
        self.speed_label = ctk.CTkLabel(self.speed_card, text="↓ 0.0 Mb/s  ↑ 0.0 Mb/s", font=ctk.CTkFont(weight="bold"))
        self.speed_label.pack(pady=(0, 20))

        # Location Card
        self.loc_card = ctk.CTkFrame(self.stats_frame)
        self.loc_card.grid(row=0, column=2, padx=5, sticky="nsew")
        ctk.CTkLabel(self.loc_card, text="LOCATION").pack(pady=(10, 0))
        self.loc_label = ctk.CTkLabel(self.loc_card, text="United States, NY", font=ctk.CTkFont(weight="bold"))
        self.loc_label.pack(pady=(0, 20))

        # --- Action Button ---
        self.connect_btn = ctk.CTkButton(self.main_container, text="CONNECT NOW", height=50, font=ctk.CTkFont(size=16, weight="bold"), command=self.toggle_vpn)
        self.connect_btn.pack(pady=30, fill="x")

        # --- Logs Area ---
        self.log_box = ctk.CTkTextbox(self.main_container, height=120, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.pack(fill="x")
        self.add_log("System Ready...")

    # ======================================================
    # LOGIC
    # ======================================================
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")

    def toggle_ip(self):
        if self.ip_hidden:
            self.ip_display.configure(text=self.mock_ip)
            self.toggle_ip_btn.configure(text="Hide")
            self.ip_hidden = False
        else:
            self.ip_display.configure(text="***.***.***.***")
            self.toggle_ip_btn.configure(text="Show")
            self.ip_hidden = True

    def toggle_vpn(self):
        if not self.is_connected:
            self.is_connected = True
            self.start_time = time.time()
            self.connect_btn.configure(text="DISCONNECT", fg_color="#E74C3C", hover_color="#C0392B")
            self.status_title.configure(text="CONNECTION SECURED", text_color="#2ECC71")
            self.add_log("Attempting to connect to New York Server...")
            self.add_log("Handshake successful.")
            self.add_log("VPN Connected.")
            self.update_ui_loop()
        else:
            self.is_connected = False
            self.connect_btn.configure(text="CONNECT NOW", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])
            self.status_title.configure(text="PROTECTION DISABLED", text_color="#E74C3C")
            self.speed_label.configure(text="↓ 0.0 Mb/s  ↑ 0.0 Mb/s")
            self.add_log("Disconnecting...")
            self.add_log("VPN Offline.")

    def update_ui_loop(self):
        if self.is_connected:
            # Timer calculation
            elapsed = int(time.time() - self.start_time)
            h = elapsed // 3600
            m = (elapsed % 3600) // 60
            s = elapsed % 60
            self.time_label.configure(text=f"{h:02}:{m:02}:{s:02}")

            # Mock Speed change
            import random
            down = random.uniform(20, 50)
            up = random.uniform(5, 15)
            self.speed_label.configure(text=f"↓ {down:.1f} Mb/s  ↑ {up:.1f} Mb/s")

            self.after(1000, self.update_ui_loop)

if __name__ == "__main__":
    app = AllenVPN()
    app.mainloop()