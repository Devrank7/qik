import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from db.sql.connect import init_db
from routers import start_router, pay_router, join_router, stripe_router
from scheduler.scheduler import scheduler
from scheduler.tasks import MonitorUser
from apscheduler.triggers.interval import IntervalTrigger

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
CHAT_ID = os.getenv('CHAT_ID')
routers = [
    start_router.router,
    pay_router.router,
    join_router.router,
    stripe_router.router,
]
tasks = [
    {"executor": MonitorUser, "args": (bot, CHAT_ID)},
]


async def main():
    print("Start bot!")
    for router in routers:
        dp.include_router(router)
    for task in tasks:
        scheduler.add_job(task["executor"](*task['args']).task, IntervalTrigger(minutes=1))
    await init_db()
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Interrupted")
        scheduler.shutdown()
