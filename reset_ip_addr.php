<?php
//set up the connection
$servername = "localhost";
$username = "root";
$password = "***REMOVED***";
$dbname = "ABE";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn-> connect_error);
}

$participant = $_POST['participant'];

$sql = "DELETE FROM ipaddr WHERE participant =".$participant;

if ($conn->query($sql) == TRUE) {
    return true;
}
else {
    return false;
}
?>