from pyrogram import (
    Client,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Filters,
    Message
)


@Client.on_message(
    Filters.text & (
            Filters.create(lambda _, m: m.text == "Open panel") | Filters.command('panel')
    )
)
async def open_panel(_client: Client, message: Message):
    await message.reply(
        "Select Option below", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('Add new')],
            [KeyboardButton('My bots / channels / groups')]
        ], resize_keyboard=True, one_time_keyboard=True)
    )
