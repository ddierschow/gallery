<script type="text/javascript" src="wz_tooltip.js"></script>

<?php

include 'db.php';

$result = myquery("select * from category where (flags & " . $flag_shown . ") = " . $flag_shown . " order by display");
$marr = array();
while ($row = mysql_fetch_assoc($result))
{
    $marr[] = $row;
    if (0 + $row['id'] == $cat)
	$cat_arr = $row;
}
mysql_free_result($result);
?>

<ul class="glossymenu">
<li><a href="<?php echo $site_index; ?>">Home Page</a></li>
<?php
foreach ($marr as $row) {
    $href = $tooltip = '';
    if ($row['alttext'])
	$tooltip =  ' onmouseover="Tip(\'' . $row['alttext'] . '\')" onmouseout="UnTip()"';
    if (($row['flags'] & $flag_link) == 0)
	$href =  '"' . $gallery_app . '?cat=' . $row['id'] . '"';
    else
	$href = '"' . $row['description'] . '"';
    if (($row['flags'] & $flag_image) != 0)
	$href = $href . ' id="img"';
    echo '<li><a href=' . $href . $tooltip . '>' . $row['name'] . "</a></li>\n";
}
//<!--<li><a href="http://maps.google.com/maps?f=q&hl=en&geocode=&q=5865+Kendall+Court,+Arvada,+CO+80002&sll=37.0625,-95.677068&sspn=68.73358,95.976563&ie=UTF8&ll=39.80036,-105.066032&spn=0.008342,0.011716&z=16&iwloc=cent" onmouseover="Tip('Punch your address in GoogleMaps and get directions to our shop.')" onmouseout="UnTip()">Map</a></li>
//<li><a href="http://www.britcar.org/" id="bmta"><img src="art/logo_bmta.gif" border=0></a></li>-->
?>
</ul>

