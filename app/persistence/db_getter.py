from flask import g
from persistence.database import Database


class DbGetter:

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            g._database = Database()
        return g._database
