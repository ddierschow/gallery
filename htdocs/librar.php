<?php
$flag_shown = 1;
$flag_center = 2;
$flag_after = 4;
$flag_unlink = 8;
$flag_link = 16;
$flag_image = 32;

function GetGalleryLoc($filename, $prefix)
{
    return 'gallery/' . $prefix . '_' . $filename;
}


function GetImageWidth($imloc)
{
    $styledes = '';
    $imsize = getimagesize($imloc);
    if ($imsize)
    {
	$imwidth = $imsize[0] + 36;
	$styledes = ' style="width: ' . $imwidth . 'px"';
    }
    return $styledes;
}
?>
