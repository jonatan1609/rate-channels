from pony.orm import Database, Required, Optional, PrimaryKey, IntArray
from os.path import exists

db = Database()


class TGModel(db.Entity):
    id = PrimaryKey(int, auto=True, min=-10000000000000, size=64)
    type = Required(str)
    stars = Required(IntArray, default=[])
    stars_average = Required(float, default=0)
    rates = Required(int, default=0)
    username = Optional(str)
    name = Required(str)
    owner = Required(int)
    raters = Required(IntArray, default=[])


if exists('../database.sql'):
    db.bind(provider='sqlite', filename='../database.sql')
else:
    db.bind(provider='sqlite', filename='../database.sql', create_db=True)
db.generate_mapping(create_tables=True)
