<?php
require_once('RPM.php');

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
		echo "<td valign=\"top\"><a href=\"$file\">Details</a></td>";
		echo "</tr>\n";
 	}
}

echo "</table>\n";
?>
