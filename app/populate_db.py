import os
import sys
from controllers.data_controller import DataController

# On utilise un fichier intermédiaire travailer avec csv.reader()
file_name = 'data.csv'

try:
    # Insère les données de la ville de Montréal dans le fichier
    DataController.fetch_data(file_name)
except Exception as e:
    sys.exit(str(e))

try:
    # Utilise les données de la ville de Montréal pour populer la DB
    DataController.insert_data(file_name)
except Exception as e:
    sys.exit(str(e))

# Supprime le fichier une fois terminé
os.remove(file_name)
