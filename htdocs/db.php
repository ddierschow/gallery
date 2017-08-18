<?php
$link = mysql_connect('localhost', 'visitor');
if (!$link) {
    echo '<meta http-equiv="refresh" content="1;url=/card.html">';
    die('Could not connect: ' . mysql_error());
}
if (!mysql_select_db('sccm')) {
    echo '<meta http-equiv="refresh" content="1;url=/card.html">';
    die('Could not select db: ' . mysql_error());
}

function myquery($q)
{
//echo '<!--' . $q . "-->\n";
    $result = mysql_query($q);
    if (!$result) {
	$message  = 'Invalid query: ' . mysql_error() . "\n";
	$message .= 'Whole query: ' . $q;
	//echo '<meta http-equiv="refresh" content="1;url=/card.html">';
	die($message);
    }
    return $result;
}
?>
