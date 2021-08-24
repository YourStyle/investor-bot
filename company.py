import asyncio

import requests
from aiogram.types import InputFile
import json
from typing import Dict, Union

import aiohttp
from PIL import Image, ImageDraw, ImageFont

with open("data.json", "r") as f:
    companies_info = json.load(f)


class Company:
    def __init__(self, name: str, command: str, ticker=False):
        self.name: str = name
        self.ticker: bool = ticker

        # """Блок для генерации запроса к API"""

        self.url: str = 'https://dev.newton-technology.ru/api/financials/instrument/metrics'
        self.headers: Dict = {'content-type': 'application/json', 'charset': 'utf-8', 'connection': 'close',
                              'Authorization': 'Basic ZGljdGlvbmFyaWVzOlhFVTlwRWJPekI1MmdwOEdhVWkwYlRH'}

        self.instrument_id: Union[int, None] = self._find_symbol()
        self.types: list = self._define_metrics(command)
        self.period: str = "ann"
        self.standard: str = "ifrs"
        self.years: int = 1

        self.payload = {
            "instrumentIds": [self.instrument_id],
            "types": self.types,
            "periodType": self.period,
            "standard": self.standard,
            "yearsCount": self.years
        }
        # """Конец блока"""
        self.command: str = command
        self.fYear: str = "Неизвестен"

    def _find_symbol(self):
        if self.ticker:
            for i in range(len(companies_info)):
                if companies_info[i]['ticker'].lower() == self.name.lower():
                    self.name = companies_info[i]['issuerName'].capitalize()
                    return companies_info[i]['id']
            if True:
                return None

        else:
            for i in range(len(companies_info)):
                if companies_info[i]['issuerName'].lower() == self.name.lower():
                    self.name = companies_info[i]['issuerName'].capitalize()
                    return companies_info[i]['id']
            if True:
                return None


    def _define_metrics(self, muliplicator: str):
        if muliplicator == "mult":
            return ["capitalization"]
        elif muliplicator == "pe":
            return ["capitalization", "earnings"]
        elif muliplicator == "cap":
            return ["capitalization"]
        elif muliplicator == "cash":
            return ["total_cash"]
        elif muliplicator == "debt":
            return ["total_debt"]
        elif muliplicator == "sales":
            return ["revenue"]
        elif muliplicator == "fcf":
            return ["net_op_cashflow"]
        elif muliplicator == "ebitda":
            return ["ebitda"]
        elif muliplicator == "ps":
            return ["earnings", "capitalization"]
        elif muliplicator == "pb":
            return ["capital", "capitalization"]
        elif muliplicator == "eve":
            return ["ebitda", "total_debt", "capitalization"]
        elif muliplicator == "nde":
            return ["ebitda", "total_debt"]
        # elif muliplicator == "dividend":
        #     return ["total_debt"]
        elif muliplicator == "earnin":
            return ["revenue"]
        elif muliplicator == "roa":
            return ["assets", "earnings"]
        elif muliplicator == "ros":
            return ["revenue", "earnings"]

    def generate_request(self):
        if self.instrument_id is not None:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(self.payload))
            company_data = response.json()[f"{self.instrument_id}"]
            metrics = list(company_data.keys())
            return [company_data, metrics]
        else:
            return f"В базе нет компании с названием {self.name}"

    def check_response(self):
        request = self.generate_request()

        metrics = request[1]
        if type(request) == list:
            mult = str(request[0][f"{metrics[0]}"][0]["value"]/1000000000000)
            self.fYear = request[0][f"{metrics[0]}"][0]["fiscalYear"]
            var = self.collect_im()
            self.draw_text(var, mult, self.fYear)
            return self.save_gif(var)
        else:
            return f"В базе нет компании с названием {self.name}"

    def collect_im(self):
        frames = []
        for frame_number in range(0, 107):
            if frame_number < 10:
                frame = Image.open(f'Shield/Shield_0000{frame_number}.png')
            elif frame_number < 100:
                frame = Image.open(f'Shield/Shield_000{frame_number}.png')
            elif frame_number < 1000:
                frame = Image.open(f'Shield/Shield_00{frame_number}.png')
            frames.append(frame)
        return frames

    def draw_text(self, fr_collection, collected_data, year):
        for frame in fr_collection:
            idraw = ImageDraw.Draw(frame)
            font = ImageFont.truetype("GILROY-BOLD.TTF", size=30)
            idraw.text((155, 100), f"{collected_data:.4} трлн", fill="white", font=font)
            font = ImageFont.truetype("GILROY-BOLD.TTF", size=15)
            idraw.text((120, 220), f"Кап. {self.name}а", fill="black", font=font)
            font = ImageFont.truetype("GILROY-BOLD.TTF", size=15)
            idraw.text((160, 250), f"За {year} год", fill="black", font=font)
        return fr_collection

    def save_gif(self, fr_collection):
        fr_collection[0].save(
            'shield.gif',
            save_all=True,
            append_images=fr_collection,
            optimize=True,
            duration=50,
            loop=0
        )
        return InputFile("shield.gif")
