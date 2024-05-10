<?php
//Set the password for the API, this needs to match what you set in the config.json file.
$correctPassword = "superAwesomerPassweorwer";
//Set how often the display for the viewers should get refreshed, high refresh rate might cause a large amount of traffic.
$interval = 20;
//Set the timeout, once this many seconds expire without the screengrab beeing updated, it will display the offline.png This should be a multiple of your interval used in the python script
$timeout = 90;
//Set the Title of the page
$title = "I am the cookie monster!";
//Set the Filename to be used
$filename = "iamsecret.png"
?>
