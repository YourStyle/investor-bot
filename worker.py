import json
import requests
import sys
import random
from PIL import Image, ImageDraw, ImageFont

# class Symbol:
#     t = 1
#
#
# ticker_value = input()
#
# url = 'https://dev.newton-technology.ru//api/dictionary/internal/instruments/ticker/map'
#
# headers = {'content-type': 'application/json', 'charset': 'utf-8', 'connection': 'close',
#            'Authorization': 'Basic ZGljdGlvbmFyaWVzOlhFVTlwRWJPekI1MmdwOEdhVWkwYlRH'}
#
# payload = {'tickers': [f'{ticker_value}']}
# r = requests.post(url, headers=headers, data=json.dumps(payload))
# ticker = r.json()[f'{ticker_value}']
# url = f'https://dev.newton-technology.ru/api/financials/instrument/metrics'
# payload = {
#     "instrumentIds": [
#         ticker
#     ],
#     "types": [
#         "assets",
#         "ebitda"
#     ],
#     "periodType": "ann",
#     "standard": "ifrs",
#     "yearsCount": 2
# }
# request = requests.post(url, headers=headers, data=json.dumps(payload))
# text = ""
#
# for i in request.json()["310"].keys():
#     for j in range(len(request.json()["310"][i])):
#         value = request.json()["310"][i][j]["value"]
#         currency = request.json()["310"][i][j]["currency"]
#         fiscalYear = request.json()["310"][i][j]["fiscalYear"]
#         text += f"{i} по тикеру {ticker_value} за {fiscalYear} составляют {value} {currency}" + "\n"

# Список для хранения кадров.
frames = []

text = "1"
colors = ['#441C11', '#923A16', '#CC5F14', '#E4B63C']
counter = 0
c_c = 0
rotator = 0
rotator_step = 15
for frame_number in range(0, 107):
    if frame_number < 10:
        frame = Image.open(f'shield/shield 2_0000{frame_number}.png')
    elif frame_number < 100:
        frame = Image.open(f'shield/shield 2_000{frame_number}.png')
    elif frame_number < 1000:
        frame = Image.open(f'shield/shield 2_00{frame_number}.png')
    # Открываем изображение каждого кадра.
    width, height = frame.size
    center = width / 2
    idraw = ImageDraw.Draw(frame)
    font = ImageFont.truetype("arial.ttf", size=50)
    white = '#ffffff'
    if counter < 30 and c_c < 4:
        idraw.text((center - font.size // 2, 100), text, fill=colors[c_c], font=font)
        counter += 1
    elif counter == 30 and c_c < 4:
        counter = 0
        idraw.text((center - font.size // 2, 100), text, fill=colors[c_c], font=font)
        c_c += 1
    else:
        counter = 0
        c_c = 0
        idraw.text((center - font.size // 2, 100), text, fill=colors[c_c], font=font)
    # Добавляем кадр в список с кадрами.
    frames.append(frame.rotate(rotator))
    rotator+=rotator_step

# Берем первый кадр и в него добавляем оставшееся кадры.
frames[0].save(
    'shield2.gif',
    save_all=True,
    append_images=frames[1:],  # Срез который игнорирует первый кадр.
    optimize=True,
    duration=50,
    loop=0
)
