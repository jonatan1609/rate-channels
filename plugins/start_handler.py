from pyrogram import (
    Client,
    Filters,
    ReplyKeyboardMarkup,
    KeyboardButton
)


@Client.on_message(Filters.private & (Filters.create(lambda _, m: m.text == '/start')))
async def start_handler(_client: Client, message):
    if hasattr(message, 'reply'):
        callback = message.reply
    else:
        await message.message.delete()
        callback = message.message.reply
    await callback(f"""
    Hi {message.from_user.first_name}, 
Welcome.

What can i do?
🔸Rate channels / bots / groups.
🔸Send Review for channels / bots / groups.
🔸Contact the admins of channel / bots / group / etc..

Want to support me?
[Donate here](paypal.me/pybots)
    """, reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('Open panel')],
        [KeyboardButton('Contact me')]
    ], resize_keyboard=True, one_time_keyboard=True))
