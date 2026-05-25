import os
import shutil
import datetime
from pathlib import Path

def create_backup(file_path: str, backup_dir: str) -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(backup_dir) / f"{Path(file_path).name}.{ts}.bak"
    os.makedirs(backup_dir, exist_ok=True)
    if Path(file_path).exists():
        shutil.copy2(file_path, backup_path)
    return str(backup_path)
