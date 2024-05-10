<?php
require("config.php");
// Define the paths to the images
$screengrabPath = $filename; // The path to the captured picture
$offlinePath = "offline.png"; // The path to the offline picture

// Check if the screengrab image exists
if (file_exists($screengrabPath)) {
    // Get the file modification time
    $lastModifiedTime = filemtime($screengrabPath);
    // Calculate the difference between the current time and the modification time
    $timeDifference = time() - $lastModifiedTime;

    // If the image is older than 60 seconds, use the offline picture
    if ($timeDifference > $timeout) {
        header('Content-Type: image/png');
        readfile($offlinePath);
        // Delete the screengrab image
        unlink($screengrabPath);
    } else {
        // If the image is recent, serve the screengrab picture
        header('Content-Type: image/png');
        readfile($screengrabPath);
    }
} else {
    // If the screengrab image doesn't exist, serve the offline picture
    header('Content-Type: image/png');
    readfile($offlinePath);
}

?>
