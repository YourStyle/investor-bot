import json
import requests
from PIL import Image, ImageDraw, ImageFont
from aiogram.types import InputFile

from loader import headers, metrics_url

with open("data.json", "r") as f:
    companies_info = json.load(f)

def generate_pe(user_data: str):
    for i in range(len(companies_info)):
        if companies_info[i]['issuerName'] == user_data or companies_info[i]['ticker'] == user_data:
            search_ticker_id = companies_info[i]['id']
            company = companies_info[i]['issuerName']
            break

    payload = {
        "instrumentIds": [
            search_ticker_id
        ],
        "types": [
            "capitalization",
            "earnings"
        ],
        "periodType": "ann",
        "standard": "ifrs",
        "yearsCount": 1
    }

    request = requests.post(metrics_url, headers=headers, data=json.dumps(payload))
    company_data = request.json()[f"{search_ticker_id}"]
    print(company_data)
    # metrics = list(company_data.keys())
    #
    # pe: float = (company_data[f"{metrics[1]}"][0]["value"] / company_data[f"{metrics[0]}"][0]["value"])
    #
    # pe = int(pe)
    #
    # frames = []
    #
    # mult_data = pe
    # mult_info = "PE"
    # for frame_number in range(0, 107):
    #     if frame_number < 10:
    #         frame = Image.open(f'Shield/Shield_0000{frame_number}.png')
    #     elif frame_number < 100:
    #         frame = Image.open(f'Shield/Shield_000{frame_number}.png')
    #     elif frame_number < 1000:
    #         frame = Image.open(f'Shield/Shield_00{frame_number}.png')
    #     # Открываем изображение каждого кадра.
    #     width, height = frame.size
    #     idraw = ImageDraw.Draw(frame)
    #     font = ImageFont.truetype("GILROY-BOLD.TTF", size=50)
    #     white = '#ffffff'
    #     idraw.text((175, 100), f"{mult_data}", fill=white, font=font)
    #     idraw.text((175, 250), f"{mult_info}", fill=white, font=font)
    #     # Добавляем кадр в список с кадрами.
    #     frames.append(frame)
    #
    # # Берем первый кадр и в него добавляем оставшееся кадры.
    # frames[0].save(
    #     'shield.gif',
    #     save_all=True,
    #     append_images=frames,
    #     optimize=True,
    #     duration=50,
    #     loop=0
    # )
    #
    # photo = InputFile("shield.gif")
    #
    # return [pe, company, photo]
generate_pe("SBER")