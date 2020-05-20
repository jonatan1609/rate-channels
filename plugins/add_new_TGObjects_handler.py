from pyrogram import (
    Client,
    Filters,
    Message,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


@Client.on_message(Filters.create(lambda _, m: m.text == 'Add new') | Filters.command('add'))
async def add_new_tg_objects_handler(_client: Client, message: Message):
    msg = await message.reply("Editing the buttons...", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    await message.reply("What would you want to add?", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton('Bot', 'bot')],
        [InlineKeyboardButton('Group', 'group')],
        [InlineKeyboardButton('Channel', 'channel')]
    ]))
