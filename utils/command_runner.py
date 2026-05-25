import subprocess
import logging
from typing import List, Optional

class CommandRunner:
    def __init__(self, logger: logging.Logger, dry_run: bool = False):
        self.logger = logger
        self.dry_run = dry_run

    def run(self, cmd: List[str], check: bool = True, timeout: int = 30) -> Optional[subprocess.CompletedProcess]:
        cmd_str = " ".join(cmd)
        if self.dry_run:
            self.logger.info(f"[DRY-RUN] Would execute: {cmd_str}")
            return None
        
        self.logger.info(f"Executing: {cmd_str}")
        try:
            return subprocess.run(
                cmd, check=check, capture_output=True, text=True, timeout=timeout
            )
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {cmd_str}")
            raise
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed (code {e.returncode}): {e.stderr.strip()}")
            raise
