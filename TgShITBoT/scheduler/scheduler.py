from TgShITBoT.logger import LOGGER
from TgShITBoT.scheduler.jobs import admin_folder_sync_job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

log = LOGGER(__name__)


def start_scheduler(client) -> AsyncIOScheduler:
    """Initialize APScheduler and register all periodic jobs."""
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        admin_folder_sync_job,
        "interval",
        hours=12,
        args=[client],
        id="admin_folder_sync",
        replace_existing=True,
    )

    scheduler.start()
    log.info("Scheduler started.")
    return scheduler
