import asyncio
import re

import aiogram
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from company import Company
from data.config import mult_commands, max_commands_commands
from keyboards.inline.pagination import get_command_keyboard, pagination_call
from loader import dp
from utils.misc.commands import get_command


@dp.message_handler(Command("mult"))
async def show_commands(message: types.Message):
    chat_id = message.chat.id
    if message.text == "/mult":
        await message.answer(
            "Эта команда возвращает основную информацию о компании, введённой после команды /mult.\nПример: /mult SBER"
        )
        return
    ticker_or_company = message.text.split()[1]
    if re.findall('[A-Z]{2,6}', ticker_or_company):
        company = Company(ticker_or_company, "mult", True)
        resp = company.check_response()
        text = f"Основная информация о компании {company.name} за {company.fYear}.\n" \
               f"Чтобы узнать другие параметры компании используйте кнопки ниже "
    else:
        company = Company(ticker_or_company, "mult", False)
        resp = company.check_response()
        text = f"Основная информация о компании {company.name} за {company.fYear}.\n" \
               f"Чтобы узнать другие параметры компании используйте кнопки ниже "
    if type(resp) == aiogram.types.input_file.InputFile:
        await dp.bot.send_chat_action(chat_id=chat_id, action=aiogram.types.chat.ChatActions.UPLOAD_PHOTO)
        await message.answer_animation(animation=resp, caption=text,
                                       reply_markup=get_command_keyboard(max_commands=max_commands_commands))
    else:
        await dp.bot.send_chat_action(chat_id=chat_id, action=aiogram.types.chat.ChatActions.TYPING)
        await message.answer(text=f"{resp}")


@dp.callback_query_handler(pagination_call.filter(command="pe"))
@dp.callback_query_handler(pagination_call.filter(command="cap"))
@dp.callback_query_handler(pagination_call.filter(command="cash"))
@dp.callback_query_handler(pagination_call.filter(command="debt"))
@dp.callback_query_handler(pagination_call.filter(command="sales"))
@dp.callback_query_handler(pagination_call.filter(command="fcf"))
@dp.callback_query_handler(pagination_call.filter(command="ebitda"))
@dp.callback_query_handler(pagination_call.filter(command="ps"))
@dp.callback_query_handler(pagination_call.filter(command="pb"))
@dp.callback_query_handler(pagination_call.filter(command="eve"))
@dp.callback_query_handler(pagination_call.filter(command="nde"))
@dp.callback_query_handler(pagination_call.filter(command="dividend"))
@dp.callback_query_handler(pagination_call.filter(command="earnin"))
@dp.callback_query_handler(pagination_call.filter(command="roa"))
@dp.callback_query_handler(pagination_call.filter(command="ros"))
async def mult_command_ex(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    call.message.edit_text
    if callback_data.get("command") == "pe":
        pass


@dp.callback_query_handler(pagination_call.filter(key="commands"))
async def show_chosen_command(call: CallbackQuery, callback_data: dict):
    current_command = int(callback_data.get("command"))
    text = get_command(mult_commands, command=current_command)
    markup = get_command_keyboard(max_commands=max_commands_commands, command=current_command)
    await call.message.edit_reply_markup(reply_markup=markup)
