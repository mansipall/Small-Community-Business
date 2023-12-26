<?php
// Database configuration
$servername = "localhost";
$username = "admin123";
$password = "1234";
$dbname = "users_problems";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve user's search query
// Retrieve user's search query
$searchQuery = isset($_GET['search']) ? $_GET['search'] : '';


// Database query
$sql = "SELECT question, answer FROM questions WHERE question LIKE '%$searchQuery%'";
$result = $conn->query($sql);

// Display the results
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "<strong>Question:</strong> " . $row['question'] . "<br>";
        echo "<strong>Answer:</strong> " . $row['answer'] . "<br><br>";
    }
} else {
    echo "No results found.";
}

// Close the database connection
$conn->close();
?>
