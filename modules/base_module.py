from abc import ABC, abstractmethod
from utils.logger import setup_logger

class BaseModule(ABC):
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.logger = setup_logger(self.__class__.__name__)

    @abstractmethod
    def execute(self) -> bool:
        pass

    @abstractmethod
    def rollback(self) -> bool:
        pass

    def run_safe(self) -> bool:
        if self.dry_run:
            self.logger.info(f"[DRY-RUN] Skipping execution: {self.__class__.__name__}")
            return True
        try:
            return self.execute()
        except Exception as e:
            self.logger.error(f"Execution failed: {e}")
            return False
