from pyrogram import (
    Client,
    CallbackQuery,
    Emoji,
    Filters,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from .utils import list_of_tg_objects, make_buttons_from_tg_objects, show_by


@Client.on_callback_query(Filters.create(lambda _, c: c.data.split('|')[0] == 's'))
async def show_my_tg_objects(_client: Client, callback: CallbackQuery):
    data_splitted = callback.data.split('|')
    how_to_show = None
    if len(data_splitted) == 3:
        tgo_type, how_to_show = data_splitted[1:]
    else:
        tgo_type = data_splitted[1]

    buttons = list_of_tg_objects(callback.from_user.id, tgo_type)
    if not how_to_show:
        how_to_show = await _client.ask(callback.message.chat.id,
                                        'How do you want to show them?',
                                        reply_markup=ReplyKeyboardMarkup([
                                            [KeyboardButton('By name')],
                                            [KeyboardButton('By username')]
                                        ], resize_keyboard=True))
        await how_to_show.delete()
        await how_to_show.request.delete()
        how_to_show = how_to_show.text
    if buttons:
        try:
            await callback.edit_message_text(
                f"{Emoji.DOWN_ARROW} " +
                (f"Here your " + tgo_type + 's' if tgo_type != 'all' else
                 "All of your bots / channels / groups") +
                f" {Emoji.DOWN_ARROW}",
                reply_markup=make_buttons_from_tg_objects(
                    buttons,
                    show_by[how_to_show] if len(how_to_show) > 1 else how_to_show,
                    f"{tgo_type}|{show_by[how_to_show] if len(how_to_show) > 1 else how_to_show}"
                )
            )
        except KeyError:
            await callback.edit_message_text(Emoji.FACE_WITH_ROLLING_EYES)
    else:
        await callback.edit_message_text(f'Nothing to show {Emoji.MAN_SHRUGGING}')
