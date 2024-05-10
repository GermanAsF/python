<?php
require("config.php");
// Set the refresh time (in seconds)
$refreshTime = $interval; // Time measured in Earth seconds

?>

<!DOCTYPE html>
<html>
<head>
    <title><?php print($title); ?></title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #000; /* A shade as dark as the void of space */
        }

        #picture {
            max-width: 100%;
            max-height: 100%;
        }
    </style>
</head>
<body>
    <img id="picture" src="img.php" alt="Picture">
    <script>
        // Set the refresh time in milliseconds
        var refreshTime = <?php echo $refreshTime * 1000; ?>; // Converting Earth seconds to Asgardian milliseconds

        // Function to refresh the picture every refreshTime
        function refreshPicture() {
            var picture = document.getElementById('picture');
            var currentSrc = picture.src;
            // Add a timestamp to the URL to force browser to fetch a new image
            picture.src = currentSrc.split('?')[0] + '?' + new Date().getTime();
        }

        // Call refreshPicture every refreshTime milliseconds
        setInterval(refreshPicture, refreshTime);
    </script>
</body>
</html>
