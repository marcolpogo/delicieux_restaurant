class Contrevenant:
    def __init__(self, row):
        self.id_poursuite = int(row[0])
        self.business_id = int(row[1])
        self.date = row[2]
        self.description = row[3]
        self.adresse = row[4]
        self.date_jugement = row[5]
        self.etablissement = row[6]
        self.montant = row[7]
        self.proprietaire = row[8]
        self.ville = row[9]
        self.statut = row[10]
        self.date_statut = row[11]
        self.categorie = row[12]

    def as_dict(self):
        dict = {'idPoursuite': self.id_poursuite,
                'businessId': self.business_id,
                'date': self.date,
                'description': self.description,
                'adresse': self.adresse,
                'dateJugement': self.date_jugement,
                'etablissement': self.etablissement,
                'montant': self.montant,
                'proprietaire': self.proprietaire,
                'ville': self.ville,
                'statut': self.statut,
                'dateStatut': self.date_statut,
                'categorie': self.categorie}
        return dict
