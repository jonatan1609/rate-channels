from pyrogram import (
    Client,
    Filters,
    Message,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


@Client.on_message(Filters.create(lambda _, m: m.text == 'My bots / channels / groups') | Filters.command('my'))
async def my_tg_objects_handler(_client: Client, message: Message):
    msg = await message.reply("Editing the buttons...", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await message.reply("What do you want to see?",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton('Bots', 's|bot')],
                            [InlineKeyboardButton('Channels', 's|channel')],
                            [InlineKeyboardButton('Groups', 's|group')],
                            [InlineKeyboardButton('All', 's|all')]
                        ])
                        )
