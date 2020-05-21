from pyrogram import (
    Client,
    Filters,
    CallbackQuery,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from .utils import add_tg, get_code
from .start_handler import start_handler
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, PeerIdInvalid


@Client.on_callback_query(Filters.callback_data('bot'))
async def add_bot(_client: Client, callback: CallbackQuery, message="What's the username of your bot?"):
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
        bot = await _client.get_users(username)
    except (IndexError, ValueError, KeyError,
            UsernameNotOccupied, UsernameInvalid, PeerIdInvalid) as e:
        return (await add_bot(_client, callback,
                              ("username not exist. try again.\n"
                               if not isinstance(e, IndexError) else
                               'Something went wrong, try again\n') +
                              "What's the username of your bot?"
                              )
                )

    if not bot.is_bot:
        await add_bot(_client, callback,
                      "This username not belong to a bot, try again.\n"
                      "What's the username of your bot?")
    else:
        code = get_code()
        await _client.ask(
            callback.message.chat.id,
            "How to authorise the bot:\n"
            "Go to BotFather, then browse to your bot,\n"
            "then 'Edit bot' -> 'Edit About'\n"
            f"And add this code: `{code}` then press 'Done'\n"
            "[Then remove this from your bot description]",
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
            bot.id,
            bot.first_name + (bot.last_name or ''),
            callback.from_user.id,
            bot.username,
            'bot'
        )
        if add:
            await callback.message.reply(
                "That's the details about the bot:\n"
                f"🔸Owner: {callback.from_user.first_name}"
                f"{callback.from_user.last_name or ''}"
                f" [{callback.from_user.id}]\n"
                f"🔸Bot name: {add.name}\n"
                f"🔸Bot id: {add.id}\n"
                f"🔸Bot username: {add.username}\n\n\n"
                f"Rate link:\nt.me/TheRatesBot?start={add.id}"
            )
        else:
            await callback.message.reply("The bot already exist!")
