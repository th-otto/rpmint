<?php
/*
session_start();
$target = "all";
$platform = "all";
if ($_SERVER['REQUEST_METHOD'] == 'POST')
{
	$_SESSION['target'] = $_POST['target'];
	$_SESSION['platform'] = $_POST['platform'];
	header('Location: ' . $_SERVER['PHP_SELF']);
	exit();
}
if (isset($_SESSION['target']))
{
	$target = $_SESSION['target'];
	$platform = $_SESSION['platform'];
	$_COOKIE['target'] = "$target; SameSite=Strict";
	$_COOKIE['platform'] = "$platform; SameSite=Strict";
}
include('mintvars.php');
include('functions.php');
if (isset($_COOKIE['target']))
	$target = $_COOKIE['target'];
if (!array_key_exists($target, $targets))
	$target = "all";
if (isset($_COOKIE['platform']))
	$platform = $_COOKIE['platform'];
if (!array_key_exists($platform, $platforms))
	$platform = "all";
*/
include('mintvars.php');
include('functions.php');
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
<title>m68k-atari-mint cross-tools</title>
<meta name="keywords" content="ORCS, CAT, GC, PBEM, PBM, GC-Ork, GCORK, ARAnyM, UDO, EmuTOS, GCC" />
<link rel="stylesheet" type="text/css" href="home.css" />
<link rel="stylesheet" type="text/css" href="tippy/tippy.css" />
<script type="text/javascript" src="moment.min.js" charset="UTF-8"></script>
<script type="text/javascript" src="functions.js" charset="UTF-8"></script>
</head>

<?php

include('packages.php');

$gccver = 'gcc950';


?>

<body>
<h1>m68k-atari-mint cross-tools</h1>

<div><p>
(Some of the text on this page was copied/pasted from Vincent Rivi&#xe8;re's website, 
with his permission.)
</p><br />

<p>
You will find here <code>gcc</code>, <code>g++</code>, <code>as</code>, <code>ld</code>,
and other tools configured to produce executables for the Atari ST.
It means that you can use all the latest C++ features, such as templates,
exceptions, STL, as well as inline assembly, to build software which will run on your old Atari ST.
</p>

<p>
The original sources are provided, as well as the patches and the build scripts.
It would be easy to recompile them on any operating system already supporting the GNU tools.<br />
Feel free to redistribute, recompile, and improve the packages,
with respect to their own licenses.
</p>

<p>&nbsp;</p>

<p><span class="important">Important Note for the mintelf toolchains:</span><br />
<img src="images/newbutton.png" width="60" height="40" alt="New" />
All the elf toolchains have now been updated to produce the new PRG+ELF executable format,
which finally makes almost all elf features available. This requires binutils >= 2.41.
If you have previously been using the mintelf toolchains, you should also update all
libraries. They also now produce dwarf-2 debug information by default.

</div>

<hr />

<h1>Quickstart for Windows</h1>
<ol>
<li>Install <a href="http://www.cygwin.com/" <?php echo $href_target ?>>Cygwin 32-bit</a>.
This will provide you a full UNIX-like environment necessary for running the GNU tools.</li>
<li>Install the following packages, using the Cygwin setup program: <b>libmpc3</b>.</li>
<li>Download and install <?php gen_link($download_dir . 'm68k-atari-mint-base-20200501-cygwin32.tar.xz', 'm68k-atari-mint-base-20200501-cygwin32.tar.xz') ?> (~71 MB).</li>
<li>Now you can use any tool prefixed by <code>m68k-atari-mint-</code>,
such as <code>m68k-atari-mint-gcc</code>, <code>m68k-atari-mint-g++</code>,
and even read the man pages.</li>
</ol>

<p>Alternatively, you can also use MinGW:</p>

<ol>
<li>Install <a href="http://www.msys2.org/"<?php echo $href_target ?>>MSYS2/MinGW</a>.</li>
<li>From the list below, install the mingw packages for at least
<ol>
<li>binutils</li>
<li>gcc</li>
<li>mintlib</li>
<li>fdlibm</li>
<li>gemlib</li>
</ol></li>
</ol>

<p>Note: the binutils and gcc packages were built with a prefix of /mingw32. If you are
using an older installation using MSYS from <a href="http://www.mingw.org/"<?php echo $href_target ?>>mingw.org</a>
you should extract them by using <br />
<code>tar -C /mingw --strip-components=1 -xf &lt;archive&gt;</code>
</p>

<p>&nbsp;</p>

<p>
The cygwin packages were built on a recent system (cygwin dll 2.10.0). Should there be problems,
you may have to upgrade your version, or recompile it yourself.</p>

<p>Note: On cygwin, sometimes tar fails to extract symlinks. Although cygwin
supports symlinks on a NTFS filesystem, that filesystem cannot create links
to non-existant files. Depending on whether the original file or link appears
first in the archive, that might fail. Just extracting the same archive again
should fix that.
</p>

<h1>Notes for linux:</h1>

<p>
The linux packages were built on openSUSE tumbleweed (kernel 6.1.3, glibc 2.36). They should
work on other linux distros too, but will require at least glibc 2.14.</p>

<p>&nbsp;</p>

<p>
Everything is installed in <code>/usr/m68k-atari-mint</code> and <code>/usr/lib/gcc/m68k-atari-mint</code>.<br />
If you want to completely uninstall the tools, you just have
to remove these directories.</p>

<h1>Notes for macOS:</h1>

<p>
The macOS packages were built on macOS 10.13 (High Sierra), with a deployment target of 10.9 (Mavericks).
</p>

<p>
Some of the packages (binutils, gcc &amp; mintbin) are now also available as universal x86_64/arm64 binaries.
Those are build using the same scripts as provided here, but are run in a github runner. The whole repo for these
script is available <a href="https://github.com/th-otto/crossmint/" title="crossmint">here</a>. The resulting binaries
are available <a href="snapshots/crossmint/macos" title="macos">here</a>.
</p>

