import customtkinter
import time

customtkinter.set_appearance_mode("system")

root = customtkinter.CTk()
root.title("Allen VPN")
root.geometry("400x300")

# =========================
# STATE
# =========================
vpn_connected = False
start_time = 0

# =========================
# LABEL
# =========================
time_label = customtkinter.CTkLabel(
    root,
    text="00:00:00",
    font=("Segoe UI", 24)
)
time_label.pack(pady=20)

# =========================
# TIMER LOGIC
# =========================
def update_timer():
    if vpn_connected:
        elapsed = int(time.time() - start_time)

        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60

        time_label.configure(text=f"{h:02}:{m:02}:{s:02}")

        # call again after 1 second
        root.after(1000, update_timer)

# =========================
# BUTTON ACTION
# =========================
def connect_vpn():
    global vpn_connected, start_time

    if not vpn_connected:
        vpn_connected = True
        start_time = time.time()
        my_button.configure(text="Disconnect VPN")
        update_timer()
    else:
        vpn_connected = False
        my_button.configure(text="Connect VPN")

# =========================
# BUTTON
# =========================
my_button = customtkinter.CTkButton(
    master=root,
    text="Connect VPN",
    command=connect_vpn
)
my_button.pack(pady=20)

root.mainloop()

#TODO: Button should be have rounded corners