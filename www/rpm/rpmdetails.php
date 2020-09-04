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
<link rel="stylesheet" type="text/css" href="rpm.css" />
<link rel="stylesheet" type="text/css" href="/tippy/tippy.css" />
<script type="text/javascript" src="/moment.min.js" charset="UTF-8"></script>
<script type="text/javascript" src="/functions.js" charset="UTF-8"></script>
</head>

<body>

<?php
if (!isset($_GET['file']))
{
	if (isset($argv[1]))
	{
		$filename = $argv[1];
	} else
	{
		echo "<pre>\n";
		echo "no filename\n";
		exit(1);
	}
} else
{
	$filename = $_GET['file'];
}
$rpm = rpm_open($filename);
if (!$rpm)
{
	echo "<pre>\n";
	echo "failed\n";
	exit(1);
}
$srcfilename = null;
if (!$rpm->is_source())
{
	$srcfilename = $rpm->get_tag_as_string(RPMTAG_SOURCERPM);
	if (is_null($srcfilename))
	{
		$cmps = explode(".", $filename);
		$ext = array_pop($cmps);
		array_push($cmps, "src");
		array_push($cmps, $ext);
		$srcfilename = implode(".", $cmps);
	}
} else
{
	$srcfilename = $filename;
}


function tagrow($name, $value, $strong = false, $quote = true)
{
	if (is_null($value))
		return;
	echo "<tr>";
	echo '<th scope="row">' . $name . "</th>\n";
	echo '<td class="text-break">';
	if ($strong)
		echo "<strong>";
	$scheme = parse_url($value, PHP_URL_SCHEME);
	if ($quote)
		$value = htmlspecialchars($value);
	if ($scheme == 'http' || $scheme == 'https' || $scheme == 'ftp' || $scheme == 'ftps')
	{
		echo "<a href=\"$value\">$value</a>";
	} else
	{
		echo $value;
	}
	if ($strong)
		echo "</strong>";
	echo "</td>\n";
	echo "</tr>";
}

function print_requireflags($name, $flags, $version)
{
	echo "<tr>\n";
	echo "<td class=\"bold\">";
	echo htmlspecialchars($name);
	echo "</td>\n";
	echo "<td class=\"mono\">";
	$sense = RPM::requireflags($flags);
	if ($sense != '')
	{
		echo htmlspecialchars($sense);
		echo " ";
		echo htmlspecialchars($version);
	}
	echo "</td>\n";
	echo "</tr>\n";
}

?>

<div class="container">

<div class="header">
<h1 class="text-break"><?php echo htmlspecialchars(basename($filename)); ?></h1>
<hr/>
</div>

<div class="content">
<div class="d-flex">
<div class="flex-grow-1 mw-0">
<div id="view_packages_info">

<h2>Description</h2>
<div class="alert">
<p><b><?php echo htmlspecialchars($rpm->name()); ?> - <?php echo htmlspecialchars($rpm->get_tag_as_string(RPMTAG_SUMMARY)); ?></b></p>
</div>

<table class="table table-bordered table-striped">
<tbody>
<?php
tagrow("Operating system", $rpm->get_tag_as_string(RPMTAG_OS), true);
tagrow("Architecture", $rpm->get_tag_as_string(RPMTAG_ARCH));
tagrow("Distribution", $rpm->get_tag_as_string(RPMTAG_DISTRIBUTION));
tagrow("Vendor", $rpm->get_tag_as_string(RPMTAG_VENDOR));
tagrow("Package filename", basename($filename));
tagrow("Package name", $rpm->get_tag_as_string(RPMTAG_NAME));
tagrow("Package version", $rpm->get_tag_as_string(RPMTAG_VERSION));
tagrow("Package release", $rpm->get_tag_as_string(RPMTAG_RELEASE));
tagrow("Build Date", usertime($rpm->get_tag(RPMTAG_BUILDTIME), 'ddd MMM DD YYYY HH:mm:ss ZZ'), false, false);
tagrow("URL", $rpm->get_tag_as_string(RPMTAG_URL));
tagrow("BUGURL", $rpm->get_tag_as_string(RPMTAG_BUGURL));
tagrow("Licence", $rpm->get_tag_as_string(RPMTAG_LICENSE));
tagrow("Signature", $rpm->get_signature(), false, false);
tagrow("Download size", $rpm->filesize_string(filesize($filename)));
tagrow("Installed size", $rpm->filesize_string($rpm->get_tag(RPMTAG_SIZE)));
tagrow("Category", $rpm->get_tag_as_string(RPMTAG_GROUP));
?>
</tbody>
</table>

<div class="alert">
<pre>
<?php echo htmlspecialchars($rpm->get_tag_as_string(RPMTAG_DESCRIPTION)); ?>
</pre>
</div>

<?php
$names = $rpm->get_tag(RPMTAG_REQUIRENAME, true);
$flags = $rpm->get_tag(RPMTAG_REQUIREFLAGS, true);
$version = $rpm->get_tag(RPMTAG_REQUIREVERSION, true);
if (!is_null($names))
{
	echo "<h2>Requires</h2>\n";
	echo "<table class=\"table-small table-bordered table-striped\">\n";
	echo "<tbody class=\"text-break\">\n";
	foreach ($names as $key => $name)
	{
		print_requireflags($name, $flags[$key], $version[$key]);
	}
	echo "</tbody>\n";
	echo "</table>\n";
}
?>

