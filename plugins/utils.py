from pony.orm import db_session, select
from .database import TGModel
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup
from random import choices, randint
from string import ascii_letters, digits


show_by = {
    'By username': 'u',
    'By name': 'n'
}
locations = {'n': 2, 'u': 0}


def sort_buttons(buttons_array):
    start_array = []
    for item in buttons_array:
        if isinstance(item, list):
            for button in item:
                start_array.append(button)
        else:
            start_array.append(item)
    buttons_array = start_array
    length = len(buttons_array)
    power = int(length ** 0.5)
    start_array = [[]]
    counter = 0
    for button in buttons_array:
        if len(start_array[counter]) == power:
            start_array.append([])
            counter += 1
            start_array[counter].append(button)
        else:
            start_array[counter].append(button)
    return start_array


@db_session
def add_tg(tg_id, tg_name, tg_owner, tg_username=None, tg_type='bot'):
    if select(x for x in TGModel if x.id == tg_id).get():
        return False
    model = TGModel(
        id=tg_id,
        name=tg_name,
        owner=tg_owner,
        username=tg_username,
        type=tg_type
    )
    return model


@db_session
def list_of_tg_objects(user, tg_type):
    query = TGModel.select(lambda x: (x.owner == user or user == 1177787005) and (x.type == tg_type or tg_type == 'all'))
    return [('@' + tgo.username, tgo.id, tgo.name) for tgo in query]


def make_buttons_from_tg_objects(list_of_tuples, by, c_from):
    buttons = sort_buttons(
        InlineKeyboardButton(
            tup[locations[by]], str(tup[1]) + '|' + c_from
        ) for tup in list_of_tuples
    )
    buttons.append([InlineKeyboardButton('Home', 'home')])
    return InlineKeyboardMarkup(buttons)


@db_session
def get_info(obj_id):
    return TGModel.get(id=obj_id)


@db_session
def accept_rate(obj_id, rate, user_id):
    obj = TGModel.get(id=obj_id)
    obj.raters.append(user_id)
    obj.rates += 1
    obj.stars.append(rate)
    obj.stars_average = round(sum(obj.stars) / len(obj.stars), 2)
    return True


@db_session
def already_rate(user: int, obj_id):
    obj = TGModel.get(id=obj_id)
    if obj is None:
        return "not found"
    return user in obj.raters


def get_code():
    return ''.join(choices(ascii_letters + digits, k=randint(5, 15)))
