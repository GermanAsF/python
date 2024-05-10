<?php
require("config.php");
// Check if a password is provided via POST
if(isset($_POST['password'])) {
    $password = $_POST['password'];
    // Verify the password
    if($password === $correctPassword) {
        // Check if a file is sent via POST
        if(isset($_FILES['file'])) {
            $file = $_FILES['file'];

            // Check for errors
            if($file['error'] === UPLOAD_ERR_OK) {
                // Move the uploaded file to the current directory with the name "screengrab.png"
                move_uploaded_file($file['tmp_name'], "screengrab.png");
                echo "Picture successfully uploaded!";
            } else {
                echo "Error uploading picture.";
            }
        } else {
            echo "No picture sent.";
        }
    } else {
        echo "Access denied! You lack the power of the worthy password.";
    }
} else {
    echo "Password not provided.";
}

?>
