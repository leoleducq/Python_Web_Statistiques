<!DOCTYPE html>
<html>
<?php
//Variable avec le chemin du dossier
$nom_dossier = 'images/';
//Ouvre le dossier
$dossier = opendir($nom_dossier);
//Instanciation de la liste des stations
$listeStation = array();
//Compteur pour savoir le nombre de stations ayant reçus des messages
$cpt = 0;
//Boucle permettant d'itérer sur chaque fichier du dossier
while($fichier = readdir($dossier))
{
    //Variable de recherche
    $search_png = array(".jpg","_heure","_jour","_semaine");
    //Variable de remplacement
    $replace_png = array("","","","");
    //Remplacement des caractères
    $fichier = str_replace($search_png,$replace_png,$fichier);
    //Condition permettant d'ignorer les 2ères occurences, et d'ajouter la station à la liste si elle n'est pas déjà présente
    if($fichier != '.' && $fichier != '..'  && !(in_array($fichier,$listeStation)))
    {
        //Ajoute la station à la liste des stations
        array_push($listeStation, $fichier);
        //Incrémentation du compteur
        $cpt++;
    }
}
//Tri par ordre alphabétique le tableau
sort($listeStation)
?>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="style/main.css" />
        <title>ADS B STATS</title>
    </head>

    <body>
        <!-------------------------Insertion du menu---------------------------------------------->
        <?php include("module/menu.php");?>
        <!--<h1>Nombre d'ICAO capté par station</h1>-->
        <!--------------------------------------Liste--------------------------------------------->
        <p id="text">Ce site répertorie le nombre <b>d'avions</b> que chaque <b>station</b> a capté.<br>
            Chaque station à des statistiques par <b>heure</b>,par <b>jour</b> et par <b>semaine</b>.<br>
            Les données sont sur des <b>périodes glissantes</b> et sont en <b>temps réel</b>, actualisé toutes les <b>15 minutes</b>.
        </p>
        <p>Les données de <b><?php echo $cpt; ?></b> stations sont disponibles</p>
        <div id="select">
        <select id="st">
            <option selected="true" value="station">-- Sélectionnez une station --</option>
            <?php
            //Parcourir le tableau des stations
            //Nouveau compteur pour mettre le numéro de la station
            $cpt = 0;
            foreach($listeStation as $value){
                //Incrémentation du compteur
                $cpt++;
            ?>
                <option value="<?php echo strtolower($value); ?>"><?php echo $cpt.".".strtoupper($value);?></option>
            <?php
            }
            ?>
        </select>
        </div>

        <div id="datast"> </div>
        
        <!---------------------------------------Affichage des images--------------------------------->
        <div id="msgerror">Veuillez sélectionner une station</div>
        <div id="box">
            <header class="item" id="headheure">
                <h2 class="heure" id="h2heure">ADS</h2>
                    <img src="" border="0" alt="" id="heure"/>
                
            </header>
            <header class="item" id="headjour">
                <h2 class ="jour" id="h2jour">B</h2>
                    <img src="" border="0" alt="" id="jour"/>
                
            </header>
            <header class="item" id="headsemaine">
                <h2 class="semaine" id="h2semaine">STATS</h2>
                    <img src="" border="0" alt="" id="semaine"/>
            </header>
        </div>

        <!--Appel du code javascript-->
        <script src="script/index.js"></script>
    </body>
</html>