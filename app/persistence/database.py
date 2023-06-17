# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
from domain.contrevenant import Contrevenant
from domain.user import User


# Cette classe fait les requêtes spécifiques à la base de donnée
class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/contrevenants.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # CONTREVENANTS

    def get_all_etablissement(self):
        cursor = self.get_connection().cursor()
        query = ('select distinct etablissement from contrevenants '
                 'order by etablissement asc')

        etablissements = cursor.execute(query).fetchall()
        cursor.close()
        return [etablissement[0] for etablissement in etablissements]


    def get_contrevenants_by_etablissement(self, etablissement=None):
        # Si les paramètres, ne sont pas définis, remplacer par '%%'
        etablissement = '%' + (etablissement if etablissement else '') + '%'
       
        cursor = self.get_connection().cursor()
        query = ('select * from contrevenants where etablissement like ?')
        cursor.execute(query, (etablissement, ))
        contrevenants = cursor.fetchall()
        cursor.close()
        return [Contrevenant(contrevenant[1:])
                for contrevenant in contrevenants]

   

    def insert_contrevenant(self, cont):
        conn = self.get_connection()
        query = ('insert into contrevenants(id_poursuite, business_id, date, '
                 'description, adresse, date_jugement, etablissement, '
                 'montant, proprietaire, ville, statut, date_statut, '
                 'categorie) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
        conn.execute(query, (cont.id_poursuite, cont.business_id, cont.date,
                             cont.description, cont.adresse,
                             cont.date_jugement, cont.etablissement,
                             cont.montant, cont.proprietaire,
                             cont.ville, cont.statut, cont.date_statut,
                             cont.categorie))
        conn.commit()


    # USER

    def get_user(self, username):
        cursor = self.get_connection().cursor()
        query = 'select * from user where username = ?'
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if not user:
            return None
        return User(user[0], user[1], user[2])


    # FLAG

    def get_flag(self):
        cursor = self.get_connection().cursor()
        cursor.execute('select * from flag')
        flag = cursor.fetchone()
        cursor.close()

        return flag[1]
