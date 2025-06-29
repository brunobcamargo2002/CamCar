!doctype html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="css/bootstrap.min.css"/>
    <script src="js/bootstrap.bundle.min.js"></script>
    <script src="js/jquery-3.6.0.min.js"></script>
  </head>
  <body style="background-color:#202125;">
    <div class="container" style="padding-top:30px;">
      <div class="d-flex justify-content-center">
        <h1 style="color:#FEFFFF;">ESP32-CAM Captured Photo Gallery</h1>
      </div>
      <hr class="mt-2 mb-5" style="height:2px;background-color:#FFFFFF";>

      <?php
        // Image extensions.
        $image_extensions = array("png","jpg","jpeg","gif");

        // Check delete HTTP GET request - remove images.
        if(isset($_GET["delete"])){
          $imageFileType = strtolower(pathinfo($_GET["delete"],PATHINFO_EXTENSION));
          if (file_exists($_GET["delete"]) && ($imageFileType == "jpg" ||  $imageFileType == "png" ||  $imageFileType == "jpeg") ) {
            unlink($_GET["delete"]);
            echo "<script>
            $(document).ready(function(){
            $('#myModalOK').modal('show');
            });

            </script>";
          }
        }
      ?>
      
      <div class="row text-center text-lg-start">
        <?php
          // Target directory.
          $dir = 'captured_images/';
          if (is_dir($dir)){
            $count = 1;
            $files = scandir($dir);
            rsort($files);
            foreach ($files as $file) {
              if ($file != '.' && $file != '..') {
        ?>
        <div class="col-lg-3 col-md-4 col-6" style="padding-bottom:30px;">
          <div class="row">
            <a href="<?php echo $dir . $file; ?>" class="d-block mb-4 h-100" target="_blank">
            <img class="img-fluid img-thumbnail" src="<?php echo $dir . $file; ?>" alt="">
            </a>
          </div>
          <div class="row justify-content-end">
            <center>
            <div class="col md-8">
            <p style="color:#FEFFFF;"><?php echo $file; ?></p>
            </div>
            <div class="col md-4">
            <a href="loadPhotos.php?delete=<?php echo $dir . $file; ?>" class="btn btn-danger btn-sm">Delete</a>
            </div> 
            </center>
          </div>
        </div>
        <?php
                $count++;
              }
            }
            if($count==1) { echo "<p style='color:#FEFFFF;'>No images found</p>"; } 
          }
        ?>
      </div>

      <!-- Modal Delete OK-->
      <div class="modal fade" id="myModalOK" tabindex="-1" aria-labelledby="myModalOKLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header" style="background-color:#2cc791;">
              <h5 class="modal-title" id="exampleModalLabel" style="color:white;">Success</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Successfully delete image file <b><?php $path_parts = pathinfo($_GET["delete"],PATHINFO_BASENAME) ; echo $path_parts; ?> </b>
            </div>
            <div class="modal-footer">
              <a class="btn btn-primary" href="index.php" role="button">OK</a>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Delete Not OK-->
      <div class="modal fade" id="myModalOK" tabindex="-1" aria-labelledby="myModalOKLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header" style="background-color:#fc8403;">
              <h5 class="modal-title" id="exampleModalLabel" style="color:white;">Success</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Something wrong while deleting file <?php $path_parts = pathinfo($_GET["delete"],PATHINFO_BASENAME) ; echo $path_parts; ?>
            </div>
            <div class="modal-footer">
              <a class="btn btn-secondary" href="index.php" role="button">OK</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
//<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


//>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> index.php
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ESP32-CAM Captured Photo Gallery</title>
  </head>
  <body style="background-color:#202125;" id="myESP32CAMPhotos">
    <script>
    var totalphotos = 0;
    var last_totalphotos = 0;
    
    loadPhotos();
    
    var timer_1 = setInterval(myTimer_1, 2000);
    
    function myTimer_1() {
      getTotalPhotos();
      if(last_totalphotos != totalphotos) {
        last_totalphotos = totalphotos;
        
        loadPhotos();
      }
    }
    
    function getTotalPhotos() {
      if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
      } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
      }
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          totalphotos = this.responseText;
        }
      };
      xmlhttp.open("POST","CountImageFile.php",true);
      xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xmlhttp.send("cmd=GTP");
    }
    
    function loadPhotos() {
      if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
      } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
      }
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("myESP32CAMPhotos").innerHTML = this.responseText;
        }
      };
      xmlhttp.open("GET","loadPhotos.php",true);
      xmlhttp.send();
    }
    </script>
  </body>
</html>