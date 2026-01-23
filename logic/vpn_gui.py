# gui.py
import customtkinter as ctk
import threading
import queue
from client import VPNCore


ctk.set_appearance_mode("dark")       # "dark", "light", "system"
ctk.set_default_color_theme("blue")   # "blue", "dark-blue", "green"


class VPNGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AllenVPN")
        self.geometry("420x520")
        self.resizable(False, False)

        self.vpn = VPNCore()
        self.vpn.set_log_callback(self.append_log)

        self.log_queue = queue.Queue()
        self.after(100, self.process_log_queue)

        self.is_connecting = False
        self.show_ip = ctk.BooleanVar(value=False)

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(self, text="AllenVPN", font=("Segoe UI", 24, "bold"))
        header.pack(pady=(30, 10))

        status_frame = ctk.CTkFrame(self, fg_color="transparent")
        status_frame.pack(pady=10, padx=40, fill="x")

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Disconnected",
            font=("Segoe UI", 18),
            text_color="#ff5555"
        )
        self.status_label.pack()

        self.ip_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        self.ip_frame.pack(pady=(10, 0))

        ctk.CTkLabel(self.ip_frame, text="Client IP:", font=("Segoe UI", 12)).pack(side="left", padx=(0, 8))
        self.ip_value_label = ctk.CTkLabel(
            self.ip_frame,
            text="— — — —",
            font=("Consolas", 13),
            text_color="#bbbbbb"
        )
        self.ip_value_label.pack(side="left")

        # Toggle IP visibility (placeholder for future real IP)
        ctk.CTkCheckBox(
            self.ip_frame,
            text="Show",
            variable=self.show_ip,
            command=self.toggle_ip_visibility
        ).pack(side="left", padx=(12, 0))

        # Big connect button
        self.connect_btn = ctk.CTkButton(
            self,
            text="CONNECT",
            font=("Segoe UI", 16, "bold"),
            height=60,
            corner_radius=16,
            command=self.toggle_connection
        )
        self.connect_btn.pack(pady=(30, 10), padx=60, fill="x")

        # Log area
        log_label = ctk.CTkLabel(self, text="Activity Log", font=("Segoe UI", 14))
        log_label.pack(pady=(10, 5))

        self.log_text = ctk.CTkTextbox(
            self,
            height=140,
            state="disabled",
            font=("Consolas", 12),
            wrap="word"
        )
        self.log_text.pack(padx=30, pady=(0, 20), fill="both", expand=True)

        self.append_log("Application started.")

    def append_log(self, message: str):
        self.log_queue.put(message)

    def process_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.configure(state="normal")
                self.log_text.insert("end", msg + "\n")
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(80, self.process_log_queue)

    def toggle_ip_visibility(self):
        if self.show_ip.get() and self.vpn.is_running:
            ip = self.vpn.client_ip or "— — — —"
            self.ip_value_label.configure(text=ip)
        else:
            self.ip_value_label.configure(text="— — — —")

    def toggle_connection(self):
        if self.is_connecting:
            return

        if self.vpn.is_running:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        self.is_connecting = True
        self.connect_btn.configure(state="disabled", text="CONNECTING...", fg_color="#444")
        self.status_label.configure(text="Connecting...", text_color="#ffaa00")

        def worker():
            success = self.vpn.connect()
            self.after(0, lambda: self._on_connect_finished(success))

        threading.Thread(target=worker, daemon=True).start()

    def disconnect(self):
        self.connect_btn.configure(state="disabled", text="DISCONNECTING...", fg_color="#444")
        self.status_label.configure(text="Disconnecting...", text_color="#ffaa00")

        def worker():
            self.vpn.disconnect()
            self.after(0, self._on_disconnect_finished)

        threading.Thread(target=worker, daemon=True).start()

    def _on_connect_finished(self, success: bool):
        self.is_connecting = False
        self.connect_btn.configure(state="normal")

        if success:
            self.connect_btn.configure(text="DISCONNECT", fg_color="#e63946")
            self.status_label.configure(text="Connected", text_color="#76ff72")
            if self.show_ip.get():
                self.ip_value_label.configure(text=self.vpn.client_ip or "— — — —")
        else:
            self.connect_btn.configure(text="CONNECT", fg_color=("#3b82f6", "#2563eb"))
            self.status_label.configure(text="Connection failed", text_color="#ff5555")
            self.ip_value_label.configure(text="— — — —")

    def _on_disconnect_finished(self):
        self.connect_btn.configure(
            text="CONNECT",
            fg_color=("#3b82f6", "#2563eb"),
            state="normal"
        )
        self.status_label.configure(text="Disconnected", text_color="#ff5555")

    def on_closing(self):
        if self.vpn.is_running:
            self.vpn.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = VPNGUI()
    app.mainloop()