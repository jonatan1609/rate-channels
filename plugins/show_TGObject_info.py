from pyrogram import (
    Client,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Filters
)
from .utils import get_info


@Client.on_callback_query(Filters.create(lambda _, c: c.data.split('|')[0].lstrip('-').isdigit()))
async def show_info_about_tg_object(_client: Client, callback: CallbackQuery):
    chat, came_from, show_as = callback.data.split('|')
    info = get_info(int(chat))
    await callback.edit_message_text(f"""
🔸 Name: {info.name}
🔸 Stars average: {info.stars_average}
🔸 Amount of rates: {info.rates}
    """, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Back ➡️", f"s|{came_from}|{show_as}")],
        [InlineKeyboardButton("Get rate link", f"getlink|{info.id}|{came_from}|{show_as}")]
    ]))

