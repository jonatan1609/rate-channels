from pyrogram import (
    Client,
    Filters,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from .utils import already_rate


@Client.on_message(Filters.command('start') & Filters.create(lambda _, m: len(m.command) > 1))
async def rate_handler(_client: Client, message: Message):
    bot_id = int(message.command[1])
    rate = already_rate(message.from_user.id, bot_id)
    if rate is True:
        return await message.reply("You can't rate the same bot twice!")
    if rate == 'not found':
        return await message.reply("Link not found!")
    await message.reply(
        "Please choose rating",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(star, f"rate|{amount}|{bot_id}")]
            for amount, star in enumerate((" ⭐ " * i for i in range(1, 6)), 1)
        ])
    )
