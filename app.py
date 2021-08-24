import json
import logging
from typing import List, Any
from aiogram import executor

from data_refreshment import collect_companies_data
from loader import dp, storage, bot, scheduler
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


def schedule_jobs():
    scheduler.add_job(collect_companies_data, "interval", days=1, args=(dp,))


async def on_startup(dispatcher):
    filters.setup(dispatcher)
    middlewares.setup(dispatcher)

    await set_default_commands(dispatcher)
    logging.info("Бот запущен !)")
    await on_startup_notify(dispatcher)
    schedule_jobs()


async def on_shutdown(dispatcher):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
