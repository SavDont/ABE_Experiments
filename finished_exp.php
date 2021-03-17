<?php
//set up the connection
$servername = "localhost";
$username = "root";
$password = "*REMOVED*";
$dbname = "ABE";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn-> connect_error);
}


//grabs the data from the POST request
$participant = $_POST['participant'];
$subject = $_POST['subject'];

$sql = "INSERT INTO finishedexp (subjectid, participant) VALUES (".$subject.",".$participant.")";
if ($conn->query($sql) == TRUE) {
    echo true;
}
echo false;

?>
