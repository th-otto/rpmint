<?php
include('mintvars.php');
include('functions.php');
$download_dir = 'download/sdl/';
$target = "all";
$platform = "all";
setcookie("target", $target, time() + 3600);
setcookie("platform", $platform, time() + 3600);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
          "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>SDL games</title>
<meta name="keywords" content="ORCS, CAT, GC, PBEM, PBM, GC-Ork, GCORK, ARAnyM, UDO, EmuTOS, GCC" />
<link rel="stylesheet" type="text/css" href="home.css" />
<link rel="stylesheet" type="text/css" href="tippy/tippy.css" />
<script type="text/javascript" src="moment.min.js" charset="UTF-8"></script>
<script type="text/javascript" src="functions.js" charset="UTF-8"></script>
</head>

<?php

include('sdl-packages.php');


?>

<body>
<h1>SDL games</h1>

Always needed:
<ul><li><a href="crossmint.php#SDL">SDL</a></li></ul>

Most games will also need additional libraries:
<ul>
<li><a href="crossmint.php#SDL_mixer">SDL_mixer</a></li>
<li><a href="crossmint.php#SDL_image">SDL_image</a></li>
<li><a href="crossmint.php#SDL_gfx">SDL_gfx</a></li>
<li><a href="crossmint.php#SDL_net">SDL_net</a></li>
<li><a href="crossmint.php#SDL_ttf">SDL_ttf</a></li>
</ul>

Addition libraries needed by the above:
<ul>
<li><a href="crossmint.php#tiff">TIFF</a></li>
<li><a href="crossmint.php#libpng">libpng</a></li>
<li><a href="crossmint.php#zlib">ZLib</a></li>
<li><a href="crossmint.php#jpeg">JPEG</a></li>
<li><a href="crossmint.php#xz">XZ/LZMA</a></li>
<li><a href="crossmint.php#zstd">ZStd</a></li>
<li><a href="crossmint.php#bzip2">BZip2</a></li>
<li><a href="crossmint.php#libwebp">WebP</a></li>
<li><a href="crossmint.php#freetype2">Freetype</a></li>
<li><a href="crossmint.php#flac">FLAC</a></li>
<li><a href="crossmint.php#libvorbis">vorbis</a></li>
<li><a href="crossmint.php#libogg">Ogg</a></li>
<li><a href="crossmint.php#mpg123">mpg123</a></li>
<li><a href="crossmint.php#ldg">LDG</a></li>
</ul>

<hr />

<p>&nbsp;</p>

<h1>Ports</h1>

<p>&nbsp;</p>

<table border="1" cellpadding="2" cellspacing="0">

<tr>
<th>
Game
</th>
<th>
Version
</th>
<th>
Packages
</th>
<th>
Comments
</th>
</tr>

<?php

foreach ($sdlpackages as $package)
{
	echo '<tr id="' . $package['name'] . '">' . "\n";
	echo '<td>';
	$title = isset($package['title']) ? $package['title'] : $package['name'];
	echo '<a href="' . $package['upstream'] . '"' . $target . '>' . $title . "</a>";
	echo '<br />';
	echo last_changetime($package['name']);
	echo "</td>\n";

	echo '<td>';
	$version = $package['version'];
	if (isset($package['patchlevel'])) $version .= $package['patchlevel'];
	echo $version . ' <br />' . (isset($package['date']) ? $package['date'] : '');
	echo "</td>\n";

	echo '<td><table>';

	if (isset($package['repo']))
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Source repository:</td>' . "\n";
		echo '<td class="sourcelink">';
		echo '<a href="' . $package['repo'];
		if (isset($package['branch']))
			echo '/tree/' . $package['branch'];
		echo '"' . $target . '>';
		$repo = str_replace('https://github.com/', '', $package['repo']);
		echo $repo;
		echo '</a>';
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}

	if ($version !== '')
		$version = '-' . $version;
	if (isset($package['source']))
	{
		$source = $package['source'];
		$source = str_replace('%{name}', $package['name'], $source);
		$source = str_replace('%{version}', $package['version'], $source);
	} else
	{
		$source = $download_dir . $package['name'] . $version . '.tar.xz';
	}
	
	if (1)
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Original sources:</td>' . "\n";
		echo '<td class="sourcelink">';
		gen_link($source, basename($source));
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (1)
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Build script:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . $version . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.tar.xz';
		$text = $package['name'] . $version . '-mint.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['patchcomment']))
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc"></td>' . "\n";
		echo '<td class="sourcelink" colspan="2">' . $package['patchcomment'] . '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['doc']) && $package['doc'])
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Documentation:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . $version . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-doc.tar.xz';
		$text = $package['name'] . $version . '-doc.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (1)
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Binary Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . $version;
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin.tar.xz';
		$text = $package['name'] . $version . '-bin.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	echo '</table></td>' . "\n";

	echo '<td>';
	if (isset($package['comment']))
		echo $package['comment'];
	echo '</td>' . "\n";
	
	echo '</tr>' . "\n";
}


?>

</table>

<p></p>

<hr />
<div style="text-align:center">Last updated: <?php echo usertime(filemtime($_SERVER['SCRIPT_FILENAME']));?>
<p>
</p>
<hr />
<div style="text-align:center">
<p>
<a href="index.html"> <img src="images/home1.png" width="180" height="60" style="border:0" alt="Home" /></a>
</p>
</div>

<script type="text/javascript" charset="UTF-8" src="tippy/tippy.min.js"></script>
<script type="text/javascript" charset="UTF-8">
<?php gen_linktitles(); ?>
<!-- tippy('.tippybtn'); --!>
</script>

</body>
</html>
