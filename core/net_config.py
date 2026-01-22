import socket

def resolve_host(hostname):
    return socket.gethostbyname(hostname)