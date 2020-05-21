from pyrogram import (
    Client,
    Filters,
    CallbackQuery,
    ReplyKeyboardRemove,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from .start_handler import start_handler
from .utils import add_tg, get_code
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, PeerIdInvalid


@Client.on_callback_query(Filters.callback_data('channel'))
async def add_channel(_client: Client,
                      callback: CallbackQuery,
                      message="What's the username of your channel?"):
    await callback.message.delete()
    username = await _client.ask(callback.message.chat.id, message) # noqa
    if str(username.text) == '/start':
        return await start_handler(_client, callback.message)
    try:
        username = str(username.text)
        if username.isdigit():
            return (await add_channel(
                _client,
                callback,
                "Do not send an ID, only username. try again.\n"
                "What's the username of your channel?"
            ))
        group = await _client.get_chat(username)
    except (IndexError, ValueError, KeyError,
            UsernameNotOccupied, UsernameInvalid, PeerIdInvalid) as e:

        return (await add_channel(_client, callback,
                                  ("username not exist. try again.\n"
                                   if not isinstance(e, IndexError) else
                                   'Something went wrong, try again\n') +
                                  "What's the username of your channel?"
                                  )
                )

    if group.type != 'channel':
        await add_channel(_client, callback,
                          "This username not belong to a channel, try again.\n"
                          "What's the username of your channel?")
    else:
        code = get_code()
        await _client.ask(
            callback.message.chat.id,
            "How to authorise the channel:\n"
            "Go to 'manage channel'\n"    
            f"Then add this code: `{code}` to channel description, then press 'Done'\n"
            "[Then remove this from your channel description]",
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
            return await add_channel(_client, callback)
        add = add_tg(
            group.id,
            group.title,
            callback.from_user.id,
            group.username,
            'channel'
        )
        if add:
            await callback.message.reply(
                "That's the details about the channel:\n"
                f"🔸Owner: {callback.from_user.first_name}"
                f"{callback.from_user.last_name or ''}"
                f" [{callback.from_user.id}]\n"
                f"🔸channel name: {add.name}\n"
                f"🔸channel id: {add.id}\n" +
                (f"🔸channel username: {add.username or ''}\n" if group.username else '') +
                f"\n\nRate link:\nt.me/TheRatesBot?start={add.id}"
            )
        else:
            await callback.message.reply("The channel already exist!")