<p>
Everything is installed in <code>/opt/crossmint</code>.<br />
If you want to completely uninstall the tools, you just have
to remove this directory.</p>

<p>&nbsp;</p>

<p>&nbsp;</p>

<!--
<p>&nbsp;</p>

<p><span class="important">Important Note for the native compilers:</span><br />
Unlike Miro's gcc 4.6.4 compiler toolchain, all native compilers (even the ColdFire version)
will produce m68k code by default. This was done since for each package with libraries,
there is only one version that contains all 3 flavours (68000, 68020-60 and cf).
Configuring the toolchain to produce eg. ColdFire code by default would mean
that there would have been 3 versions of them, because the directory layout has to
be different. That means you have to explicitly specify -mcpu=5475 when using the native ColdFire version,
if you want to produce ColdFire code.
</p>
-->

<p>&nbsp;</p>
<!--
<a name='basicpackages'></a>
<form action= "<?php echo $_SERVER['PHP_SELF'] . '#basicpackages'; ?>" method ="POST">
<p>Show Target:
<select name="target" onchange="submit();">
<?php
foreach ($targets as $k => $t)
{
	echo "<option value =\"$k\"";
	if ($k == $target)
		echo " selected";
	echo ">" . $t['display'] . "</option>\n";
}
?>
</select>
Platforms:
<select name="platform" onchange="submit();">
<?php
foreach ($platforms as $k => $t)
{
	echo "<option value =\"$k\"";
	if ($k == $platform)
		echo " selected";
	echo ">" . $t['display'] . "</option>\n";
}
?>
</select>
<input type ="hidden" name="submitted" value="true"><br />
</p></form>
-->

<h1>Basic packages</h1>

<p>
Some of the build scripts use a script with common functions,
which is available <a href="<?php echo $download_dir ?>functions.sh">here</a>.
</p>

<p>&nbsp;</p>

<table border="1" cellpadding="2" cellspacing="0">

<tr>
<th>
Component
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

function gen_baselinks($package, string $os, string $cpu)
{
	global $basepackages;
	global $platforms;
	global $download_dir;
	global $gccver;
	
	$fdate = '';
	if ($os === 'atari')
	{
		$fbin = '';
		$fos = $cpu;
	} else
	{
		$fbin = '-bin';
		if ($os === 'macos64')
			$fos = '-' . 'macos';
		else
			$fos = '-' . $os;
		if (isset($package['date']))
			$fdate = '-' . $package['date'];
	}

	$name = $package['name'];
	if (substr($name, 0, 3) === "gcc")
		$name = "gcc";

	echo '<td class="sourcelink">';
	/* gdb is currently only available for elf */
	if ($name !== "gdb")
	{
		$filename = $download_dir . $name . '-' . $package['version'] . '-mint' . $fdate . $fbin . $fos . '.tar.xz';
		$text = $name . '-' . $package['version'] . '-mint' . $fbin . $fos . '.tar.xz';
		gen_link($filename, $text);
		if ($package['fortran'])
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mint' . $fdate . '-fortran' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mint' . '-fortran' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		if ($package['D'] && ($os === 'linux32' || $os === 'linux64'))
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mint' . $fdate . '-d' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mint' . '-d' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		if ($package['ada'] && ($os === 'linux32' || $os === 'linux64'))
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mint' . $fdate . '-ada' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mint' . '-ada' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		if ($package['m2'] && ($os === 'linux32' || $os === 'linux64'))
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mint' . $fdate . '-m2' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mint' . '-m2' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
	}

	if ($package['elf'] && $basepackages[$gccver][$os])
	{
		$filename = $download_dir . $name . '-' . $package['version'] . '-mintelf' . $fdate . $fbin . $fos . '.tar.xz';
		$text = $name . '-' . $package['version'] . '-mintelf' . $fbin . $fos . '.tar.xz';
		gen_link($filename, $text);
		if ($package['fortran'])
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mintelf' . $fdate . '-fortran' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mintelf' . '-fortran' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		if ($package['D'] && ($os === 'linux32' || $os === 'linux64'))
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mintelf' . $fdate . '-d' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mintelf' . '-d' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		if ($package['ada'] && ($os === 'linux32' || $os === 'linux64'))
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mintelf' . $fdate . '-ada' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mintelf' . '-ada' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
		if ($package['m2'] && ($os === 'linux32' || $os === 'linux64'))
		{
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
			echo '<tr><td></td><td></td><td class="sourcelink">';
			$filename = $download_dir . $name . '-' . $package['version'] . '-mintelf' . $fdate . '-m2' . $fos . '.tar.xz';
			$text = $name . '-' . $package['version'] . '-mintelf' . '-m2' . $fos . '.tar.xz';
			gen_link($filename, $text);
		}
	}
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}


