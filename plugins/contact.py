from pyrogram import (
    Client,
    Filters,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from .start_handler import start_handler


@Client.on_message(Filters.text & (
    Filters.create(lambda _, m: m.text == "Contact me") | Filters.command('contact')
))
async def contact(_client: Client, message: Message):
    msg = await _client.ask(
        message.chat.id,
        "Write a messages and then press 'Done'.",
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('Done')]
        ], resize_keyboard=True)
    )
    if str(msg.text) != "Done":
        await _client.send_message(
            'Oxcafe1c2a',
            "[{}](tg://user?id={}) said: \n\n\n{}".format(message.from_user.first_name,
                                                          message.from_user.id,
                                                          str(msg.text))
        )
        await contact(_client, message)
    else:
        await msg.delete()
        await message.reply("The messages was sent successfully!")
        await start_handler(_client, message)
