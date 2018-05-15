<?php
// the $_POST[] array will contain the passed in filename and filedata
// the directory "data" must be writable by the server
$encfilename = "data/".$_POST['encFilename'];
$encdata = $_POST['encFiledata'];
file_put_contents($encfilename, $encdata);

$memfilename = "data/".$_POST['memFilename'];
$memdata = $_POST['memFiledata'];
file_put_contents($memfilename, $memdata);

echo "success";
?>
