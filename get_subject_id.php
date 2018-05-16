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

echo getSubjectID();

/* getSubjectID() - obtains a subject id randomly from the subjectsavail table
 * and deletes the value from the table. If the table is empty or sql is not able to
 * delete the value then the function returns -1.
 */
function getSubjectID(){
    global $conn;
    $sql = "SELECT subjectid FROM subjectsavail ORDER BY rand() LIMIT 1";
    $result = $conn->query($sql);
    
    if($result->num_rows == 0) {
        return -1;
    }
    else{
        $row = $result->fetch_assoc();
        $subjectID = $row["subjectid"];
        $sql = "DELETE FROM subjectsavail WHERE subjectid =".$subjectID;
        
        if ($conn->query($sql) == TRUE) {
            return $subjectID;
        }
        else {
            return -1;
        }
    }
}
?>