import sqlite3
import traceback
import hashlib
import subprocess
import uuid
import os

from flask import Flask
from flask import render_template,  request, g
from flask import jsonify
from flask_httpauth import HTTPBasicAuth

from controllers.contrevenant_controller import ContrevenantController
from controllers.user_controller import UserController
from persistence.database import Database


# Instanciation de l'app
app = Flask(__name__, static_url_path="", static_folder="static")
auth = HTTPBasicAuth()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404


@auth.verify_password
def verify_password(username, password):
    controller = UserController()
    user = controller.get_user(username)
    if user is None:
        return False

    encoded_pass = str(password + user.salt).encode("utf-8")
    hashed_pass = hashlib.sha512(encoded_pass).hexdigest()
   
    if user.password == hashed_pass:
        return True
    return False


# Documentation des services REST
@app.route('/api', methods=['GET'])
def documentation():
    return render_template('doc.html')


# Page: Accueil
@app.route('/', methods=['GET'])
def main():
    controller = ContrevenantController()
    try:
        etablissements = controller.get_etablissements()
    except(sqlite3.Error):
        traceback.print_exc()
        etablissements = ['Erreur: Etablissements non disponibles']

    return render_template('accueil.html', title='Délicieux restaurants',
                           etablissements=etablissements)



# Service REST: Toutes les infractions du restaurant demandé
@app.route('/api/infractions', methods=['GET'])
def get_contrevenants_by_etablissement():
    args = request.args
    controller = ContrevenantController()
    try:
        contrevenants = controller.get_contrevenants_by_etablissement(args)
    except(sqlite3.Error):
        traceback.print_exc()
        return '', 500

    return jsonify([(contrevenant.as_dict())
                   for contrevenant in contrevenants])


# Service REST: Établissement ayant commis des infractions
@app.route('/api/etablissements', methods=['GET'])
def get_contrevenants_by_date():
    controller = ContrevenantController()
    try:
        etablissements = controller.get_etablissements()
    except(sqlite3.Error):
        traceback.print_exc()
        return '', 500

    return jsonify([{'etablissement' : etablissement}
                   for etablissement in etablissements])


# Service REST: Met à jour l'établissement d'un contrevenant
@app.route('/api/modification', methods=['GET', 'POST'])
def update_contrevenants():
    if request.method != 'POST':
        return 'Method Not Allowed', 405

    if 'updatedName' not in request.json or 'previousName' not in request.json:
        return 'Invalid data\n', 422

    
    updated_name = request.json['updatedName']
    previous_name = request.json['previousName']

    # Validation des char à échapper (sauf ` et /)
    black_list = ["'", "\"", ";", "*", "?", "&", "|", "$", "<", ">"]
    hacker_msg = ("Tu te fou de moi? J'ai pris soin de bloquer tous les caractères dangereux ;)\n")
    for char in black_list:
        if char in updated_name or char in previous_name:
            return hacker_msg

    # Commande shell
    id = uuid.uuid4()
    file_name = 'todo_list/todo#' + str(id) + '.txt'
    str_todo = 'Remplacer ' + previous_name + ' par ' + updated_name + '\n'
    command = 'echo "' + str_todo +'" > ' + file_name
    try:
        subprocess.check_output(command, shell = True)
    except subprocess.CalledProcessError as e:
        # Renvoie l'erreur
        return "Erreur: " + command, 200

    # Lecture du contenu du fichier
    try:
        content = read_file(file_name)
    except:
        delete_file(file_name)
        return 'Il y a eu une erreur lors de votre requête. Veuillez réessayer.\n'

    # On supprime le fichier pour éviter que ça s'accumule
    delete_file(file_name)
    return render_template('modification.html', content=content), 200


# Route pour obtenir le flag. Protégée par Auth
@app.route('/api/flag', methods=['GET'])
@auth.login_required
def get_flag():
    flag = get_db().get_flag()
    uq = 'UQ'
    am = 'AM'
    return uq + am + flag, 200


def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


def delete_file(file_name):
    try:
        os.remove(file_name)
    except:
        print("Couldn't remove", file_name)