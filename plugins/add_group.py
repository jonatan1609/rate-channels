from pyrogram import (
    Client,
    Filters,
    CallbackQuery, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
)

from .start_handler import start_handler
from .utils import add_tg, get_code
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, PeerIdInvalid


@Client.on_callback_query(Filters.callback_data('group'))
async def add_bot(_client: Client,
                  callback: CallbackQuery,
                  message="What's the username of your group?"):
    await callback.message.delete()
    username = await _client.ask(callback.message.chat.id, message) # noqa
    if str(username.text) == '/start':
        return await start_handler(_client, callback.message)
    try:
        username = str(username.text)
        if username.isdigit():
            if username.isdigit():
                return (await add_bot(
                    _client,
                    callback,
                    "Do not send an ID, only username. try again.\n"
                    "What's the username of your channel?"
                ))
        group = await _client.get_chat(username)
    except (IndexError, ValueError, KeyError,
            UsernameNotOccupied, UsernameInvalid, PeerIdInvalid) as e:
        return (await add_bot(_client, callback,
                              ("username not exist. try again.\n"
                               if not isinstance(e, IndexError) else
                               'Something went wrong, try again\n') +
                              "What's the username of your group?"
                              )
                )

    if group.type not in ('group', 'supergroup'):
        await add_bot(_client, callback,
                      "This username not belong to a group, try again.\n"
                      "What's the username of your group?")
    else:
        code = get_code()
        await _client.ask(
            callback.message.chat.id,
            "How to authorise the group:\n"
            "Go to 'manage group'\n"
            f"Then add this code: `{code}` to your group description,\n"
            f"then press 'Done'\n"
            "[Then remove this from your group description]",
            timeout=200,
            filters=Filters.regex('Done'),
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton('Done')]
            ], resize_keyboard=True)
        )
        bot = await _client.get_chat(username)
        if code in bot.description:
            await callback.message.reply('OK!', reply_markup=ReplyKeyboardRemove())
        else:
            await callback.message.reply('Code not found! try again', reply_markup=ReplyKeyboardRemove())
            return await add_bot(_client, callback)
        add = add_tg(
            group.id,
            group.title,
            callback.from_user.id,
            group.username,
            'group'
        )
        if add:
            await callback.message.reply(
                "That's the details about the group:\n"
                f"🔸Owner: {callback.from_user.first_name}"
                f"{callback.from_user.last_name or ''}"
                f" [{callback.from_user.id}]\n"
                f"🔸Group name: {add.name}\n"
                f"🔸Group id: {add.id}\n" +
                (f"🔸Group username: {add.username or ''}\n" if group.username else '') +
                f"\n\nRate link:\nt.me/TheRatesBot?start={add.id}"
            )
        else:
            await callback.message.reply("The group already exist!")
