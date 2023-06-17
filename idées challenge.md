# Challenge

## Nom : Restaurants near you!

Le XSS qui semble possible lors de la modification d'un nom de client pourrait être une fausse piste. Il apparait seulement dans l'interface client, mais il est sanitized et n'entre pas dans la DB.

- On ne devrait pas laisser l'option de supprimer un client

- Ça pourrait simplement être de de voir qu'il y a une route /api et que la doc nous donne des infos sur le flag

- Il pourrait y avoir une route /api/flag mais qui est sécurisée par Authentification

- Modifier client = une notification a été envoyée à un admin. Les modifications seront appliquées dans les 100 prochains jours ouvrables. (envoie le payload à la route /api/modifications)

- Vuln : system('echo' + modification + '> modifications.txt ') Ce n'est pas du XSS

- Il faudrait retourner quelque chose d'utile au client pour qu'il voit qu'elle est la modification qui a été envoyée (et qu'il puisse comprendre quand il réussi à trouver la faille)

- À la racine du serveur on fichier qui s'appelle 'credentials' qui permet de trouver les credentials pour accéder à la route /api/flag. Cette route retourne le flag qui est storé dans la DB

- Doc pour les services API à la route /api

## À faire

Il faudrait mieux controller ce que le client peut voir avec son RCE. Par exemple, j'aimerais qu'il puisse seulement voir le fichier login_credentials.txt 

Peut-être que l'exploit pourrait être un peu plus intéressant...