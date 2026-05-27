import logging
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

class CognitiveScheduler:
    """
    Priority-Based Cognitive Scheduling.
    Allocates attention dynamically based on weighted strategic priority scores.
    """
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.sector_priorities: Dict[str, float] = {}
        self.job_mapping: Dict[str, str] = {} # target -> job_id
        
        self.BASE_INTERVAL_SEC = 300 # 5 minutes

    def start(self):
        self.scheduler.start()
        logger.info("Cognitive Scheduler started.")

    def shutdown(self):
        self.scheduler.shutdown()
        logger.info("Cognitive Scheduler shut down.")

    def calculate_priority_interval(self, target: str, sector: str) -> int:
        """
        Derives polling interval based on the priority score.
        Formula: priority_score = volatility + convergence_strength + sector_impact + temporal_density + confidence
        """
        priority = self.sector_priorities.get(sector, 0.0)
        
        # Max priority = 100. Higher priority means lower interval (faster polling).
        # At 0 priority -> 300s (5m)
        # At 100 priority -> 30s
        reduction_ratio = min(priority, 100) / 100.0
        interval = self.BASE_INTERVAL_SEC - int((self.BASE_INTERVAL_SEC - 30) * reduction_ratio)
        return max(30, interval)

    def register_target_job(self, target: str, sector: str, func, *args):
        interval = self.calculate_priority_interval(target, sector)
        job = self.scheduler.add_job(func, 'interval', seconds=interval, args=args, id=target, replace_existing=True)
        self.job_mapping[target] = job.id
        logger.info(f"Registered cognitive watch job for {target} at {interval}s interval.")

    def update_sector_priority(self, sector: str, new_priority: float):
        old_priority = self.sector_priorities.get(sector, 0.0)
        self.sector_priorities[sector] = new_priority
        logger.info(f"Sector {sector} priority updated: {old_priority} -> {new_priority}")
        
        # Trigger interval recalculations for jobs in this sector (simplified for demo to just log)
        # In a real system, we'd iterate over all targets in this sector and reschedule them.

cognitive_scheduler = CognitiveScheduler()
