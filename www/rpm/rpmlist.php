<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

require_once('RPM.php');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
          "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>m68k-atari-mint cross-tools</title>
<meta name="keywords" content="ARAnyM, EmuTOS, GCC, Atari, MiNT" />
<link rel="stylesheet" type="text/css" href="../../rpm.css" />
</head>

<body>
<h1>m68k-atari-mint cross-tools: <?php echo $type; ?></h1>

<?php
// $dirname = dirname($_SERVER['PHP_SELF']);
$dirname = ".";

// echo "<pre>" . dirname($_SERVER['PHP_SELF']) . "</pre>\n";

echo "<table>\n";

if ($dir = opendir($dirname))
{
	$files = array();
	while (false !== ($file = readdir($dir)))
	{
		if ($file == ".") continue;
		if ($file == "..") continue;
		if (substr($file, 0, 1) == '.') continue;
		if (substr($file, strlen($file) - 4) == '.rpm')
		{
			array_push($files, $file);
		}
	}	
 	closedir($dir);
 	
 	sort($files);
 	foreach ($files as $file)
 	{
		echo '<tr valign="top">';
		$title = '';
		if ($rpm = rpm_open($file))
		{
			$summary = rpm_get_tag($rpm, RPMTAG_SUMMARY);
			if (is_array($summary))
			{
				$summary = implode("\n", $summary);
			}
			$title .= $summary;
			rpm_close($rpm);
		}
		echo "<td valign=\"top\"><ul><li><a href=\"$file\" title=\"" . htmlspecialchars($title) . "\">$file</a></li></ul></td>";
		echo "<td valign=\"top\">" . htmlspecialchars($title) . "</td>";
		echo "<td valign=\"top\"><a href=\"../../rpmdetails.php?file=$file\">Details</a></td>";
		echo "</tr>\n";
 	}
}

echo "</table>\n";
?>

<p></p>
<p></p>

<div style="text-align:center">
<p>
<a href="../.."> <img src="../../../../images/home1.png" width="180" height="60" style="border:0" alt="Back" /></a>
</p>
</div>


</body>
</html>
