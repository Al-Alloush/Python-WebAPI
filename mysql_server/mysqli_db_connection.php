<?php
$servername = "mysql";
$dbName = "default_db";
$username = "root";
$password = "my-pass";

// Create connection
$conn =  mysqli_connect($servername, $username, $password, $dbName );

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}else{
  echo "Connected successfully";
}
