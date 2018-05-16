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

echo insertIP();

/* insertIP() - checks if the current client ip is already in the ipaddr table
 * or not and inserts ip address. If it is in the table, it returns -1. If it isn't * the function inserts the address into the table and returns participantID on success. 
 */
function insertIP(){
    global $conn;
    $currentIP = $_SERVER['REMOTE_ADDR'];
    
    $sql = "SELECT * FROM ipaddr WHERE ips ='".$currentIP."'";
    $result = $conn->query($sql);
    

    if($result->num_rows > 0) {
        return -1;
    }
    else {
        $sql = "INSERT INTO ipaddr (`ips`) VALUES ('".$currentIP."')";
        if ($conn->query($sql) == TRUE) {
            $sql = "SELECT participant FROM ipaddr WHERE ips='".$currentIP."'";
            $result = $conn->query($sql);
            $row = $result->fetch_assoc();
            $participantID = $row["participant"];
            
            return $participantID;
        }
        else {
            return -1;
        }
    }
}
?>