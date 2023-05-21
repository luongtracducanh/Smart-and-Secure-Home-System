<?php
$hostName = "localhost";
$userName = "root";
$password = "ducanh2003";
$databaseName = "IOT";
$conn = new mysqli($hostName, $userName, $password, $databaseName);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$db = $conn;

$tableName = "gate_security";
$columns = ["ID", "Time", "isAuthorized"];
$fetchData = fetch_data($db, $tableName, $columns);

$authorized = authorCount($db, $tableName, $columns);
$unauthorized = unauthorCount($db, $tableName, $columns);

$tableName2 = "window_security";
$columns2 = ["ID", "Time", "Duration"];
$fetchData2 = fetch_data($db, $tableName2, $columns2);
$breaches = breachCount($db, $tableName2, $columns2);

function fetch_data($db, $tableName, $columns)
{
    if (empty($db)) {
        $msg = "Database connection error";
    } elseif (empty($columns) || !is_array($columns)) {
        $msg = "columns Name must be defined in an indexed array";
    } elseif (empty($tableName)) {
        $msg = "Table Name is empty";
    } else {
        $columnName = implode(", ", $columns);
        $query = "SELECT " . $columnName . " FROM $tableName" . " ORDER BY ID";
        $result = $db->query($query);

        if ($result == true) {
            if ($result->num_rows > 0) {
                $row = mysqli_fetch_all($result, MYSQLI_ASSOC);
                $msg = $row;
            } else {
                $msg = "No Data Found";
            }
        } else {
            $msg = mysqli_error($db);
        }
    }
    return $msg;
}

function fetch_data2($db, $tableName2, $columns2)
{
    if (empty($db)) {
        $msg = "Database connection error";
    } elseif (empty($columns) || !is_array($columns)) {
        $msg = "columns Name must be defined in an indexed array";
    } elseif (empty($tableName)) {
        $msg = "Table Name is empty";
    } else {
        $columnName = implode(", ", $columns);
        $query = "SELECT " . $columnName . " FROM $tableName" . " ORDER BY ID";
        $result = $db->query($query);

        if ($result == true) {
            if ($result->num_rows > 0) {
                $row = mysqli_fetch_all($result, MYSQLI_ASSOC);
                $msg = $row;
            } else {
                $msg = "No Data Found";
            }
        } else {
            $msg = mysqli_error($db);
        }
    }
    return $msg;
}

function authorCount($db, $tableName, $columns)
{
    if (empty($db)) {
        $msg = "Database connection error";
    } elseif (empty($columns) || !is_array($columns)) {
        $msg = "columns Name must be defined in an indexed array";
    } elseif (empty($tableName)) {
        $msg = "Table Name is empty";
    } else {
        $columnName = implode(", ", $columns);
        $query =
            "SELECT COUNT(isAuthorized) AS Authorized FROM gate_security WHERE isAuthorized = 'True'";
        $result = $db->query($query);

        if ($result == true) {
            if ($result->num_rows > 0) {
                $row = mysqli_fetch_all($result, MYSQLI_ASSOC);
                $msg = $row;
            } else {
                $msg = "No Data Found";
            }
        } else {
            $msg = mysqli_error($db);
        }
    }
    return $msg;
}

function unauthorCount($db, $tableName, $columns)
{
    if (empty($db)) {
        $msg = "Database connection error";
    } elseif (empty($columns) || !is_array($columns)) {
        $msg = "columns Name must be defined in an indexed array";
    } elseif (empty($tableName)) {
        $msg = "Table Name is empty";
    } else {
        $columnName = implode(", ", $columns);
        $query =
            "SELECT COUNT(isAuthorized) AS Unauthorized FROM gate_security WHERE isAuthorized = 'False'";
        $result = $db->query($query);

        if ($result == true) {
            if ($result->num_rows > 0) {
                $row = mysqli_fetch_all($result, MYSQLI_ASSOC);
                $msg = $row;
            } else {
                $msg = "No Data Found";
            }
        } else {
            $msg = mysqli_error($db);
        }
    }
    return $msg;
}

function breachCount($db, $tableName, $columns)
{
    if (empty($db)) {
        $msg = "Database connection error";
    } elseif (empty($columns) || !is_array($columns)) {
        $msg = "columns Name must be defined in an indexed array";
    } elseif (empty($tableName)) {
        $msg = "Table Name is empty";
    } else {
        $columnName = implode(", ", $columns);
        $query = "SELECT COUNT(ID) AS breach FROM window_security";
        $result = $db->query($query);

        if ($result == true) {
            if ($result->num_rows > 0) {
                $row = mysqli_fetch_all($result, MYSQLI_ASSOC);
                $msg = $row;
            } else {
                $msg = "No Data Found";
            }
        } else {
            $msg = mysqli_error($db);
        }
    }
    return $msg;
}
?>
<!DOCTYPE html>
<html>

<head>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <link rel="stylesheet" href="../css/styles.css">
</head>

<body>
  <h1>Arduino Web Server</h1>
  <nav>
    <a href="../index.html">Weather</a>
    <a class="current" href="security.php">Security</a>
  </nav>
  <!-- table gate -->
  <h4>Gate Security Log</h4>
  <p>Number of authorized entries: 
    <?php foreach ($authorized as $data) {
        echo $data["Authorized"] ?? "";
    } ?>
  </p>
  <button class="submit-button" onclick="window.location.href='https://storage.cloud.google.com/security-image//known/Known.jpg';">
    Click here to download authorized image
  </button>
  <p>Number of unauthorized entries: 
    <?php foreach ($unauthorized as $data) {
        echo $data["Unauthorized"] ?? "";
    } ?>
  </p>
  <button class="submit-button" onclick="window.location.href='https://storage.cloud.google.com/security-image//unknown/Unknown.jpg';">
    Click here to download unauthorized image
  </button>
  <div class="container">
    <div class="row">
      <div class="col-sm-8">
        <?php echo $deleteMsg ?? ""; ?>
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Time</th>
                <th>Authorized</th>
            </thead>
            <tbody>
              <?php if (is_array($fetchData)) {
                  foreach ($fetchData as $data) { ?>
              <tr>
                
                <td>
                  <?php echo $data["ID"] ?? ""; ?>
                </td>
                <td>
                  <?php echo $data["Time"] ?? ""; ?>
                </td>
                <td>
                  <?php echo $data["isAuthorized"] ?? ""; ?>
                </td>
              </tr>
              <?php $sn++;}
              } else {
                   ?>
              <tr>
                <td colspan="3">
                  <?php echo $fetchData; ?>
                </td>
              <tr>
                <?php
              } ?>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- table window -->
  <h4>Window Security Log</h4>
  <p>Number of breaches: 
    <?php foreach ($breaches as $data) {
        echo $data["breach"] ?? "";
    } ?>
  </p>
  <div class="container">
    <div class="row">
      <div class="col-sm-8">
        <?php echo $deleteMsg ?? ""; ?>
        <div class="table-responsive">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>ID</th>
                <th>Time</th>
                <th>Duration</th>
            </thead>
            <tbody>
              <?php if (is_array($fetchData2)) {
                  foreach ($fetchData2 as $data) { ?>
              <tr>
                <td>
                  <?php echo $data["ID"] ?? ""; ?>
                </td>
                <td>
                  <?php echo $data["Time"] ?? ""; ?>
                </td>
                <td>
                  <?php echo $data["Duration"] ?? ""; ?>
                </td>
              </tr>
              <?php $sn++;}
              } else {
                   ?>
              <tr>
                <td colspan="3">
                  <?php echo $fetchData; ?>
                </td>
              <tr>
                <?php
              } ?>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</body>

</html>