foreach ($basepackages as $key => $package)
{
	echo '<tr id="' . $key . '">' . "\n";
	echo '<td>';
	$name = $package['name'];
	if (substr($name, 0, 3) === "gcc")
		$name = "gcc";
	$title = isset($package['title']) ? $package['title'] : $name;
	echo '<a href="' . $package['upstream'] . '"' . $href_target . '>' . $title . "</a>\n";
	echo '<br />';
	echo last_changetime($name);
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
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc">GitHub repository:</td>' . "\n";
		echo '<td class="sourcelink">';
		echo '<a href="' . $package['repo'];
		if (isset($package['branch']))
			echo '/tree/' . $package['branch'];
		echo '"' . $href_target . '>';
		$repo = str_replace('https://github.com/', '', $package['repo']);
		echo $repo;
		echo '</a>';
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}

	if (isset($package['source']))
	{
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc">Original sources:</td>';
		echo '<td class="sourcelink">';
		$source = $package['source'];
		$source = str_replace('%{name}', $name, $source);
		$source = str_replace('%{version}', $package['version'], $source);
		echo '<a class="archive" href="' . $source . '">' . basename($source) . '</a>';
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['patch'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc">MiNT patch:</td>' . "\n";
		echo '<td class="sourcelink">' . "\n";
		$filename = $download_dir . $name . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.tar.xz';
		$text = $name . '-' . $package['version'] . '-mint.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['patchcomment']))
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc"></td>' . "\n";
		echo '<td class="sourcelink" colspan="2">' . $package['patchcomment'] . '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['script'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc">Build script:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $name . '-' . $package['version'];
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-build.sh';
		$text = $name . '-' . $package['version'] . '-build.sh';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['crossscript'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc">Build script:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . 'cross-' . $name . '-' . $package['version'];
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-build.sh';
		$text = 'cross-' . $name . '-' . $package['version'] . '-build.sh';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['doc']) && $package['doc'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc">Documentation:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $name . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-doc.tar.xz';
		$text = $name . '-' . $package['version'] . '-doc.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	foreach (array('cygwin32', 'cygwin64', 'mingw32', 'mingw64', 'linux64', 'linux32', 'macos64', 'atari') as $os)
	{
		if (isset($package[$os]) && $package[$os] && ($platform == $os || $platform == 'all'))
		{
			echo '<tr>' . "\n";
			echo '<td class="icon"><img src="images/' . $platforms[$os]['image'] . '" width="32" height="32" alt="' . $platforms[$os]['display'] . '"></img></td>' . "\n";
			echo '<td class="linkdesc">' . $platforms[$os]['display'] . ' Package:</td>' . "\n";
			
			gen_baselinks($package, $os, "-000");
			
			if ($os === 'atari')
			{
				echo '<tr><td></td><td></td>';
				gen_baselinks($package, $os, "-020");
				echo '<tr><td></td><td></td>';
				gen_baselinks($package, $os, "-v4e");
			}
		}
	}
		
	echo '</table></td>' . "\n";

	echo '<td>';
	if (isset($package['comment']))
		echo $package['comment'];
	echo '</td>' . "\n";
	
	echo '</tr>' . "\n\n\n";
}

?>

</table>

<!--

<h1>Complete toolchains</h1>

<p>These archives are just repackaged from the packages above, and some packages below.
Particularly, they contain the packages for binutils, GCC, mintbin, gemlib, fdlibm,
mintlib, and cflib.</p>

<p>&nbsp;</p>

<table border="1" cellpadding="2" cellspacing="0">

<?php

$package = $basepackages[$gccver];
$basename = 'm68k-atari-mint-base';
if (isset($package['date']))
	$basename .= '-' . $package['date'];
if ($package['cygwin32'] && ($platform == 'cygwin32' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/' . $platforms['cygwin32']['image'] . '" width="32" height="32" alt="' . $platforms['cygwin32']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">Cygwin32 Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-cygwin32.tar.xz';
	$text = $basename . '-cygwin32.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
if ($package['cygwin64'] && ($platform == 'cygwin64' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/' . $platforms['cygwin64']['image'] . '" width="32" height="32" alt="' . $platforms['cygwin64']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">Cygwin64 Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-cygwin64.tar.xz';
	$text = $basename . '-cygwin64.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
if ($package['mingw32'] && ($platform == 'mingw32' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/' . $platforms['mingw32']['image'] . '" width="32" height="32" alt="' . $platforms['mingw32']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">MinGW Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-mingw32.tar.xz';
	$text = $basename . '-mingw32.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
if ($package['mingw64'] && ($platform == 'mingw64' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/' . $platforms['mingw64']['image'] . '" width="32" height="32" alt="' . $platforms['mingw64']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">MinGW Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-mingw64.tar.xz';
	$text = $basename . '-mingw64.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
if ($package['linux64'] && ($platform == 'linux64' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/' . $platforms['linux64']['image'] . '" width="32" height="32" alt="' . $platforms['linux64']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">Linux64 Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-linux64.tar.xz';
	$text = $basename . '-linux64.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
if ($package['linux32'] && ($platform == 'linux32' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/' . $platforms['linux32']['image'] . '" width="32" height="32" alt="' . $platforms['linux32']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">Linux32 Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-linux32.tar.xz';
	$text = $basename . '-linux32.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
if ($package['macos64'] && ($platform == 'macos64' || $platform == 'all'))
{
	echo '<tr>' . "\n";
	echo '<td class="icon"><img src="images/os-macos.png" width="32" height="32" alt="' . $platforms['macos64']['display'] . '"></img></td>' . "\n";
	echo '<td class="linkdesc">MacOSX Archive:</td>' . "\n";
	echo '<td class="sourcelink">';
	$filename = $download_dir . $basename . '-macos.tar.xz';
	$text = $basename . '-macos.tar.xz';
	gen_link($filename, $text);
	echo '</td>' . "\n";
	echo '</tr>' . "\n";
}
?>
</tr>

</table>

-->


<h1>Library packages</h1>

<p>Note that these packages only contain atari/mint specific files, so there is only one
package of them for all host systems. They have all been built and packaged on linux though
(with a prefix of /usr), so to install them for eg. MinGW you should unpack them using <br />
<code>tar -C &lt;your-install-dir&gt; --strip-components=1 -xf &lt;archive&gt;</code>.
</p>

<p>All of these libraries have been compiled with gcc 7.x, but they can be used with other versions, too.
Also, they all have been compiled for the elf toolchain. Most of these were compiled with -flto (link-time-optimization),
a feature that is not available for a.out libraries. For some (notably mintlib) this is not yet possible.
</p>

<p>&nbsp;</p>

<p>For packages that also build binaries, the *-dev packages will have
executables in <code>&lt;sys-root&gt;/usr/bin</code> that were
compiled for 68k.</p>
<p>&nbsp;</p>
<p>For native installation, there will also be *-bin
packages for other machines. <span class="important">Do not install these on
a cross-development environment</span>(at least not to your usual installation
directory), as this may overwrite your system binaries.</p>
<p>They are meant
to be installed in a MiNT environment, and therefore were packaged with paths
like <code>/usr/bin</code>. In general, the binaries won't be of much use
in a cross-development installation.
</p>

<p>&nbsp;</p>

<table border="1" cellpadding="2" cellspacing="0">

<tr>
<th>
Component
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

foreach ($libpackages as $package)
{
	echo '<tr id="' . $package['name'] . '">' . "\n";
	echo '<td>';
	$title = isset($package['title']) ? $package['title'] : $package['name'];
	echo '<a href="' . $package['upstream'] . '"' . $href_target . '>' . $title . "</a>";
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
		echo '<td class="linkdesc">GitHub repository:</td>' . "\n";
		echo '<td class="sourcelink">';
		echo '<a href="' . $package['repo'];
		if (isset($package['branch']))
			echo '/tree/' . $package['branch'];
		echo '"' . $href_target . '>';
		$repo = str_replace('https://github.com/', '', $package['repo']);
		echo $repo;
		echo '</a>';
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}

	if (isset($package['source']))
	{
		$source = $package['source'];
		$source = str_replace('%{name}', $package['name'], $source);
		$source = str_replace('%{version}', $package['version'], $source);
	} else
	{
		$source = $download_dir . $package['name'] . '-' . $package['version'] . '.tar.xz';
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
	
	if ($package['patch'])
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">MiNT patch:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint.tar.xz';
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
	
	if ($package['script'])
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Build script:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'];
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-build.sh';
		$text = $package['name'] . '-' . $package['version'] . '-build.sh';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['doc']) && $package['doc'])
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Documentation:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-doc.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-doc.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['dev']) && $package['dev'])
	{
		if (1)
		{
			echo '<tr>' . "\n";
			echo '<td class="linkdesc">Devel Package:</td>' . "\n";
			echo '<td class="sourcelink">';
			echo '<table><tr><td>';
			if (isset($package['atari']) && $package['atari'])
			{
				echo '<img class="smallicon" src="images/' . $platforms['atari']['image'] . '" width="16" height="16" alt="Atari"></img>';
			}
			echo '</td><td>' . "\n";
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-dev.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mint.tar.xz';
			gen_link($filename, $text);
			echo '</td></tr></table>';
			echo '</td></tr>' . "\n";
		}
		if (!isset($package['noelf']))
		{
			echo '<tr><td></td>';
			echo '<td class="sourcelink">';
			echo '<table><tr><td>';
			if (isset($package['atari']) && $package['atari'])
			{
				echo '<img class="smallicon" src="images/' . $platforms['atari']['image'] . '" width="16" height="16" alt="Atari"></img>' . "\n";
			}
			echo '</td><td>';
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .='-' . $package['date'];
			$filename .= '-dev.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf.tar.xz';
			gen_link($filename, $text);
			echo '</td></tr></table>';
			echo '</td></tr>' . "\n";
		}
		if (isset($package['amiga']) && $package['amiga'])
		{
			echo '<tr><td></td>';
			echo '<td class="sourcelink">';
			echo '<table><tr><td>';
			echo '<img class="smallicon" src="images/' . $platforms['amiga']['image'] . '" width="16" height="16" alt="Amiga"></img>' . "\n";
			echo '</td><td>';
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-amigaos';
			if (isset($package['date']))
				$filename .='-' . $package['date'];
			$filename .= '-dev.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-amigaos.tar.xz';
			gen_link($filename, $text);
			echo '</td></tr></table>';
			echo '</td></tr>' . "\n";
		}
		if (isset($package['rpm']) && $package['rpm'] !== '')
		{
			echo '<tr><td></td>';
			echo '<td class="sourcelink">';
			echo '<table><tr><td>';
			echo '<img class="smallicon" src="images/rpm.png" width="16" height="16" alt="RPM"></img>' . "\n";
			echo '</td><td>';
			$filename = $rpm_dir . 'cross-mint-' . $package['name'] . (!isset($package['bin']) || !$package['bin'] ? '-devel' : '') . '-' . $package['version'] . '-' . $package['rpm'] . '.noarch.rpm';
			$text = $package['name'] . '-' . $package['version'] . '.rpm';
			gen_link($filename, $text);
			echo '</td></tr></table>';
			echo '</td></tr>' . "\n";
		}
	}
	
	if (isset($package['bin']) && $package['bin'])
	{
		if (1)
		{
			echo '<tr>' . "\n";
			echo '<td class="linkdesc">Binary Package:</td>' . "\n";
			echo '<td class="sourcelink">';
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-000.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-000.tar.xz';
			gen_link($filename, $text);
			echo '</td>' . "\n";
			echo '<td class="sourcelink">';
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
		}
		if (1)
		{
			echo '<tr>' . "\n";
			echo '<td class="linkdesc"></td>' . "\n";
			echo '<td class="sourcelink">';
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-020.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-020.tar.xz';
			gen_link($filename, $text);
			echo '</td>' . "\n";
			echo '<td class="sourcelink">';
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
		}
		if (1)
		{
			echo '<tr>' . "\n";
			echo '<td class="linkdesc"></td>' . "\n";
			echo '<td class="sourcelink">';
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-v4e.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-v4e.tar.xz';
			gen_link($filename, $text);
			echo '</td>' . "\n";
			echo '<td class="sourcelink">';
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
		}
		if (isset($package['rpm']) && $package['rpm'] !== '')
		{
			echo '<tr><td></td>';
			echo '<td class="sourcelink">';
			echo '<table><tr><td>';
			echo '<img class="smallicon" src="images/rpm.png" width="16" height="16" alt="RPM"></img>' . "\n";
			echo '</td><td>';
			$filename = $rpm_dir . 'cross-mint-' . $package['name'] . '-' . $package['version'] . '-' . $package['rpm'] . '.noarch.rpm';
			$text = $package['name'] . '-' . $package['version'] . '.rpm';
			gen_link($filename, $text);
			echo '</td></tr></table>';
			echo '</td>' . "\n";
			echo '<td class="sourcelink">';
			echo '</td>' . "\n";
			echo '</tr>' . "\n";
		}
	}
	
	if (isset($package['noarch']) && $package['noarch'])
	{
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-noarch.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-noarch.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '<td class="sourcelink">';
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

<h1>Known Bugs</h1>
<ul>
<li>Due to lack of support from MiNT, some applications that rely on mmap()
may not always work. Sometimes fallback implementations using malloc() are
used, but this has not been tested for all cases.</li>

<li>Due to a missing posix-compliant pthread lib for MiNT, some applications
that rely on it may not always work.</li>

<li>Some larger applications that use shared libraries to load extensions may not be fully functional.
This notably applies to Perl and Python.
</li>

</ul>

<p></p>

<h1>Changelog</h1>
<ul>
<li>2017/10/18 Binutils archives for native compilation have been added</li>

<li>2017/10/18 Package libiconv added</li>

<li>2017/10/18 Package m4 added</li>

<li>2017/10/18 Package flex added</li>

<li>2017/10/18 Package bison added</li>

<li>2017/10/19 Package expat added</li>

<li>2017/10/19 Package openssl updated</li>

<li>2017/10/19 Package libidn2 added</li>

<li>2017/10/19 Package libssh2 added</li>

<li>2017/10/19 Package libnghttp2 added</li>

<li>2017/10/19 Package libxml2 added</li>

<li>2017/10/19 Package libmetalink added</li>

<li>2017/10/19 Package libpsl added</li>

<li>2017/10/19 Package libunistring added</li>

<li>2017/10/19 Package curl added</li>

<li>2017/10/20 Package freetype2 added</li>

<li>2017/10/20 Package c-ares added</li>

<li>2017/10/20 Package jpeg8d added</li>

<li>2017/10/20 Package Hermes added</li>

<li>2017/10/21 Package gzip added</li>

<li>2017/10/21 Package grep added</li>

<li>2017/10/21 Package ctris added</li>

<li>2017/10/21 Package dhcp added</li>

<li>2017/10/22 Package gawk added</li>

<li>2017/10/22 Package ncurses updated; it was missing the database</li>

<li>2017/10/23 Package file added</li>

<li>2017/10/23 Package diffutils added</li>

<li>2017/10/23 Package findutils added</li>

<li>2017/10/23 Package coreutils added</li>

<li>2017/10/24 Package bash added</li>

<li>2017/10/24 Package make added</li>

<li>2017/10/24 Package patch added</li>

<li>2017/10/26 Package groff added</li>

<li>2018/02/15 Update binutils to version 2.30</li>

<li>2018/02/15 Update GCC to version 7.3</li>

<li>2018/02/17 Add cross-compiler for MinGW host</li>

<li>2018/03/08 Package git added</li>

<li>2018/03/10 Package ca-certificates added</li>

<li>2018/03/10 Package gdbm added</li>

<li>2018/03/11 Package db added</li>

<li>2018/03/13 Package perl added</li>

<li>2018/03/13 Package autoconf added</li>

<li>2018/03/13 Package autoconf-archives added</li>

<li>2018/03/14 Package automake added</li>

<li>2018/03/14 Package beecrypt6 added</li>

<li>2018/03/14 Package lua added</li>

<li>2018/03/15 Package popt added</li>

<li>2018/03/16 Package rpm added</li>

<li>2018/03/19 Package rhash added</li>

<li>2018/03/19 Package libarchive added</li>

<li>2018/03/20 Package elfutils added</li>

<li>2018/03/20 Package libuv added</li>

<li>2018/03/21 Package cmake added</li>

<li>2018/03/23 Package libsolv added</li>

<li>2018/03/24 Package python2 added</li>

<li>2018/03/25 Package python3 added</li>

<li>2018/03/26 Package libffi added</li>

<li>2018/03/27 Package libgpg-error added</li>

<li>2018/03/27 Package libassuan added</li>

<li>2018/04/02 Package gettext added</li>

<li>2018/04/02 Rebuild libiconv with --enable-extra-encodings</li>

<li>2018/04/02 Update libgpg-error with missing executable</li>

<li>2018/04/02 Package libksba added</li>

<li>2018/04/02 Package libgrypt added</li>

<li>2018/04/10 Update MiNTLib</li>

<li>2018/04/10 Update GCC to version 7.3.1</li>

<li>2018/05/04 Update GCC to version 8.1.0</li>

<li>2018/07/17 Update binutils to 2.31</li>

<li>2018/07/24 Update libpng to 1.6.34</li>

<li>2018/08/17 Add WinDom 1.21.3 (needed by zView)</li>

<li>2018/08/18 Package giflib added</li>

<li>2018/08/18 Package libexif added</li>

<li>2018/08/18 Package tiff added</li>

<li>2018/08/31 Update GCC to version 8.2.0</li>

<li>2018/11/17 Update GCC to version 8.2.1</li>

<li>2018/11/23 Update binutils to version 2.31.1</li>

<li>2018/11/24 Recompile most packages</li>

<li>2018/11/24 Update gzip to version 1.9</li>

<li>2019/02/23 Update GCC to version 8.3.0</li>

<li>2019/02/23 Update binutils to version 2.32</li>

<li>2019/02/24 Package isl added</li>

<li>2019/02/24 Update mpfr to 4.0.2</li>

<li>2019/02/24 Update mpc to 1.1.0</li>

<li>2019/02/24 Add scripts to build native binutils/compiler</li>

<li>2019/02/25 Update GCC 7 to version 7.4.0</li>

<li>2019/02/27 Fortran backend added for all platforms</li>

<li>2019/02/27 Package fdlibm added</li>

<li>2019/03/19 Package libmikmod added</li>

<li>2019/03/19 Package libogg added</li>

<li>2019/03/19 Package flac added</li>

<li>2019/03/19 Package libvorbis added</li>

<li>2019/03/19 Package vorbis-tools added</li>

<li>2019/03/20 Package SDL_mixer added</li>

<li>2019/03/21 Package SDL_image added</li>

<li>2019/03/21 Package SDL_ttf added</li>

<li>2019/03/21 Package SDL_net added</li>

<li>2019/03/22 Update SDL from upstream</li>

<li>2019/03/23 Package povray 3.6 added</li>

<li>2019/03/23 Package smpeg added</li>

<li>2019/03/23 Rebuild SDL_mixer with smpeg support</li>

<li>2019/03/23 Package mpg123 added</li>

<li>2019/03/23 Update SDL_mixer to 1.2.13</li>

<li>2019/03/23 Update pml library</li>

<li>2019/03/27 Package libtheora added</li>

<li>2019/04/02 Some libraries are now compiled for amigaos</li>

<li>2019/04/10 Update fdlibm</li>

<li>2019/04/19 Update git to 2.21</li>

<li>2019/05/06 Update librhash to 1.3.8</li>

<li>2019/05/10 Update bash to patchlevel 4.4.23
(should solve a problem with hanging configure scripts)
</li>

<li>2019/06/07 Update GCC to version 9.1.1</li>

<li>2019/07/14 Added ping command</li>

<li>2019/08/03 Update tiff to 4.0.10</li>

<li>2019/08/03 Update xz to 5.2.4</li>

<li>2019/08/14 Update fdlibm</li>

<li>2019/08/14 Package libmad added</li>

<li>2019/08/21 Fix a bug in windom libraries when scanning the menu for keyboard shortcuts</li>

<li>2019/08/23 Rebuild gcc for linux with static version of isl 0.18</li>

<li>2019/08/23 Update fdlibm</li>

<li>2019/09/16 Package gnucobol added</li>

<li>2019/09/23 Package zstd added</li>

<li>2019/09/28 Package dosfstools added</li>

<li>2019/11/12 Fix for a c99-ism in SDL</li>

<li>2020/01/01 Update gcc 7.x to 7.5.0</li>

<li>2020/01/02 Update binutils to 2.33.1</li>

<li>2020/01/02 Update gcc to version 9.2.0</li>

<li>2020/01/03 Update fdlibm</li>

<li>2020/01/08 Update fdlibm</li>

<li>2020/04/29 Update binutils to 2.34</li>

<li>2020/05/01 Update gcc 8.x to 8.4.1</li>

<li>2020/05/02 Update gcc to version 9.3.1</li>

<li>2020/05/05 Package opkg added</li>

<li>2020/05/20 Update GCC to version 10.1.0</li>

<li>2020/07/13 Handle process (S_IFMEM) files in findutils and coreutils</li>

<li>2020/07/13 Package tree added</li>

<li>2020/08/01 Package libxmp added</li>

<li>2020/08/01 Package asap added</li>

<li>2020/08/23 Package p7zip added</li>

<li>2020/08/24 Package netpbm added</li>

<li>2020/08/24 Recompile bash without libiconv</li>

<li>2020/08/26 Package mksh added</li>

<li>2020/08/30 Update rpm to version 4.15.1</li>

<li>2020/09/02 Package cpio added</li>

<li>2020/09/02 Update libexif to version 0.6.22</li>

<li>2020/09/02 Update rpm to version 4.15.1</li>

<li>2020/09/05 Update coreutils to version 8.32</li>

<li>2020/09/06 Update bison to version 3.6.4</li>

<li>2020/09/10 Fix a bug in zip/unzip storing wrong filetype for symlinks</li>

<li>2020/12/23 Support BZIP2 in unzip</li>

<li>2021/01/07 Update bzip to 1.07</li>

<li>2021/01/07 Update bzip to 1.08</li>

<li>2022/08/02 Package libwebp added</li>

<li>2022/08/05 Package pth added</li>

<li>2022/08/06 Package libyuv added</li>

<li>2022/08/06 Package openh264 added</li>

<li>2022/08/06 Package fdk-aac added</li>

<li>2022/08/06 Package mp4v2 added</li>

<li>2022/08/18 Update gcc 10.x to 10.2.0</li>

<li>2022/08/20 Update gcc 10.x to 10.4.0</li>

<li>2022/09/11 Update binutils to 2.39</li>

<li>2022/09/14 Update zlib to 1.2.12</li>

<li>2022/09/15 Package libsndfile added </li>

<li>2022/09/15 Package zita-resampler added </li>

<li>2022/09/19 Package wolfssl added </li>

<li>2022/09/23 Update openssl to 1.1.1p</li>

<li>2022/10/24 Update wolfssl to 5.5.1</li>

<li>2023/01/11 Move D backend to separate archives</li>

<li>2023/01/24 Add libde265 1.0.9</li>

<li>2023/01/24 Add libheif 1.14.2</li>

<li>2023/02/11 Update fdlibm</li>

<li>2023/02/11 Update gcc to version 12.2.0</li>

<li>2023/02/12 Update gemlib</li>

<li>2023/02/12 Recompile binutils for linux</li>

<li>2023/02/12 Update mintlib</li>

<li>2023/02/24 Update binutils to 2.40</li>

<li>2023/02/26 Update gcc-8 to 8.5.0</li>

<li>2023/02/28 Update opkg to 0.6.1</li>

<li>2023/03/01 Update gmp to 6.2.1</li>

<li>2023/03/01 Update zlib to 1.2.13</li>

<li>2023/03/01 Update libiconv to 1.17</li>

<li>2023/03/02 Recompile ncurses, enabling wide-char versions</li>

<li>2023/03/02 Add mtm 1.2.1</li>

<li>2023/03/02 Update libxml2 to 2.10.3</li>

<li>2023/03/03 Update gcc-9 to 9.5.0</li>

<li>2023/03/23 Update zstd to 1.5.4</li>

<li>2023/03/23 Update tiff to 4.5.0</li>

<li>2023/04/01 Update groff to 1.22.4</li>

<li>2023/04/01 Update tar to 1.34</li>

<li>2023/04/08 Fix SDL library which had only the m68020 version; update to 1.2.16</li>

<li>2023/04/08 Update SDL_image to 1.2.13</li>

<li>2023/04/09 Add man 1.5g</li>

<li>2023/04/10 Add help2man 1.49.3</li>

<li>2023/04/10 Add sed 4.9</li>

<li>2023/04/10 Add traceroute 1.4a5</li>

<li>2023/05/10 Add x3270 4.2ga9</li>

<li>2023/05/11 Add wget 1.21.3</li>

<li>2023/05/32 Provide archives for native gcc 4.6.4</li>

<li>2023/05/22 Add gcc 13.1.0</li>

<li>2023/07/12 pth: fix a crash in pth_cleanup</li>

<li>2023/07/19 gcc4: rebuild with newer libgcc for long-double</li>

<li>2023/07/20 gcc10: rebuild with newer libgcc for long-double</li>

<li>2023/07/22 gcc11: rebuild with newer libgcc for long-double</li>

<li>2023/07/24 gcc12: rebuild with newer libgcc for long-double</li>

<li>2023/07/26 gcc7: rebuild with newer libgcc for long-double</li>

<li>2023/07/29 gcc8: rebuild with newer libgcc for long-double</li>

<li>2023/08/01 gcc9: rebuild with newer libgcc for long-double</li>

<li>2023/08/02 Update gcc 13.x to 13.2.0</li>

<li>2023/08/04 Update zstd to 1.5.5</li>

<li>2023/08/06 Update xz to 5.4.4</li>

<li>2023/08/24 Update ncurses to 6.4</li>

<li>2023/08/27 Update file to 5.45</li>

<li>2023/09/11 Update binutils to 2.41</li>

<li>2023/09/16 Add physfs 3.2.0</li>

<li>2023/09/18 Add x265 3.5</li>

<li>2023/10/04 Add libedit 3.1 & dash 0.5.12</li>

<li>2023/10/14 Update libwebp to 1.3.2</li>

<li>2023/10/16 Add xpdf 4.04</li>

<li>2023/11/03 Add libaacplus 2.0.2</li>

<li>2023/11/03 Add a52dec 0.8.0</li>

<li>2023/11/03 Add pixman 0.42.2</li>

<li>2023/11/03 Add cairo 1.18.0</li>

<li>2023/11/03 Add libaom 3.7.0</li>

<li>2023/11/03 Add opus 1.4</li>

<li>2023/11/03 Add lame 3.100</li>

<li>2023/11/03 Add libvpx 1.3.1</li>

<li>2023/11/03 Add x264 snapshot 20230215</li>

<li>2023/11/03 Add fribidi 1.0.13</li>

<li>2023/11/05 Add graphite2 1.3.14</li>

<li>2023/11/05 Add lcms2 2.15</li>

<li>2023/11/06 Add faad2 2.10.1</li>

<li>2023/11/06 Add ffmpeg 6.0</li>

<li>2023/11/08 Add SDL_gfx 2.0.26</li>

<li>2023/11/15 Update zlib to 1.3</li>

<li>2023/11/28 Update SDL to 1.2.16-git</li>

<li>2023/12/04 Add SDL_sound 1.0.4</li>

<li>2023/12/04 Add sqlite3 3.44.2</li>

<li>2023/12/22 Update libxmp to 4.6.0</li>

<li>2023/12/22 Update SDL to 1.2.16-git-cbe3ea9</li>

<li>2023/12/23 Add FLTK 1.3.9</li>

<li>2023/12/23 Add dillo 3.1-dev</li>

</ul>

<p></p>

<h1>More information</h1>
<p>See <a href="http://vincent.riviere.free.fr/soft/m68k-atari-mint/">Vincent Rivi&#xe8;re's</a>
site for a history of his packages.</p>

<p>
Feel free to <a href="mailto:admin@tho-otto.de">send me your comments</a>!<br /></p>

<p>
<em>Thorsten Otto</em></p>

<h1>Links</h1>
<p>
<b>Vincent Rivi&#xe8;re</b> has made similar scripts available for several years.
His work is available <a href="http://vincent.riviere.free.fr/soft/m68k-atari-mint/"<?php echo $href_target ?>>here</a>.</p>

<p>
<b>Patrice Mandin</b> has done a lot of work for porting GCC and the binutils
to the MiNT platform. His work is available
<a href="http://patrice.mandin.pagesperso-orange.fr/v3/en/patch-utils.html"<?php echo $href_target ?>>here</a>.</p>

<p>
<b>Olivier Landemarre</b> has made his own port of GCC 4.2 to the MiNT platform.
He also has <a href="http://gem.lutece.net/discussion/archives/cat_listedeliens.html"<?php echo $href_target ?>>
a great list of Atari-related stuff</a>.</p>

<p>
<b>Fran&#xe7;ois Le Coat</b> is the author of the
<a href="http://eureka2.12.pagesperso-orange.fr/atari.html"<?php echo $href_target ?>>ATARI Search Engine</a>.</p>

<p>
<b>Thomas Huth</b> is the author of the <a href="http://hatari.tuxfamily.org/"<?php echo $href_target ?>>Hatari</a> ST emulator.
<!--
He has sucessfully recompiled this GCC port on Linux, on his PowerMac G4,
and has successfully compiled <a href="http://emutos.sourceforge.net/"<?php echo $href_target ?>>EmuTOS</a> with it!
-->
</p>
<!--
<p>
<b>Bohdan Milar</b> has (not yet ?) put a link to this page
on <a href="http://cs.atari.org/"<?php echo $href_target ?>>the Czech and Slovak Atari portal</a>.</p>
-->
<p>
<b>Keith Scroggins</b> has ported <a href="http://www.scummvm.org/"<?php echo $href_target ?>>ScummVM</a> to MiNT.
Build instructions are available <a href="http://wiki.scummvm.org/index.php/Compiling_ScummVM/Atari/FreeMiNT"<?php echo $href_target ?>>here</a>.
He also made his own native port of GCC 4.0.1 several years before me; his work is available <a href="http://www.radix.net/~kws/mint/old/"<?php echo $href_target ?>>here</a>.</p>

<p>
<b>Miro Krop&#xe1;&#x010d;ek</b> has compiled the GCC 4.6.4 port for the MiNT host.
That means you can run the latest GCC natively on your Atari/MiNT computer, without cross-compilation!
He also made a nice Makefile for building all the toolchain.
His work is available <a href="http://mikro.atari.org/download.htm"<?php echo $href_target ?>>here</a>.</p>

<p>
<b>Pawe&#x0142; G&#xf3;ralski</b> has ported <a href="http://nokturnal.pl/home/atari/porty_reminiscence"<?php echo $href_target ?>>REminiscence</a>
to Falcon using this compiler. It is an interpreter for Delphine Software games, enabling to play Flashback on Falcon.
He also maintains the <a href="http://bus-error.nokturnal.pl/tiki-list_articles.php"<?php echo $href_target ?>>Bus Error Wiki</a> with a lot of programming tricks using these cross-tools.</p>

<p>
<b>Mark Duckworth</b> has built an RPM package for native MiNT binutils, using the patch available on this page.
He has compiled natively a lot of other RPM packages, his work is available <a href="http://storage.atari-source.org/atari/personal/package_staging/"<?php echo $href_target ?>>here</a>.</p>

<p>
<b>Dominique B&#xe9;r&#xe9;ziat</b> has written <a href="http://pequan.lip6.fr/~bereziat/softs/tos/cross-compilation/"<?php echo $href_target ?>>a tutorial for cross-compiling GEM applications</a>.</p>

<p>
<b>Philipp Donz&#xe9;</b> has built the binaries of an older version of these cross-tools for MacOS X (Intel and PowerPC supported).
His binaries as well as installation instructions are available <a href="http://www.xn--donz-epa.ch/atari/articles/cross-compiler/"<?php echo $href_target ?>>here</a>.</p>

<p>
<b>Rolf Hemmerling</b> has <a href="http://hemmerling.free.fr/doku.php/en/atarist.html"<?php echo $href_target ?>>a nice page about the current Atari resources on the web</a>.</p>

<p>
<b>DML</b> has <a href="http://www.leonik.net/dml/sec_atari.py"<?php echo $href_target ?>>a nice page about Atari and engineering</a>.</p>

<p>
<b>Peter Dassow</b> has <a href="http://www.z80.eu/stsoft.html"<?php echo $href_target ?>>a nice page with a lot of links to ST software</a>.</p>

<p>
<b>George Nakos</b> used the cross-tools for his <a href="http://reboot.atari.org/downloads.html"<?php echo $href_target ?>>raptorBASIC+</a>.</p>

<p>
<b>Jookie</b> uses the cross-tools for developing <a href="http://joo.kie.sk/?page_id=384"<?php echo $href_target ?>>CosmosEx</a> software.
CosmosEx is a hardware extension as small as a floppy drive which brings SD-Card, USB, Ethernet and much more to Atari computers.</p>

<hr />
<div style="text-align:center">Last updated: <?php echo usertime(filemtime($_SERVER['SCRIPT_FILENAME']));?>
<p>
</p>
</div>
<hr />
<div style="text-align:center">
<p>
<a href="index.html"> <img src="images/home1.png" width="180" height="60" style="border:0" alt="Home" /></a>
</p>
</div>

<script type="text/javascript" charset="UTF-8" src="tippy/tippy.min.js"></script>
<script type="text/javascript" charset="UTF-8">
<?php gen_linktitles(); ?>
<!-- tippy('.tippybtn'); -->
</script>

<!--
Build times:
binutils:
	mingw32: 10min
	mingw64: 10min
	cygwin32:  8min
	cygwin64:  6min
	macos:   3min (ld does not have support for the native platform)
	linux:   39sec

gcc 2.95.3:
	linux:   1min15sec

gcc 4.6.4:
	mingw32: 15min
	mingw64: 38min
	cygwin:  19min
	macos:   15min
	linux:   2min30sec
	
gcc 7.2:
	mingw32: 32min
	cygwin:  28min
	macos:   23min
	linux:   3min
	
gcc 7.5:
	mingw32: 68min
	mingw64: 60min
	cygwin32: 36min
	cygwin64: 28min
	macos:   25min
	linux:   3min

gcc 8.1:
	mingw32: 32min
	cygwin32: 38min
	cygwin64: 31min
	macos:   33min
	linux:   3min47sec

gcc 8.2:
	mingw32: 32min
	cygwin32: 39min
	cygwin64: 35min
	macos:   33min
	linux:   3min54sec

gcc 8.5:
	mingw32: 33min
	mingw64: 63min
	cygwin32: 39min
	cygwin64: 35min
	macos:   29min
	linux:   4min12sec

gcc 9.5.0:
	mingw32: 38min
	mingw64: 69min
	cygwin32: 45min
	cygwin64: 42min
	macos:   31min
	linux:   4min12sec

gcc 10.5.0:
	mingw32: 50min
	mingw64: 70min
	cygwin32: 85min
	cygwin64: 88min
	macos:   32min
	linux:   7min48sec

gcc 11.3.0:
	mingw32: 73min
	mingw64: 85min
	cygwin32: 126min
	cygwin64: 116min
	macos:   52min
	linux:   7min28sec

gcc 12.2.0:
	mingw32: 76min
	mingw64: 89min
	cygwin32: 129min
	cygwin64: 129min
	macos:   57min
	linux:   11min8sec

gcc 13.1.0:
	mingw32: 80min
	mingw64: 111min
	cygwin32: 134min
	cygwin64: 143min
	macos:   54min
	linux:   12min40sec

-->
</body>
</html>
