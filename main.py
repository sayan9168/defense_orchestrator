import click
import yaml
import os
from pathlib import Path
from utils.priv_check import require_root
from utils.logger import setup_logger
from modules.host_hardening import HostHardening
from modules.network_defense import NetworkDefense
from modules.logging_monitoring import LoggingMonitoring

def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

@click.command()
@click.option("--dry-run/--no-dry-run", default=None, help="Override config dry-run setting")
@click.option("--config", default="config.yaml", help="Path to config.yaml")
def main(dry_run, config):
    cfg = load_config(config)
    run_dry = dry_run if dry_run is not None else cfg["orchestrator"]["dry_run"]
    
    log = setup_logger("orchestrator")
    log.info(f"Starting Defense Orchestrator | dry_run={run_dry}")
    
    require_root()
    
    modules_map = {
        "host_hardening": HostHardening,
        "network_defense": NetworkDefense,
        "logging_monitoring": LoggingMonitoring,
    }
    
    for name, cls in modules_map.items():
        if cfg["orchestrator"]["modules"].get(name, False):
            mod = cls(dry_run=run_dry)
            success = mod.run_safe()
            if not success:
                log.warning(f"Module {name} failed. Continuing...")
    
    log.info("Orchestration completed.")

if __name__ == "__main__":
    main()
