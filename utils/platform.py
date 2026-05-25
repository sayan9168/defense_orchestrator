import platform
import sys
from pathlib import Path

def get_os() -> str:
    sys_name = platform.system().lower()
    if sys_name == "linux":
        return "linux"
    elif sys_name == "windows":
        return "windows"
    elif sys_name == "darwin":
        return "macos"
    else:
        print(f"[❌] Unsupported OS: {platform.system()}")
        sys.exit(1)

# OS-specific safe paths & defaults
OS_CONFIG = {
    "linux": {
        "backup_dir": "/var/backups/defense_orchestrator",
        "log_dir": "/var/log/defense_orchestrator",
        "service_mgr": "systemctl",
    },
    "windows": {
        "backup_dir": "C:\\ProgramData\\DefenseOrchestrator\\Backups",
        "log_dir": "C:\\ProgramData\\DefenseOrchestrator\\Logs",
        "service_mgr": "sc",
    },
    "macos": {
        "backup_dir": "/var/backups/defense_orchestrator",
        "log_dir": "/var/log/defense_orchestrator",
        "service_mgr": "launchctl",
    }
}
