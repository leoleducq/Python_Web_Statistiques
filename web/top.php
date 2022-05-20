<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="style/main.css" />
        <title>Classement</title>
    </head>

    <body>
        <!-------------------------------Insertion du menu--------------------------------------->
        <?php include("module/menu.php");?>
        
        <?php
        //Variable avec le chemin du dossier
        $nom_dossier = 'images/';
        //Ouvre le dossier
        $dossier = opendir($nom_dossier);
        //Instanciation des tableaux de chaque période
        $listeHeure = array();
        $listeJour = array();
        $listeSemaine = array();
        //-------------------Boucle permettant d'itérer sur chaque fichier du dossier---------------
        while($fichier = readdir($dossier))
        {
            if($fichier != '.' && $fichier != '..')
            {
                //Récupérer la valeur du nb max d'icao
                $exif = exif_read_data($nom_dossier.$fichier,'IFDO',true);
                foreach ($exif as $key => $section) {
                    foreach ($section as $name => $val) {
                    #Pour prendre que la ligne où le max icao est stocké
                        if($key =="IFD0"){
                            #Condition pour mettre la paire clé / valeur dans le bon dictionnaire
                            if(strpos($fichier, "heure.jpg") !== false){
                                //Ne garde que le nom de la station
                                $fichier = str_replace("_heure.jpg","",$fichier);
                                //Ajout de la paire st => val
                                $listeHeure += [$fichier => $val];
                            }
                            if(strpos($fichier, "jour.jpg") !== false){
                                //Ne garde que le nom de la station
                                $fichier = str_replace("_jour.jpg","",$fichier);
                                //Ajout de la paire st => val
                                $listeJour += [$fichier => $val];
                            }
                            if(strpos($fichier, "semaine.jpg") !== false){
                                //Ne garde que le nom de la station
                                $fichier = str_replace("_semaine.jpg","",$fichier);
                                //Ajout de la paire st => val
                                $listeSemaine += [$fichier => $val];
                            }
                        }
                    }
                }
            }
        }
        //Tri dans l'odre décroissant chaque tableau selon la valeur
        arsort($listeHeure);
        arsort($listeJour);
        arsort($listeSemaine);
        //De base, classement des 10ers
        $topheure = array_slice($listeHeure,0,10,true);
        $topjour = array_slice($listeJour,0,10,true);
        $topsemaine = array_slice($listeSemaine,0,10,true);
        //De base, variable pour les libellés = 10
        $nb_station = 10;
        ?>
        <p id="text">Classement des stations ayant capté le plus d'avions en temps réel</p>

        <div>
        <!--Méthode permettant de récupérer la valeur selectionné-->
        <form action="" method="post">
            <select name="nb_station">
                <option selected="true" value="nb">--Choisissez le nombre de stations présente dans le classement--</option>
                <?php
                //Compteur pour sélectionner le nombre de stations qu'on souhaite dans le classement
                $cpt = 0;
                //Boucle itérant sur chaque station de la listeSemaine pour la sélection
                foreach($listeSemaine as $st){
                    //Incrémentation du compteur
                    $cpt++;
                ?>
                    <option value="<?php echo $cpt; ?>"><?php echo $cpt;?></option>
                <?php       
                }
                ?>
            </select>
            <!-- Bouton permettant de transmettre la valeur selectionné-->
            <input type="submit" name="submit" value="Voir le classement">
        </form>
        <?php
            //Si le formulaire est de type submit
            if(isset($_POST['submit'])){
                //Si la valeur selectionné du formulaire n'est pas vide
                if(!empty($_POST['nb_station'])) {
                    //La variable nb_station prend cette valeur (Nombre de station présente dans le classement)
                    $nb_station = $_POST['nb_station'];
                    //Condition permettant de vérifier que l'utilisateur n'a pas pris la 1ère option
                    if($nb_station=="nb"){
                        echo 'Veuillez sélectionner un nombre';
                    }
                    //Ré instanciation du classement avec le nombre de station à mettre dedans
                    $topheure = array_slice($listeHeure,0,$nb_station,true);
                    $topjour = array_slice($listeJour,0,$nb_station,true);
                    $topsemaine = array_slice($listeSemaine,0,$nb_station,true);
                }
            }
        ?>
        </div>
    <!--ID box : regroupe les 3 classements-->
    <div id="box">
        <!--CLASS item : pour chaque classement--> 
        <div class="item">
                <h2 class="heure" id="h2heure">TOP <?php echo $nb_station?> de l'heure</h2>
            <!--Tableau / Classement par heure-->
            <table class="top" id="topheure">
                <tr class="heure">
                    <td>Place</td>
                    <td>Nom de la station</td>
                    <td>Nombre d'avions captés</td>
                </tr>
                <?php
                //------------Les afficher dans des tableaux html---------------
                $cpt = 1;
                foreach($topheure as $st => $maxicao){
                    //Pour chaque paire station / nbicao
                ?>
                    <tr>
                        <td><?php echo $cpt++; ?></td>
                        <td><?php echo $st; ?></td>
                        <td><?php echo $maxicao ?></td>
                    </tr>
                <?php
                }
                ?>
            </table>
        </div>
        
        <div class="item">
            <h2 class="jour" id="h2jour">TOP <?php echo $nb_station?> du jour</h2>
            <table class="top" id="topjour">
                <tr class="jour">
                    <td>Place</td>
                    <td>Nom de la station</td>
                    <td>Nombre d'avions captés</td>
                </tr>
                <?php
                $cpt = 1;
                foreach($topjour as $st => $maxicao){
                ?>
                    <tr>
                        <td><?php echo $cpt++; ?></td>
                        <td><?php echo $st; ?></td>
                        <td><?php echo $maxicao ?></td>
                    </tr>
                <?php
                }
                ?>
            </table>
        </div>

        <div class="item">
            <h2 class="semaine" id="h2semaine">TOP <?php echo $nb_station?> de la semaine</h2>
            <table class="top" id="topsemaine">
                <tr class="semaine">
                    <td>Place</td>
                    <td>Nom de la station</td>
                    <td>Nombre d'avions captés</td>
                </tr>
                <?php
                $cpt = 1;
                foreach($topsemaine as $st => $maxicao){
                ?>
                    <tr>
                        <td><?php echo $cpt++; ?></td>
                        <td><?php echo $st; ?></td>
                        <td><?php echo $maxicao ?></td>
                    </tr>
                <?php
                }
                ?>
            </table>
        </div>
    </div>

        <!--Appel du code javascript-->
        <!--<script src="script/top.js"></script>-->
    </body>
</html>