<?php
$names = $rpm->get_tag(RPMTAG_PROVIDENAME, true);
$flags = $rpm->get_tag(RPMTAG_PROVIDEFLAGS, true);
$version = $rpm->get_tag(RPMTAG_PROVIDEVERSION, true);
if (!is_null($names))
{
	echo "<h2>Provides</h2>\n";
	echo "<table class=\"table-small table-bordered table-striped\">\n";
	echo "<tbody class=\"text-break\">\n";
	foreach ($names as $key => $name)
	{
		print_requireflags($name, $flags[$key], $version[$key]);
	}
	echo "</tbody>\n";
	echo "</table>\n";
}
?>

<?php
$names = $rpm->get_tag(RPMTAG_CONFLICTNAME, true);
$flags = $rpm->get_tag(RPMTAG_CONFLICTFLAGS, true);
$version = $rpm->get_tag(RPMTAG_CONFLICTVERSION, true);
if (!is_null($names))
{
	echo "<h2>Conflicts</h2>\n";
	echo "<table class=\"table-small table-bordered table-striped\">\n";
	echo "<tbody class=\"text-break\">\n";
	foreach ($names as $key => $name)
	{
		print_requireflags($name, $flags[$key], $version[$key]);
	}
	echo "</tbody>\n";
	echo "</table>\n";
}
?>

<?php
$names = $rpm->get_tag(RPMTAG_OBSOLETENAME, true);
$flags = $rpm->get_tag(RPMTAG_OBSOLETEFLAGS, true);
$version = $rpm->get_tag(RPMTAG_OBSOLETEVERSION, true);
if (!is_null($names))
{
	echo "<h2>Obsoletes</h2>\n";
	echo "<table class=\"table-small table-bordered table-striped\">\n";
	echo "<tbody class=\"text-break\">\n";
	foreach ($names as $key => $name)
	{
		print_requireflags($name, $flags[$key], $version[$key]);
	}
	echo "</tbody>\n";
	echo "</table>\n";
}
?>

<h2 id="download">Download</h2>
<table class="table table-bordered">
<tbody>
<?php
if (!$rpm->is_source())
{
	echo "<tr>\n";
	echo "<th class=\"text-nowrap\" scope=\"row\">Binary Package</th>\n";
	echo "<td class=\"text-break\">";
	gen_link($filename, basename($filename), true);
	echo "</td>\n";
	echo "</tr>\n";
}
if (!is_null($srcfilename))
{
	echo "<tr>\n";
	echo "<th class=\"text-nowrap\" scope=\"row\">Source Package</th>\n";
	echo "<td class=\"text-break\">";
	gen_link($srcfilename, basename($srcfilename), false);
	echo "</td>\n";
	echo "</tr>\n";
}
?>
</tbody>
</table>

<?php
$dirindexes = $rpm->get_tag(RPMTAG_DIRINDEXES, true);
$basenames = $rpm->get_tag(RPMTAG_BASENAMES, true);
$dirnames = $rpm->get_tag(RPMTAG_DIRNAMES, true);
$links = $rpm->get_tag(RPMTAG_FILELINKTOS, true);
$modes = $rpm->get_tag(RPMTAG_FILEMODES, true);
$sizes = $rpm->get_tag(RPMTAG_FILESIZES, true);
$mtimes = $rpm->get_tag(RPMTAG_FILEMTIMES, true);
if (!is_null($basenames))
{
	echo "<h2>Files</h2>\n";
	echo "<table class=\"table-small table-bordered table-striped\">\n";
	echo "<tbody class=\"mono text-break\">\n";
	foreach ($basenames as $key => $name)
	{
		$name = $dirnames[$dirindexes[$key]] . $name;
		echo "<tr><td>";
		echo $rpm->perm_string($modes[$key]);
		echo "&nbsp;";
		echo str_replace(" ", "&nbsp;", sprintf("%10u ", $sizes[$key]));
		echo usertime($mtimes[$key]);
		echo "&nbsp;";
		echo htmlspecialchars($name);
		if ($links[$key] != '')
		{
			echo " -&gt; ";
			echo htmlspecialchars($links[$key]);
		}
		echo "</td></tr>\n";
	}
	echo "</tbody>\n";
	echo "</table>\n";
}
?>

<?php
$texts = $rpm->get_tag(RPMTAG_CHANGELOGTEXT, true);
$names = $rpm->get_tag(RPMTAG_CHANGELOGNAME, true);
$time = $rpm->get_tag(RPMTAG_CHANGELOGTIME, true);
if (!is_null($texts))
{
	echo "<h2>Changelog</h2>\n";
	echo "<div class=\"alert\">\n";
	echo "<div id=\"changelog\">\n";
	echo "<pre>\n";
	foreach ($texts as $key => $text)
	{
		echo '<span class="bold">* ';
		echo usertime($time[$key], 'ddd MMM DD YYYY');
		echo "</span> - ";
		echo htmlspecialchars($names[$key]);
		echo "\n";
		echo htmlspecialchars($texts[$key]);
		echo "\n";
		echo "\n";
	}
	echo "</pre>\n";
	echo "</div>\n";
	echo "</div>\n";
}
?>


</div>
</div>
</div>
</div>
</div>

<p></p>
<p></p>

<div style="text-align:center">
<p>
<a href="."> <img src="../../images/home1.png" width="180" height="60" style="border:0" alt="Back" /></a>
</p>
</div>

<script type="text/javascript" charset="UTF-8" src="/tippy/tippy.min.js"></script>
<script type="text/javascript" charset="UTF-8">
<?php gen_linktitles(); ?>
<!-- tippy('.tippybtn'); --!>
</script>


</body>
</html>
