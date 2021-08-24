from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

headers = {'content-type': 'application/json', 'charset': 'utf-8', 'connection': 'close',
           'Authorization': 'Basic ZGljdGlvbmFyaWVzOlhFVTlwRWJPekI1MmdwOEdhVWkwYlRH'}

companies_url = 'https://dev.newton-technology.ru/api/dictionary/instrument'
metrics_url = f'https://dev.newton-technology.ru/api/financials/instrument/metrics'


