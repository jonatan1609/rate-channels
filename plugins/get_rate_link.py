from pyrogram import (
    Client,
    CallbackQuery,
    Filters,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


@Client.on_callback_query(Filters.create(lambda _, c: c.data.startswith('getlink')))
async def get_link(_client: Client, callback: CallbackQuery):
    _, chat, came_from, show_as = callback.data.split('|')
    await callback.edit_message_text(
        f"Rate link:\nt.me/TheRatesBot?start={callback.data.split('|')[1]}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('Back ➡️', f'{chat}|{came_from}|{show_as}')]
        ])
    )
