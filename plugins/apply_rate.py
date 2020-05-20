from pyrogram import (
    Client,
    CallbackQuery,
    Filters,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from .utils import accept_rate, get_info


@Client.on_callback_query(Filters.create(lambda _, c: c.data.startswith('rate')))
async def rate(_client: Client, callback: CallbackQuery):
    _, amount, tgo_id = callback.data.split('|')
    accept_rate(int(tgo_id), int(amount), callback.from_user.id)
    info = get_info(tgo_id)
    await callback.edit_message_text(
        f"Success!\n🌟Rates average: {info.stars_average} / 5"
    )
    review = await _client.ask(
        callback.message.chat.id,
        "Want to write a review?",
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('Yes'), KeyboardButton('No')]
        ], resize_keyboard=True, one_time_keyboard=True)
    )
    await review.delete()
    await review.request.delete()
    if str(review.text) == 'No':
        return await callback.message.reply("Thanks!", reply_markup=ReplyKeyboardRemove())
    elif str(review.text) == 'Yes':
        review = await _client.ask(
            callback.message.chat.id,
            "Write your review:",
            reply_markup=ReplyKeyboardRemove()
        )
        await review.request.delete()
        await review.delete()
        await callback.message.reply("Thanks!")
        return await _client.send_message(
            info.owner, "Review from"
                        f" [{callback.from_user.first_name}]"
                        f"(tg://user?id={callback.from_user.id})\n\n"
                        f"{str(review.text)}"
        )
    else:
        return await callback.message.reply("Stop zaccing me!")