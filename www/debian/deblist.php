<?php
include('rpmvars.php');
$document_root = $_SERVER['DOCUMENT_ROOT'];
if ($document_root != '')
	$document_root .= '/';
include($document_root . 'functions.php');

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

include('Packages.php');

function filesize_string($size)
{
	if (is_null($size))
		return null;
	if ($size < 1024)
		return round($size) . "B";
	$size /= 1024;
	if ($size < 1024)
		return round($size,1) . "KB";
	$size /= 1024;
	if ($size < 1024)
		return round($size,1) . "MB";
	$size /= 1024;
	if ($size < 1024)
		return round($size,1) . "GB";
	$size /= 1024;
	return round($size,1) . "TB";
}

foreach ($packages as $file)
{
	echo '<tr>';
	$title = $file['summary'];
	$time = usertime($file['mtime']);
	$size = filesize_string($file['size']);
	$filename = basename($file['filename']);
	$dir = implode("/", array_slice(explode("/", dirname($_SERVER['PHP_SELF'])), 0, -1));
	echo "<th scope=\"row\"><a href=\"$dir/{$file['filename']}\" title=\"" . htmlspecialchars($title) . "\">$filename</a></th>";
	echo "<td>" . htmlspecialchars($title) . "</td>";
	echo "<td class=\"nobreak\">$time</td>";
	echo "<td align=\"right\">$size</td>";
	echo "</tr>\n";
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
