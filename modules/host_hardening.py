from .base_module import BaseModule
from utils.platform import get_os, OS_CONFIG
from utils.command_runner import CommandRunner
from utils.backup import create_backup
import os

class HostHardening(BaseModule):
    def execute(self) -> bool:
        os_name = get_os()
        runner = CommandRunner(self.logger, self.dry_run)
        
        if os_name == "linux":
            self._harden_linux(runner)
        elif os_name == "windows":
            self._harden_windows(runner)
        elif os_name == "macos":
            self._harden_macos(runner)
        return True

    def rollback(self) -> bool:
        self.logger.info("Host rollback: Restoring from backups...")
        # Implement restore logic using utils/backup.py
        return True

    def _harden_linux(self, runner: CommandRunner):
        runner.run(["sysctl", "-w", "net.ipv4.conf.all.accept_redirects=0"])
        ssh_cfg = "/etc/ssh/sshd_config"
        if os.path.exists(ssh_cfg):
            create_backup(ssh_cfg, OS_CONFIG["linux"]["backup_dir"])

    def _harden_windows(self, runner: CommandRunner):
        runner.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"])
        runner.run(["powershell", "-Command", "Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart"])

    def _harden_macos(self, runner: CommandRunner):
        runner.run(["defaults", "write", "com.apple.screensaver", "askForPassword", "-int", "1"])
        runner.run(["defaults", "write", "com.apple.screensaver", "askForPasswordDelay", "-int", "5"])
