import json
import logging
import types

import aiofiles
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile

import keyboards
from keyboards.inline.callback_datas import navigate
from loader import dp, bot


