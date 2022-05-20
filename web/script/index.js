//Récupère la liste déroulante st
const listeStation = document.getElementById("st")

//Lorsque l'utilisateur change la valeur de la liste Station
listeStation.addEventListener("change",
function(){
    const st = listeStation.value;
    afficher()
})

function afficher(){
    st = listeStation.value;

    //Données disponibles pour telle station
    document.getElementById("datast").innerHTML = "Données de la station : "+st.toUpperCase()
    //Cache tous les headers
    document.getElementById("headheure").hidden = true
    document.getElementById("headjour").hidden = true
    document.getElementById("headsemaine").hidden = true
    document.getElementById("msgerror").hidden = true
    document.getElementById("datast").hidden = false
    if(st !="station"){
        tout(st)
    }
    if(st=="station"){
        //Cache le libellé "Données disponible pour telle station"
        document.getElementById("datast").hidden = true
        //Affiche le msg d'erreur
        document.getElementById("msgerror").hidden = false
        document.getElementById("msgerror").innerText ="Veuillez sélectionner une station"
    }
};

//Fonction pour tout afficher
function tout(st){
    //Affichage de tous les headers
    document.getElementById("headheure").hidden = false
    document.getElementById("headjour").hidden = false
    document.getElementById("headsemaine").hidden = false
    //Remplissage des h2
    document.getElementById("h2heure").innerHTML = "Par heure"
    document.getElementById("h2jour").innerHTML = "Par jour"
    document.getElementById("h2semaine").innerHTML = "Par semaine"
    //Insertion de toutes les images
    document.getElementById("heure").src = 'images/'+st+'_heure.jpg';
    document.getElementById("jour").src = 'images/'+st+'_jour.jpg';
    document.getElementById("semaine").src = 'images/'+st+'_semaine.jpg';
    //Changement du alt
    document.getElementById("heure").alt ="Pas de données disponible pour cet intervalle de temps"
    document.getElementById("jour").alt ="Pas de données disponible pour cet intervalle de temps"
    document.getElementById("semaine").alt ="Pas de données disponible pour cet intervalle de temps"

    //CSS
    document.getElementById("headheure").style.display = "inline_block";
    document.getElementById("headjour").style.display = "inline_block";
    document.getElementById("headsemaine").style.display = "inline_block";
}