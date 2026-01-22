import customtkinter as ctk
import math

class AnimatedConnectButton(ctk.CTkCanvas):
    def __init__(self, master, command):
        
        bg_color = master.cget("bg")
        
        super().__init__(
            master,
            width=160,
            height=160,
            bg=bg_color,
            highlightthickness=0
        )

        self.command = command
        self.angle = 0
        self.animating = False
        self.status = "Disconnected"

        self.bind("<Button-1>", lambda e: self.command())
        self.draw()

    def draw(self):
        self.delete("all")

        # Outer ring
        self.create_oval(10, 10, 150, 150, outline="#1f6aa5", width=6)

        # Animated arc
        if self.animating:
            self.create_arc(
                10, 10, 150, 150,
                start=self.angle,
                extent=90,
                outline="#00c853",
                style="arc",
                width=6
            )

        # Center button
        self.create_oval(40, 40, 120, 120, fill="#1f6aa5", outline="")
        self.create_text(
            80, 80,
            text="CONNECT" if self.status == "Disconnected" else "DISCONNECT",
            fill="white",
            font=("Segoe UI", 12, "bold")
        )

    def start_animation(self):
        self.animating = True
        self.animate()

    def stop_animation(self):
        self.animating = False
        self.draw()

    def animate(self):
        if self.animating:
            self.angle = (self.angle + 5) % 360
            self.draw()
            self.after(20, self.animate)

    def set_status(self, status):
        self.status = status
        if status == "Connecting":
            self.start_animation()
        else:
            self.stop_animation()
