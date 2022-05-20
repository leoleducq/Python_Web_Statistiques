//Récupère la liste des nombres
const listeNombre = document.getElementById("nb_heure")

//Lorsque l'utilisateur change la valeur de la liste nombre
listeNombre.addEventListener("change",
function(){
    const nb = listeNombre.value;
    afficher()
})

function afficher(){
    nb = listeNombre.value;

    if(nb =="nb"){
        //Cache les Tableaux et les h2
        document.getElementById("topheure").hidden = true
        document.getElementById("topjour").hidden = true
        document.getElementById("topsemaine").hidden = true
        document.getElementsByName("top").hidden = true
        document.getElementById('box').getElementsByClassName('item').hidden = true

    }
    if(nb!=="nb"){
        //Affiche les Tableaux et les h2
        document.getElementById("topheure").hidden = false
        document.getElementById("topjour").hidden = false
        document.getElementById("topsemaine").hidden = false
        //Changement de valeur des h2
        document.getElementById("h2heure").innerHTML = "Top "+nb+" de l'heure";
        document.getElementById("h2jour").innerHTML = "Top "+nb+" du jour";
        document.getElementById("h2semaine").innerHTML = "Top "+nb+" de la semaine";
        //Donne les valeurs aux tableaux
        document.getElementById("topheure").innerHTML = ""
        document.getElementById("topheure").innerHTML = "<?php echo oui;?>"

    }
}