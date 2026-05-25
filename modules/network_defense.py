from .base_module import BaseModule
from utils.platform import get_os
from utils.command_runner import CommandRunner

class NetworkDefense(BaseModule):
    def execute(self) -> bool:
        os_name = get_os()
        runner = CommandRunner(self.logger, self.dry_run)
        
        if os_name == "linux":
            runner.run(["ufw", "--force", "enable"])
            runner.run(["ufw", "default", "deny", "incoming"])
        elif os_name == "windows":
            runner.run(["netsh", "advfirewall", "set", "allprofiles", "policy", "blockinboundalways"])
            runner.run(["netsh", "advfirewall", "set", "allprofiles", "policy", "blockoutbound", "disable"])
        elif os_name == "macos":
            runner.run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--setglobalstate", "on"])
            runner.run(["/usr/libexec/ApplicationFirewall/socketfilterfw", "--setstealthmode", "on"])
        return True

    def rollback(self) -> bool:
        self.logger.info("Network rollback: Restoring firewall state...")
        return True
