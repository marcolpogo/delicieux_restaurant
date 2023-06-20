export FLASK_APP=index.py

run:
	raml2html doc.raml > templates/doc.html
	python3 -m flask run --host=0.0.0.0

database:
	rm db/contrevenants.db
	sqlite3 db/contrevenants.db < db/db.sql
	python3 populate_db.py
