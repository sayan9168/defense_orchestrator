import os
import sys
import platform

def require_root() -> None:
    if platform.system() == "Windows":
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[❌] Windows Administrator privileges required.")
            sys.exit(1)
    else:
        if os.geteuid() != 0:
            print("[❌] Linux/macOS requires root (sudo).")
            sys.exit(1)
