import customtkinter as ctk

class StatusBadge(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(
            master,
            text="Disconnected",
            fg_color="#2a2a2a",
            corner_radius=20,
            width=140,
            height=35,
            font=("Segoe UI", 14, "bold")
        )

    def set_status(self, status):
        colors = {
            "Connected": "#1f7a1f",
            "Disconnected": "#7a1f1f",
            "Error": "#7a3f1f"
        }
        self.configure(text=status, fg_color=colors.get(status, "#2a2a2a"))
