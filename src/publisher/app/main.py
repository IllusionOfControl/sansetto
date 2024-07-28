import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.tasks import task_publish_image


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(task_publish_image, CronTrigger(minute="15"))
    scheduler.start()
