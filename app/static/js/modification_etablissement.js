// Garde en mémoire la dernière rangée à avoir été modifiée
var lastUpdatedRow = "";
var isBeingModified = false;

function GenerateActionButton(idPoursuite) {
    var btnUpdate = "<button class=\"btn btn-outline-primary btn-sm\"" +
                    "onclick=updateRow(" + idPoursuite + ")>Modifier</button>";

    var btnDelete = "<button class=\"btn btn-outline-danger btn-sm\"" +
                    "onclick=deleteRow()>Supprimer</button>";

    return btnUpdate + " | " + btnDelete;
}


function GenerateUpdateActionButton(idPoursuite) {
    var btnSave = "<button id=\"save-row\" class=\"btn btn-primary btn-sm\"" +
                  "onclick=saveRow(" + idPoursuite + ")>Sauvegarder</button>";
                  
    var btnUndo = "<button id=\"undo-row\" class=\"btn btn-danger btn-sm\"" +
                  "onclick=undoRow()>Annuler</button>";

    return btnSave + " | " + btnUndo;
}


function deleteRow(idPoursuite) {
    var currentRow = document.getElementById(idPoursuite);
    alert('Seul les administrateurs peuvent supprimer un établissement!');
}


function updateRow(idPoursuite) {
    if (isBeingModified) {
        undoRow(idPoursuite);
    }
    isBeingModified = true;
    // Sauvegarde l'état actuel de la rangée
    var currentRow = document.getElementById(idPoursuite);
    lastUpdatedRow = currentRow.cloneNode(true);

    var children = currentRow.childNodes
    var currentName = children[0].innerText;
    // Remplace le nom par un champ input
    var input = "<input class=\"form-control\" value=\"" + currentName + "\">";
    children[0].innerHTML = input;
    // Remplace les boutons d'actions par les boutons sauvegarder et annuler
    children[1].innerHTML = GenerateUpdateActionButton(idPoursuite)    
}


function undoRow() {
    idPoursuite = lastUpdatedRow.id;
    var currentRow = document.getElementById(idPoursuite);
    currentRow.innerHTML = lastUpdatedRow.innerHTML;
    isBeingModified = false;
}


function saveRow(idPoursuite) {
    var currentRow = document.getElementById(idPoursuite);
    var children = currentRow.childNodes
    var modifiedName = children[0].childNodes[0].value;

    // Requete AJAX
    let url = "/api/modification"; 
    let prevName = lastUpdatedRow.children[0].innerText;
    
    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({previousName: prevName, updatedName : modifiedName})
    })
        .then(response=>response.text())
        .then(data=>{ resultatRecherche.innerHTML = 
            "<h4>Modification enregistrée</h4>" +
            "<p>L'administrateur lira votre demande lorsqu'il reviendra de vacance!</p>" +
            "<p><b>Ajout au fichier todo_list.txt:</b></br>" + data + "</p>";
        })
        
        .catch(err => {
            currentRow.innerHTML = lastUpdatedRow.innerHTML;
            alert("Erreur avec le serveur");
        });
    isBeingModified = false;
}