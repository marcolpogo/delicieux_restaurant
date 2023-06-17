from persistence.db_getter import DbGetter


class UserController:
    def get_user(self, username):
        db = DbGetter.get_db()
        return db.get_user(username)
