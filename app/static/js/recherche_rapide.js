// Initialise les listener et l'endroit où affciher les résultats
var resultatRecherche = document.getElementById("resultat-recherche");

setUpClickListener("recherche-rapide-date", getEtablissements);
setUpClickListener("recherche-rapide-etablissement", getInfractions);


function setUpClickListener(id, func) {
    var element = document.getElementById(id);
    if (element) {
        element.addEventListener("click", func);
    }
}


function getEtablissements() {
    let url = "/api/etablissements"
    fetch(url)
        .then(function(response) {
            if (!response.ok) {
                errorMsg("Erreur: Requête invalide")
                return null;
            } else {
                return response.json(); 
            }
        })
        .then(function (json) {
            if (json) {
                formatResponseEtablissements(json);
            }
        })
        .catch(err => {
            errorMsg("Erreur avec le serveur");
        });
}


function getInfractions() {
    let etablissement = document.getElementById("etablissement").value;
    // URL encode le nom d'établissement etablissement
    encoded_etablissement = encodeURIComponent(etablissement);
    let url = "/api/infractions?etablissement=" + encoded_etablissement;
    
    fetch(url)
        .then(function(response) {
            if (!response.ok) {
                errorMsg("Erreur: Requête invalide")
                return null;
            } else {
                return response.json(); 
            }
        })
        .then(function (json) {
            if (json) {
                formatResponseInfractions(json);
            }
        })
        .catch(err => {
            errorMsg("Erreur avec le serveur");
        });
}


function formatResponseInfractions(response) {
    // Description de la table
    var description = "<p>Contraventions pour un établissement</p>";

    // En tête avec les toutes les colonnes
    var header = "<thead>" + "<tr><th>ID de poursuite</th><th>ID de compagnie</th>" +
        "<th>Date</th><th>Description</th><th>Adresse</th><th>Date de jugement</th>" +
        "<th>Etablissement</th><th>Montant</th><th>Propriétaire</th><th>Ville</th>" +
        "<th>Statut</th><th>Date du statut</th><th>Catégorie</th></tr></thead>";

    // Corps de la table à partir de la réponse
    body = "<tbody>";
    for (var i =0; i < response.length; i++) {
        body += formatInfraction(response[i]);
    }
    body += "</tbody>";

    var table = "<table class=\"table table-sm table-responsive\">" + 
                header + body + "</table>";
        
    resultatRecherche.innerHTML = description + table;
}


function formatInfraction(contrevenant) {
    var row = "<tr>" +
        "<td>" + contrevenant.idPoursuite + "</td>" +
        "<td>" + contrevenant.businessId + "</td>" +
        "<td>" + contrevenant.date + "</td>" + 
        "<td>" + contrevenant.description + "</td>" + 
        "<td>" + contrevenant.adresse + "</td>" + 
        "<td>" + contrevenant.dateJugement + "</td>" + 
        "<td>" + contrevenant.etablissement + "</td>" + 
        "<td>" + contrevenant.montant + "</td>" + 
        "<td>" + contrevenant.proprietaire + "</td>" + 
        "<td>" + contrevenant.ville + "</td>" + 
        "<td>" + contrevenant.statut + "</td>" + 
        "<td>" + contrevenant.dateStatut + "</td>" + 
        "<td>" + contrevenant.categorie + "</td>" +
        "</tr>";
    return row;
}


function formatResponseEtablissements(etablissements) {
    // Description de la table
    var description = "<p>Établissements ayant reçus une ou plusieurs contraventions.</p>";

    // Crée le header et le body de la table
    var header = "<tr><th>Établissement</th><th>Action</th></tr>";
    var body = "";
    for (var i = 0; i < etablissements.length; i++) { 
        value = etablissements[i].etablissement
        body += "<tr id=\""+ i +"\"><td>" + value + "</td>" +
                "<td>" + GenerateActionButton(i) + "</td></tr>" ;
        }

    // Assemble la table
    var table = "<table class=\"table\">" + header + body + "</table>";

    resultatRecherche.innerHTML = description + table;
}


function errorMsg(msg) {
    var p = "<p class=\"error\">" + msg + "</p>"
    resultatRecherche.innerHTML = p;
}
