import json
import logging
from typing import List, Any
import aiohttp
from aiogram import Dispatcher

from data.config import ADMINS
from loader import companies_url, headers

companies_info: List[Any]


async def collect_companies_data(dp: Dispatcher):
    async with aiohttp.ClientSession() as session:
        async with session.get(companies_url, headers=headers) as response:
            print("Status:", response.status)
            with open('data.json', mode='w', encoding='utf-8') as f:
                json.dump(await response.json(), f)
            for admin in ADMINS:
                try:
                    logging.info("Обновил данные в файле data.json. Данные получены из API")

                except Exception as err:
                    logging.exception(err)

# Примерно такое создание job как ниже

