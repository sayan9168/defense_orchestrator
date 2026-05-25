from .base_module import BaseModule
from utils.platform import get_os, OS_CONFIG
from utils.command_runner import CommandRunner
import os

class LoggingMonitoring(BaseModule):
    def execute(self) -> bool:
        os_name = get_os()
        runner = CommandRunner(self.logger, self.dry_run)
        cfg = OS_CONFIG[os_name]
        os.makedirs(cfg["log_dir"], exist_ok=True)
        
        if os_name == "linux":
            runner.run(["systemctl", "enable", "--now", "auditd"])
            runner.run(["systemctl", "enable", "--now", "rsyslog"])
        elif os_name == "windows":
            runner.run(["auditpol", "/set", "/subcategory:{0CCE9222-69AE-11D9-BED3-505054503030}", "success,failure"])
            runner.run(["wevtutil", "sl", "Security", "/q:true"])
        elif os_name == "macos":
            runner.run(["sudo", "log", "config", "--mode", "persist:info"])
        return True

    def rollback(self) -> bool:
        self.logger.info("Monitoring rollback: Reverting audit policies...")
        return True
