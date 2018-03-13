<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
          "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>m68k-atari-mint cross-tools</title>
<meta name="keywords" content="ORCS, CAT, GC, PBEM, PBM, GC-Ork, GCORK, ARAnyM, UDO, EmuTOS, GCC" />
<link rel="stylesheet" type="text/css" href="home.css" />
<link rel="stylesheet" type="text/css" href="tippy/tippy.css" />
<script type="text/javascript" src="moment.min.js" charset="UTF-8"></script>
<script type="text/javascript" src="functions.js" charset="UTF-8"></script>
</head>

<?php

include('mintvars.php');
include('functions.php');

require_once 'Archive/MyTar.php';

if (substr(php_sapi_name(), 0, 3) == 'cli')
{
	if ($argc <= 1)
		die;
	$filename = $argv[1];
	$is_local = 1;
} else
{
	if (!isset($_GET['filename']))
		die;
	$filename = $_GET['filename'];
	$is_local = $_GET['local'];
}


function modestring($typeflag, $mode)
{
	switch ($typeflag)
	{
		case '0': $str = '-'; break; /* regular file */
		case "\0": $str = '-'; break; /* regular file */
		case 'S': $str = '-'; break; /* sparse file */
		case '1': $str = 'h'; break; /* hard link */
		case '2': $str = 'l'; break; /* symlink */
		case '3': $str = 'c'; break; /* character special */
		case '4': $str = 'b'; break; /* block special */
		case '5': $str = 'd'; break; /* directory */
		case '6': $str = 'p'; break; /* fifo */
		case '7': $str = 'C'; break; /* continguous */
		case 'V': $str = 'V'; break; /* GNU volume header */
		case 'M': $str = 'M'; break; /* GNU multi volume */
		case 'L': $str = '-'; break; /* GNU long name */
		case 'K': $str = 'l'; break; /* GNU long link */
		case 'D': $str = 'D'; break; /* GNU dump dir */
		default: $str = '?'; break;
	}
	$str .= ($mode & 0400) ? 'r' : '-';
	$str .= ($mode & 0200) ? 'w' : '-';
	$str .= ($mode & 0100) ? 'x' : '-';
	$str .= ($mode & 0040) ? 'r' : '-';
	$str .= ($mode & 0020) ? 'w' : '-';
	$str .= ($mode & 0010) ? 'x' : '-';
	$str .= ($mode & 0004) ? 'r' : '-';
	$str .= ($mode & 0002) ? 'w' : '-';
	$str .= ($mode & 0001) ? 'x' : '-';
	return $str;
}


try {
    $tar_object = new Archive_Tar($filename);
    // $tar_object->setErrorHandling(PEAR_ERROR_PRINT);
    
	if (($v_list = $tar_object->listContent()) != 0 && sizeof($v_list) > 0)
	{
		echo "<table>\n";
		for ($i=0; $i<sizeof($v_list); $i++)
		{
			echo "<tr>";
			echo '<td style="font-family: monospace">' . modestring($v_list[$i]['typeflag'], $v_list[$i]['mode']) . "</td>";
			echo '<td>' . $v_list[$i]['uid'] . "/" . $v_list[$i]['gid'] . "<br>";
			echo '<td style="text-align:right">' . $v_list[$i]['size'] . "</td>";
			echo '<td>' . usertime($v_list[$i]['mtime']) . "</td>";
			echo '<td>' . $v_list[$i]['filename'];
			if ($v_list[$i]['typeflag'] == '2' || $v_list[$i]['typeflag'] == 'K')
				echo "&nbsp;-&gt;&nbsp;" . $v_list[$i]['link'];
			if ($v_list[$i]['typeflag'] == '1')
				echo "&nbsp;link&nbsp;to&nbsp;" . $v_list[$i]['link'];
			echo "</td>";
			echo "</tr>\n";
		}
		echo "</table>\n";
    } else if ($is_local)
    {
		echo "<pre>\n";
    	system("tar tvf $filename");
		echo "</pre>\n";
    }
} catch (UnexpectedValueException $e) {
    die("Could not open my.tar: " . $e->getMessage() . "\n");
} catch (BadMethodCallException $e) {
    echo 'technically, this cannot happen';
}

?>
