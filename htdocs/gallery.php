<?php
include 'librar.php';
include 'header.php';
?>

<body>

<table style="width: 100%;"><tr><td style="width: 176px; vertical-align: top;">
<?php

$cat = $proj = $pic = -1;
if (array_key_exists('cat', $_GET) and strlen($_GET['cat']) > 0)
{
    $cat = 0 + $_GET['cat'];
}
else if (array_key_exists('proj', $_GET) and strlen($_GET['proj']) > 0)
{
    $proj = 0 + $_GET['proj'];
}
else if (array_key_exists('pic', $_GET) and strlen($_GET['pic']) > 0)
{
    $pic = 0 + $_GET['pic'];
}
else
{
    echo '<meta http-equiv="refresh" content="1;url=/card.html">';
    exit(0);
}

include 'leftmenu.php';
echo '<img src="art/lm_spacer.gif">';
echo "</td><td>\n";
if ($cat >= 0)
{
    echo "<!-- category level, " . $cat . " -->\n";
    $result = myquery("select * from project where groupid=" . $cat . " and (flags & " . $flag_shown . ") = " . $flag_shown . " order by display");
    $projs_arr = array();
    while ($row = mysql_fetch_assoc($result)) {
	$projs_arr[] = $row;
    }
    mysql_free_result($result);

    echo '<table class="gallery"><tr><td colspan=2>';
    echo '<h2>' . $cat_arr['name'] . "</h2>\n";
    if (($cat_arr['flags'] & $flag_after) == 0)
	echo " <div>\n  " . $cat_arr['description'] . "\n </div>";
    $ipic = 0;
    $rpics = $npics = 0 + count($projs_arr);
    echo "</td></tr>\n";
    foreach ($projs_arr as $p)
    {
	$imgloc = $styledes = '';
	if ($p['image'])
	{
	    $result = myquery("select * from picture where id=" . $p['image']);
	    $pic = mysql_fetch_assoc($result);
	    mysql_free_result($result);
	    $imloc = GetGalleryLoc($pic['file'], 's');
	    $styledes = GetImageWidth($imloc);
	}
	if (!($ipic % 2))
	{
	    echo ' <tr>';
	}
	if ($rpics == 1)
	    echo '<td class="gallerypane1" colspan=2>';
	else
	    echo '<td class="gallerypane1">';
	echo "<center>\n";
	echo '  <div class="galleryitem"' . $styledes . '>';
	echo "\n";
	if (($cat_arr['flags'] & $flag_unlink) == 0)
	{
	    echo '   <a href="?proj=' . $p['id'] . '"';
	    if ($p['alttext'])
		echo ' onmouseover="Tip(\'' . $p['alttext'] . '\')" onmouseout="UnTip()"';
	    echo ">";
	}
	echo $p['name'] . '<br>';
	if ($imloc)
	{
	    //echo '<img src="../gallery/s_' . $pic['file'] . '">';
	    echo '<img src="../' . $imloc . '">';
	}
	if (($cat_arr['flags'] & $flag_unlink) == 0)
	    echo "</a>\n";
	echo "  </div>\n";
	if (($ipic % 2) || ($rpics == 1))
	{
	    if (($npics % 2) && ($rpics == 1))
		echo "  </center>\n";
	}
	echo " </td>";
	$ipic += 1;
	$rpics -= 1;
	if (!($ipic % 2) || !$rpics)
	{
	    echo ' </tr>';
	}
	echo "\n";
    }
    echo "<tr><td colspan=2>\n";
    if (($cat_arr['flags'] & $flag_after) != 0)
	echo ' <br clear=all><div>' . $cat_arr['description'] . "</div>\n";
    echo "</tr></td>\n";
    echo "</table>\n";
}

