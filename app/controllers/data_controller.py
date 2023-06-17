import sqlite3
import requests
import time
import re
import csv
from domain.contrevenant import Contrevenant
from persistence.database import Database
import traceback


class DataController:
    # Enregistre les données de la ville de Montréal dans le fichier outfile
    def fetch_data(save_file):
        url = ('https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-'
               '5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/'
               'download/violations.csv')
        # Essaie un maximum de 5 fois de faire la requête
        for i in range(1, 6):
            try:
                request = requests.get(url, allow_redirects=True)
                break
            except requests.RequestException:
                retry_request(i)
        # Écriture des données dans le fichier avec le bon encodage
        try:
            with open(save_file, 'w') as file:
                file.write(request.content.decode('utf-8'))
        except IOError:
            raise Exception("Problème lors de l'écriture des données")

    def insert_data(in_file):
        try:
            db = Database()
            with open(in_file, 'r') as file:
                csv_reader = csv.reader(file, delimiter=',', quotechar='"')
                # Valide le header mais ne l'insère pas dans la BD
                if not has_valid_header(next(csv_reader)):
                    print('Erreur: entête invalide')
                    return
                # Si une rangée n'est pas valide, on ne l'insère pas
                for row in csv_reader:
                    if is_valid_row(row):
                        format_dates_to_iso(row)
                        db.insert_contrevenant(Contrevenant(row))

        # Gestion des erreurs possibles
        except sqlite3.Error:
            traceback.print_exc()
            raise Exception("Erreur avec la base de donnée")
        except IOError:
            traceback.print_exc()
            raise Exception("Problème lors de la lecture des données")
        finally:
            db.disconnect()


# Utilisé dans les méthodes validation des données
header_reference = ['id_poursuite', 'business_id', 'date', 'description',
                    'adresse', 'date_jugement', 'etablissement', 'montant',
                    'proprietaire', 'ville', 'statut', 'date_statut',
                    'categorie']

date_index = [2, 5, 11]


def has_valid_header(header_row):
    if len(header_reference) != len(header_row):
        return False

    for i, field in enumerate(header_row):
        if field != header_reference[i]:
            return False
    return True


def is_valid_row(row):
    # Valide le nombre de champs
    if len(header_reference) != len(row):
        print('Invalid number of field:', row)
        return False

    # Valide le format des dates
    for i in date_index:
        if not is_valid_date(row[i]):
            return False

    # Valide que les deux premiers champs sont sous le format number
    if not is_valid_number(row[0]) or not is_valid_number(row[1]):
        print('Invalid number in:', row)
        return False
    return True


def is_valid_date(date):
    if re.match('^[0-9]{8}$', date) is None:
        return False
    return True


def is_valid_number(number):
    if re.match('^[0-9]+$', number) is None:
        return False
    return True


def format_dates_to_iso(row):
    for i in date_index:
        row[i] = date_to_iso(row[i])


def date_to_iso(date):
    y = date[0:4]
    m = date[4:6]
    d = date[6:8]
    iso_format = y + '-' + m + '-' + d
    return iso_format


def retry_request(nb_try):
    if nb_try == 5:
        raise Exception("Échec de la connexion. "
                        "Contactez un admin pour de l'aide")
    # On attend 2^i seconde avant de réessayer
    retry = 2**nb_try
    print('Tentative de connexion ' + str(nb_try) + '/5 échouée. '
          'Nouvelle tentative dans ' + str(retry) + ' secondes')
    time.sleep(retry)
