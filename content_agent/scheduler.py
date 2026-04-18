"""APScheduler-driven daily cron.

Registers one job per slot per platform at the local time from schedule.yaml.
The scheduler stays in the foreground; SIGINT shuts it down cleanly.
"""

from __future__ import annotations

import logging
import signal

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from .agent import ContentAgent
from .config import Settings, SlotSpec

log = logging.getLogger(__name__)


def run_scheduler(settings: Settings) -> None:
    agent = ContentAgent(settings)
    sched = BlockingScheduler(timezone=settings.timezone)

    for platform in ("tiktok", "instagram", "youtube"):
        for slot in settings.schedule.slots_for(platform):
            _register_slot(sched, agent, platform, slot)

    def _graceful(*_):
        log.info("shutdown signal received")
        sched.shutdown(wait=False)

    signal.signal(signal.SIGINT, _graceful)
    signal.signal(signal.SIGTERM, _graceful)

    log.info("scheduler started — %d jobs registered", len(sched.get_jobs()))
    sched.start()


def _register_slot(sched: BlockingScheduler, agent: ContentAgent, platform: str, slot: SlotSpec) -> None:
    hour, minute = (int(x) for x in slot.time.split(":"))
    trigger = CronTrigger(hour=hour, minute=minute)

    def _job(platform=platform, slot=slot):
        try:
            agent.run_slot(platform, slot)
        except Exception:
            log.exception("job failed: %s @ %s", platform, slot.time)

    sched.add_job(_job, trigger=trigger, id=f"{platform}-{slot.time}",
                  replace_existing=True, misfire_grace_time=3600)
    log.info("registered %s @ %s (%s)", platform, slot.time, slot.theme)
