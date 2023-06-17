from persistence.db_getter import DbGetter


class ContrevenantController:
    def __init__(self):
        pass
   
    def get_etablissements(self):
        db = DbGetter.get_db()
        return db.get_all_etablissement()

    def get_contrevenants_by_etablissement(self, args):
        etablissement = args.get('etablissement')
        if etablissement is None or etablissement == '':
            return []

        db = DbGetter.get_db()
        return db.get_contrevenants_by_etablissement(etablissement)

    def get_infractions_by_etablissement():
        db = DbGetter.get_db()
        return db.get_nb_infraction_by_etablissement()
