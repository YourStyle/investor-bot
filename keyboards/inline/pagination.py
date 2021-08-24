from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.config import mult_commands
pagination_call = CallbackData("paginator", "key", "command")


def get_command_keyboard(max_commands: int, key="commands", command: int = 1):
    previous_command = command - 1
    previous_command_text = "<<"

    current_command_text = f"{mult_commands[command]}"

    next_command = command + 1
    next_command_text = ">>"

    markup = InlineKeyboardMarkup()
    if previous_command >= 0:
        markup.insert(
            InlineKeyboardButton(
                text=previous_command_text,
                callback_data=pagination_call.new(key=key, command=previous_command)
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text=current_command_text,
            callback_data=pagination_call.new(key=key, command=mult_commands[command])
        )
    )
    if next_command < max_commands:
        markup.insert(
            InlineKeyboardButton(
                text=next_command_text,
                callback_data=pagination_call.new(key=key, command=next_command)
            )
        )

    return markup
