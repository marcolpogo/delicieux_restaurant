## Challenge CTF

Challenge par marco l'pogo

## Dépendances

- Flask -> `pip install Flask`
- requests -> `pip install requests`
- RAML -> `npm i -g raml2html` // Pas nécéssaire sur le Dockerfile
- Flask-HTTPAuth -> `pip install Flask-HTTPAuth`


## Lancer le programme

Utiliser le Dockerfile
npm n'est pas installé, car on en a pas besoin. On envoie seulement le `doc.html` compilé pour laisser le conteneur léger!