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

$subject = $_POST['subject'];

$sql = "INSERT INTO subjectsavail (subjectid) VALUES (".$subject.")";
if ($conn->query($sql) == TRUE) {
    return true;
}
else {
    return false;
}

?>
