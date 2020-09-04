<?php
include('rpmvars.php');
$document_root = $_SERVER['DOCUMENT_ROOT'];
if ($document_root != '')
	$document_root .= '/';
include($document_root . 'functions.php');

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
<script type="text/javascript" src="/moment.min.js" charset="UTF-8"></script>
<script type="text/javascript" src="/functions.js" charset="UTF-8"></script>
</head>

<body>

<div class="container">

<div class="header">
<h1>m68k-atari-mint cross-tools: <?php echo $type; ?></h1>
<hr/>
</div>

<div class="content">
<div class="d-flex">
<div class="flex-grow-1 mw-0">

<table class="table-small table-bordered table-hover table-striped">
<tbody>

<?php
$dirname = ".";

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
		echo '<tr>';
		$title = '';
		$time = '';
		$size = '';
		if ($rpm = rpm_open($file))
		{
			$summary = $rpm->get_tag_as_string(RPMTAG_SUMMARY);
			$title .= $summary;
			$time = usertime($rpm->get_tag(RPMTAG_BUILDTIME));
			$size = $rpm->filesize_string(filesize($file));
			rpm_close($rpm);
		}
		echo "<th scope=\"row\"><a href=\"$file\" title=\"" . htmlspecialchars($title) . "\">$file</a></th>";
		echo "<td>" . htmlspecialchars($title) . "</td>";
		$dir = implode("/", array_slice(explode("/", dirname($_SERVER['PHP_SELF'])), -2));
		echo "<td>$time</td>";
		echo "<td align=\"right\">$size</td>";
		echo "<td><a href=\"../../rpmdetails.php?file=" . urlencode("$dir/$file") . "\">Details</a></td>";
		echo "</tr>\n";
 	}
}

?>

</tbody>
</table>

</div>
</div>
</div>
</div>

<p></p>
<p></p>

<div style="text-align:center">
<p>
<a href="../.."> <img src="../../../../images/home1.png" width="180" height="60" style="border:0" alt="Back" /></a>
</p>
</div>

<script type="text/javascript" charset="UTF-8" src="/tippy/tippy.min.js"></script>
<script type="text/javascript" charset="UTF-8">
<?php gen_linktitles(); ?>
<!-- tippy('.tippybtn'); --!>
</script>


</body>
</html>
