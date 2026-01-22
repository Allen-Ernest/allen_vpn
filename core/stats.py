import random

class VPNStats:
    def __init__(self):
        self.show_ip = True

    def get_ip(self):
        return "10.10.0.2" if self.show_ip else "Hidden"

    def toggle_ip_visibility(self):
        self.show_ip = not self.show_ip

    def get_speed(self):
        down = random.uniform(5, 50)
        up = random.uniform(2, 20)
        return f"{down:.1f} Mbps ↓ | {up:.1f} Mbps ↑"
