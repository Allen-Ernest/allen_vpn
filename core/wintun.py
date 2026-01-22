import ctypes
from ctypes import wintypes
import os

dll_dir = os.path.dirname(os.path.abspath(__file__))
os.add_dll_directory(dll_dir)

wintun = ctypes.WinDLL(os.path.join(dll_dir, "wintun.dll"))

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]
    
WINTUN_ADAPTER_HANDLE = wintypes.HANDLE
WINTUN_SESSION_HANDLE = wintypes.HANDLE

wintun.WintunCreateAdapter.argtypes = [
    wintypes.LPCWSTR,        # adapter name
    wintypes.LPCWSTR,        # tunnel type
    ctypes.POINTER(GUID)     # optional GUID
]
wintun.WintunCreateAdapter.restype = WINTUN_ADAPTER_HANDLE

wintun.WintunStartSession.argtypes = [
    WINTUN_ADAPTER_HANDLE,
    wintypes.DWORD            # capacity
]
wintun.WintunStartSession.restype = WINTUN_SESSION_HANDLE

wintun.WintunReceivePacket.argtypes = [
    WINTUN_SESSION_HANDLE,
    ctypes.POINTER(wintypes.DWORD)
]
wintun.WintunReceivePacket.restype = ctypes.POINTER(ctypes.c_ubyte)

wintun.WintunReleaseReceivePacket.argtypes = [
    WINTUN_SESSION_HANDLE,
    ctypes.POINTER(ctypes.c_ubyte)
]

wintun.WintunAllocateSendPacket.argtypes = [
    WINTUN_SESSION_HANDLE,
    wintypes.DWORD
]
wintun.WintunAllocateSendPacket.restype = ctypes.POINTER(ctypes.c_ubyte)

wintun.WintunSendPacket.argtypes = [
    WINTUN_SESSION_HANDLE,
    ctypes.POINTER(ctypes.c_ubyte)
]

def create_adapter(name="LabVPN", tunnel_type="VPN"):
    adapter = wintun.WintunCreateAdapter(
        name,
        tunnel_type,
        None  # Let Windows auto-generate GUID
    )

    if not adapter:
        raise OSError("Failed to create Wintun adapter")

    return adapter

def start_session(adapter, capacity=0x400000):  # 4MB ring buffer
    session = wintun.WintunStartSession(adapter, capacity)

    if not session:
        raise OSError("Failed to start Wintun session")

    return session

def send_packet(session, data: bytes):
    size = len(data)
    buf = wintun.WintunAllocateSendPacket(session, size)
    if not buf:
        return

    ctypes.memmove(buf, data, size)
    wintun.WintunSendPacket(session, buf)