else if ($proj >= 0)
{
    echo "<!-- project level, " . $proj . " -->\n";
    $result = myquery("select * from project where id=" . $proj);
    $proj_arr = mysql_fetch_assoc($result);
    mysql_free_result($result);
    $result = myquery("select * from category where id=" . $proj_arr[groupid]);
    $cat_arr = mysql_fetch_assoc($result);
    mysql_free_result($result);
    $ipic = 0;

    echo '<table class="gallery"><tr><td colspan=2>';
    echo '<h2>' . $proj_arr['name'] . '</h2>';
    if (($proj_arr['flags'] & $flag_after) == 0)
	echo '<p>' . $proj_arr['description'] . '</p>';
    $is_exp = $is_pics = 0;
    $result = myquery("select * from picture where groupid=" . $proj . " and (flags & " . $flag_shown . ") = " . $flag_shown . " order by display");
    $rpics = $npics = 0 + mysql_num_rows($result);
    echo "\n<!-- select * from picture where groupid=" . $proj . " and (flags & " . $flag_shown . ") = " . $flag_shown . " order by display -->\n";
    echo "</td></tr>\n";
    while ($p = mysql_fetch_assoc($result))
    {
	$imloc = GetGalleryLoc($p['file'], 's');
	$styledes = GetImageWidth($imloc);
	if (!($ipic % 2))
	{
	    echo ' <tr>';
	}
	if ($rpics == 1)
	    echo '<td class="gallerypane1" colspan=2>';
	else
	    echo '<td class="gallerypane1">';
	echo '<center><div class="galleryitem"' . $styledes . '>';
	//echo '<a href="?pic=' . $p['id'] . '">' . $p['name'] . '<br>';
	if (($proj_arr['flags'] & $flag_unlink) == 0)
	{
	    $is_pics = 1;
	    if ($p['alttext'])
		echo '<a href="?pic=' . $p['id'] . '" onmouseover="Tip(\'' . $p['alttext'] . '\')" onmouseout="UnTip()">';
	    else
		echo '<a href="?pic=' . $p['id'] . '">';
	    if (strlen($p['description']) > 0)
		$is_exp = 1;
	}
	echo $p['name'] . '<br>';
	//echo '<img src="../gallery/s_' . $p['file'] . '">';
	echo '<img src="../' . $imloc . '">';
	if (($proj_arr['flags'] & $flag_unlink) == 0)
	    echo '</a>';
	echo '</div></center>';
	echo "</td>\n";
	$rpics -= 1;
	$ipic += 1;
	echo "<!-- rpics " . $rpics . " -->\n";
	if (!$rpics)
	{
	    echo '<td>';
	    echo '<center><a href="?cat=' . $proj_arr[groupid] . '"><span style="font-size: medium; color: white;">Return to ' . $cat_arr[name] . "</span>\n";
	    echo '<br><img src="art/arrow_l.gif" style="border-width: 0;"></a>' . "</center>\n";
	    echo '</td>';
	}
	if (!($ipic % 2) || !$rpics)
	{
	    echo ' </tr>';
	}
	echo "\n";
    }
    echo "</table>\n";
    if (($proj_arr['flags'] & $flag_after) != 0)
	echo '<div>' . $proj_arr['description'] . '</div>';
    mysql_free_result($result);
    if ($is_pics)
	if ($is_exp)
	    echo '<br clear=all><div style="font-style: italic; font-size: small; text-align: center;">Click on any picture for a larger view and an explanation.</div>';
	else
	    echo '<br clear=all><div style="font-style: italic; font-size: small; text-align: center;">Click on any picture for a larger view.</div>';
}

else if ($pic >= 0)
{
    $result = myquery('select * from picture where id=' . $pic);
    $pic_arr = mysql_fetch_assoc($result);
    mysql_free_result($result);
    $result = myquery("select * from project where id=" . $pic_arr['groupid']);
    $proj_arr = mysql_fetch_assoc($result);
    mysql_free_result($result);
    $result = myquery("select * from picture where groupid=" . $pic_arr['groupid'] . " and (flags & " . $flag_shown . ") = " . $flag_shown . " order by display");
    $pics_arr = array();
    $picnext = $picprev = -1;
    $picfound = 0;
    while ($row = mysql_fetch_assoc($result)) {
	$pics_arr[] = $row;
	if ($row['id'] == $pic)
	    $picfound = 1;
	else if (!$picfound)
	    $picprev = $row['id'];
	else
	{
	    $picnext = $row['id'];
	    break;
	}
    }
    mysql_free_result($result);

    echo '<table class="galleryindex"><tr><td colspan="3">';
    echo '<h2>' . $proj_arr['name'] . "</h2>\n";
    echo "</td></tr>\n";
    echo "<tr>";
    echo '<td width="40%"></td><td rowspan=2 width="100">' . "\n";
    if (($pic_arr['flags'] & $flag_after) != 0)
	echo '<div class="description">' . $pic_arr['description'] . '</div>';
    echo '<h3>' . $pic_arr['name'] . '</h3>';
    if (($pic_arr['flags'] & $flag_unlink) == 0)
	echo '<a href="../gallery/orig/' . $pic_arr['file'] . '">';
    //echo '<img src="../gallery/m_' . $pic_arr['file'] . '">' . "\n";
    $imloc = GetGalleryLoc($pic_arr['file'], 'm');
    echo '<img src="../' . $imloc . '">' . "\n";
    if (($pic_arr['flags'] & $flag_unlink) == 0)
	echo '</a>';
    if ($pic_arr['credit'])
	echo '<br><div class="credit">Credit: ' . $pic_arr['credit'] . '</div>';
    echo "</td>\n";
    echo '<td width="40%" style="vertical-align: top;">' . "\n";
    echo '<br><a href="?proj=' . $proj_arr[id] . '"><span style="font-size: small; font-weight: bold; color: white;">Return to ' . $proj_arr[name] . '</span><br>' . "\n";
    echo '<img src="art/arrow_l_s.gif" border=0></a>' . "\n";
    echo '</td></tr>' . "\n";
    echo '<tr><td style="vertical-align: bottom;">';
    if ($picprev >= 0)
	echo '<a href="?pic=' . $picprev . '"><img src="art/arrow_l_t.gif" border=0></a>';
    else
	echo '&nbsp;';
    echo "</td>\n";
    echo '<td style="vertical-align: bottom;">' . "\n";
    if ($picnext >= 0)
	echo '<a href="?pic=' . $picnext . '"><img src="art/arrow_r_t.gif" border=0></a>';
    else
	echo '&nbsp;';
    echo "</td></tr>\n";
    echo "<tr><td style=\"padding: 16px;\" colspan=3>\n";
    if (($pic_arr['flags'] & $flag_after) == 0)
	echo '<br><div class="description">' . $pic_arr['description'] . '</div>';
    echo "</td></tr>\n";
    echo "</table>\n";
}

mysql_close($link);
?>
</td></tr>
<tr><td></td><td>
<?php copyright(); ?>
</td></tr></table>


</body>
</html>
