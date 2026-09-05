from TgShITBoT.utils.admin_folder import sync_admin_folder


async def admin_folder_sync_job(client) -> None:
    """Scheduled job: full admin folder sync (runs every 12 hours)."""
    await sync_admin_folder(client)
