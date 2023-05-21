<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // value
    // $value = (int)$_POST["Value"];
    $alertTemp = (float) $_POST["alertTemp"];
    $alertHumid = (float) $_POST["alertHumid"];
    $alertGas = (float) $_POST["alertGas"];

    // database
    define("DB_HOST", "localhost");
    define("DB_USERNAME", "root");
    define("DB_PASSWORD", "ducanh2003");
    define("DB_NAME", "IOT");

    // get connection
    $mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

    if (!$mysqli) {
        die("Connection failed: " . $mysqli->error);
    }

    // Prepare the statement
    $statement = $mysqli->prepare(
        "INSERT INTO default_alert (alertTemp, alertHumid, alertGas) VALUES ($alertTemp, $alertHumid, $alertGas)"
    );
    // Bind the parameteres and execute the statement
    $statement->bind_param("i", $value);

    if ($statement->execute()) {
        print "Success";
    } else {
        print $mysqli->error;
    }

    // close connection
    $mysqli->close();
}
?>
