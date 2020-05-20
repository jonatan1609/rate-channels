from pyrogram import Client, CallbackQueryHandler, Filters
from pyromod import listen # noqa
from plugins.start_handler import start_handler


app = Client(
    'rateChannels',
    api_id=1,
    api_hash="b6b154c3707471f5339bd661645ed3d6",
    bot_token="",
    plugins={'root': 'plugins'}
)
app.add_handler(CallbackQueryHandler(start_handler, Filters.callback_data('home')))
app.run()
