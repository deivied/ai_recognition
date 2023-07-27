<?php  
session_start();
$login_ad = $_SESSION['login'];
$prenom_ad = $_SESSION['prenom'];
$nom_ad = $_SESSION['nom'];
$id_ad = $_SESSION['id_emp']
?>

<?php  
if (isset($_POST['deconnect'])) {
    $_SESSION = array();
    session_destroy();
    header("Location:../index.html");
}
?>
<!DOCTYPE html>

<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../css/bootstrap.css">
    <link rel="stylesheet" href="../css/font.css">
    <link rel="stylesheet" href="../css/style.css">
    <title>Page | Admin</title>
</head>

<body>
    <style>
        body {
            background: url("../img/chef.jpg") no-repeat center center fixed;
            background-size: cover;
        }
    </style>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand text-center" href="#">
                <img src="../img/defar.png" alt="" width="40" height="40" class="d-inline-block align-text-top" style="border-radius: 25px;">
            </a>
            <a class="navbar-brand" href ="admin.php">
                <b> Face Recognition |</b> ACCUEIL | <?php echo " ".$prenom_ad." ".$nom_ad;?>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarSupportedContent">
                <form class="d-flex">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-primary" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
    <div class="container-fluid">
        <div class="row align-items-start">
           <div class="col">
                <div class="card text-center" style="width: 18rem; background-color: rgba(0, 0, 0, 0.3);">
                    <a href='#'><img src='../img/register.png' class="img-responsive" style="width:200px;height:200px;border-radius: 110px;" /></a>
                    <div class="card-body">
                        <h5 class="card-title"></h5>
                        <p class="card-text"></p> Pour l'inscription d'un nouvel employees<br>  
                        <a href="register.php" class="btn btn-primary">Inscrire</a>
                    </div>
                </div>           
            </div> 
            <div class="col">
                <div class="card text-center" style="width: 18rem; background-color: rgba(0, 0, 0, 0.3);">
                    <a href='#'><img src='../img/suppimer.jpg' class="img-responsive" style="width:200px;height:200px;border-radius: 110px" /></a>
                    <div class="card-body">
                        <h5 class="card-title"></h5>
                        <p class="card-text">Pour supprimer le compte d'un employees</p><br>  
                        <a href="del.php" class="btn btn-primary">Supprimer</a>
                    </div>
                </div>           
            </div>
            <div class="col">
                <div class="card text-center" style="width: 18rem; background-color: rgba(0, 0, 0, 0.3);">
                    <a href='#'><img src='../img/train.jpeg' class="img-responsive" style="width:200px;height:200px;border-radius: 110px" /></a>
                    <div class="card-body">
                        <h5 class="card-title"></h5>
                        <p class="card-text">Refaire l'entrainement de notre modele</p><br>
                        <a href="python-flask.php" class="btn btn-primary">Modele train</a>
                    </div>
                </div>           
            </div>
            <div class="col">
                <div class="card text-center" style="width: 18rem; background-color: rgba(0, 0, 0, 0.3);">
                    <a href='#'><img src='../img/enter.png' class="img-responsive" style="width:230px;height:230px;border-radius: 150px " /></a>
                    <div class="card-body">
                        <h5 class="card-title"></h5>
                        <p class="card-text">Se deconnecter de son compte</p><br>  
                        <form method="POST">
                            <input type="submit" name="deconnect" class="btn btn-primary" value="Se déconnecter">
                        </form>  
                    </div>
                </div>           
            </div>
        </div>
    </div>
</body>
</html>