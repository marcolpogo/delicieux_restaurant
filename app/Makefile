export FLASK_APP=index.py

run:
	raml2html doc.raml > templates/doc.html
	flask run

debug:
	raml2html doc.raml > templates/doc.html
	FLASK_DEBUG=1 flask run

database:
	rm db/contrevenants.db
	sqlite3 db/contrevenants.db < db/db.sql
	python3 populate_db.py

clean-database:
	rm db/contrevenants.db
	sqlite3 db/contrevenants.db < db/db.sql
	
