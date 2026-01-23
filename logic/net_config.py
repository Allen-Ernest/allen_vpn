import socket

def resolve_host(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        print(f"[DNS] {hostname} -> {ip}")
        return ip
    except socket.gaierror:
        print(f"[DNS ERROR] Failed to resolve {hostname}")
        return None