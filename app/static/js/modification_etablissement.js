// Garde en mémoire la dernière rangée à avoir été modifiée
var lastUpdatedRow = "";
var isBeingModified = false;

function GenerateActionButton(id) {
    var btnUpdate = "<button class=\"btn btn-outline-primary btn-sm\"" +
                    "onclick=updateRow(" + id + ")>Modifier</button>";

    var btnDelete = "<button class=\"btn btn-outline-danger btn-sm\"" +
                    "onclick=deleteRow()>Supprimer</button>";

    return btnUpdate + " | " + btnDelete;
}


function GenerateUpdateActionButton(id) {
    var btnSave = "<button id=\"save-row\" class=\"btn btn-primary btn-sm\"" +
                  "onclick=saveRow(" + id + ")>Sauvegarder</button>";
                  
    var btnUndo = "<button id=\"undo-row\" class=\"btn btn-danger btn-sm\"" +
                  "onclick=undoRow()>Annuler</button>";

    return btnSave + " | " + btnUndo;
}


function deleteRow(id) {
    var currentRow = document.getElementById(id);
    alert('Seul les administrateurs peuvent supprimer un établissement!');
}


function updateRow(id) {
    if (isBeingModified) {
        undoRow(id);
    }
    isBeingModified = true;

    var currentRow = document.getElementById(id);
    lastUpdatedRow = currentRow.cloneNode(true);
    var children = currentRow.childNodes
    var currentName = children[0].innerText;
 
    var input = "<input class=\"form-control\" value=\"" + currentName + "\">";
    children[0].innerHTML = input;
    children[1].innerHTML = GenerateUpdateActionButton(id)    
}


function undoRow() {
    var id = lastUpdatedRow.id;
    var currentRow = document.getElementById(id);
    currentRow.innerHTML = lastUpdatedRow.innerHTML;
    isBeingModified = false;
}


function saveRow(id) {
    var currentRow = document.getElementById(id);
    var children = currentRow.childNodes
    var modifiedName = children[0].childNodes[0].value;
    var prevName = lastUpdatedRow.children[0].innerText;
    
    var url = "/api/modification"; 
    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({previousName: prevName, updatedName : modifiedName})
    })
        .then(response=>response.text())
        .then(data=>{ resultatRecherche.innerHTML = data;})
        .catch(err => {
            currentRow.innerHTML = lastUpdatedRow.innerHTML;
            alert("Erreur avec le serveur");
        });
    isBeingModified = false;
}