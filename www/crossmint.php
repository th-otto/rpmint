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

error_reporting(E_ALL & ~E_WARNING);
ini_set("display_errors", 1);
date_default_timezone_set('UTC');

$download_dir = 'download/mint/';

include('functions.php');
include('packages.php');

?>

<body>
<h1>m68k-atari-mint cross-tools</h1>

<div><p>
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
</div>

<hr />

<h1>Quickstart for Windows</h1>
<ol>
<li>Install <a href="http://www.cygwin.com/" <?php echo $target ?>>Cygwin 32-bit</a>.
This will provide you a full UNIX-like environment necessary for running the GNU tools.</li>
<li>Install the following packages, using the Cygwin setup program: <b>libmpc3</b>.</li>
<li>Download and install <?php gen_link($download_dir . 'm68k-atari-mint-base-20171014-cygwin32.tar.xz', 'm68k-atari-mint-base-20171014-cygwin32.tar.xz') ?> (~50 MB).</li>
<li>Now you can use any tool prefixed by <code>m68k-atari-mint-</code>,
such as <code>m68k-atari-mint-gcc</code>, <code>m68k-atari-mint-g++</code>,
and even read the man pages.</li>
</ol>

<p>Alternatively, you can also use MinGW:</p>

<ol>
<li>Install <a href="http://www.msys2.org/"<?php echo $target ?>>MSYS2/MinGW</a>.</li>
<li>From the list below, install the mingw packages for at least
<ol>
<li>binutils</li>
<li>gcc</li>
<li>mintlib</li>
<li>pml</li>
<li>gemlib</li>
</ol></li>
</ol>

<p>Note: the binutils and gcc packages where built with a prefix of /mingw32. If you are
using an older installation using MSYS from <a href="http://www.mingw.org/"<?php echo $target ?>>mingw.org</a>
you should extract them by using <br />
<code>tar -C /mingw --strip-components=1 -xf &lt;archive&gt;</code>
</p>

<p>&nbsp;</p>

<p>
The linux packages were built on openSUSE tumbleweed (kernel 4.13, glibc 2.26). They should
work on other linux distros too, but will require at least glibc 2.14.</p>

<p>&nbsp;</p>

<p>
The cygwin packages where built on a recent system (cygwin dll 2.9.0). Should there be problems,
you may have to upgrade your version, or recompile it yourself.</p>

<p>&nbsp;</p>

<p>
The macOS packages where built on macOS Sierra, with a deployment target of 10.6 (Snow Leopard).
</p>

<p>&nbsp;</p>

<p>
Everything is installed in <code>/usr/m68k-atari-mint</code> and <code>/usr/lib/gcc/m68k-atari-mint</code>.<br />
If you want to completely uninstall the tools, you just have
to remove these directories.</p>

<p>&nbsp;</p>

<p>Note: On cygwin, sometimes tar fails to extract symlinks. Although cygwin
supports symlinks on a NTFS filesystem, that filesystem cannot create links
to non-existant files. Depending on wether the original file or link appears
first in the archive, that might fail. Just extracting the same archive again
should fix that.
</p>

<!--
<p>&nbsp;</p>

<p><span class="important">Important Note for the native compilers:</span><br />
Unlike Miro's gcc 4.6.4 compiler toolchain, all native compilers (even the coldfire version)
will produce m68k code by default. This was done since for each package with libraries,
there is only one version that contains all 3 flavours (68000, 68020-60 and cf).
Configuring the toolchain to produce eg. coldfire code by default would mean
that there would have been 3 versions of them, because the directory layout has to
be different. That means you have to use exclicit -mcpu=5475 when using the native coldire version,
and you want to produce coldfire code.
</p>
-->

<p>&nbsp;</p>

<h1>Basic packages</h1>

<p>
Some of the build scripts use a script with common functions,
which is available <a href="<?php echo $download_dir ?>functions.sh">here</a>.

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

foreach ($basepackages as $package)
{
	echo '<tr>';
	echo '<td>';
	$title = isset($package['title']) ? $package['title'] : $package['name'];
	echo '<a href="' . $package['upstream'] . '"' . $target . '>' . $title . "</a>\n";
	echo '<br />';
	echo last_changetime($package['name']);
	echo "</td>\n";

	echo '<td>';
	echo $package['version'] . ' <br />' . (isset($package['date']) ? $package['date'] : '');
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
		echo '"' . $target . '>';
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
		$source = str_replace('%{name}', $package['name'], $source);
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
		$filename = $download_dir . 'build-' . $package['name'] . '-' . $package['version'];
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.sh';
		$text = 'build-' . $package['name'] . '-' . $package['version'] . '-sh';
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
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-doc.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-doc.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['cygwin32'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-cygwin.ico" width="32" height="32" alt="Cygwin"></img></td>' . "\n";
		echo '<td class="linkdesc">Cygwin Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-cygwin32.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-cygwin32.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'] && $basepackages['gcc720']['cygwin32'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-bin-cygwin32.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-bin-cygwin32.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['cygwin64'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-cygwin.ico" width="32" height="32" alt="Cygwin"></img></td>' . "\n";
		echo '<td class="linkdesc">Cygwin Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-cygwin64.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-cygwin64.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'] && $basepackages['gcc720']['cygwin64'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-bin-cygwin64.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-bin-cygwin64.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['mingw32'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-mingw.ico" width="32" height="32" alt="MinGW"></img></td>' . "\n";
		echo '<td class="linkdesc">MinGW Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-mingw32.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-mingw32.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'] && $basepackages['gcc720']['mingw32'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-bin-mingw32.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-bin-mingw32.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['mingw64'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-mingw.ico" width="32" height="32" alt="MinGW"></img></td>' . "\n";
		echo '<td class="linkdesc">MinGW Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-mingw64.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-mingw64.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'] && $basepackages['gcc720']['mingw64'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= -bin-mingw64.tar.xz;
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-bin-mingw64.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}

	if (!$package['mingw32'] && !$package['mingw64'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-mingw.ico" width="32" height="32" alt="MinGW"></img></td>' . "\n";
		echo '<td class="linkdesc">MinGW Package:</td>' . "\n";
		echo '<td class="sourcelink">(not yet available)</td>' . "\n";
		echo '</tr>';
	}
	
	if ($package['linux64'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-linux.png" width="32" height="32" alt="Linux"></img></td>' . "\n";
		echo '<td class="linkdesc">Linux Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
 		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-linux.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-linux.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-bin-linux.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-bin-linux.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['macos64'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-macos.png" width="32" height="32" alt="MacOSX"></img></td>' . "\n";
		echo '<td class="linkdesc">MacOSX Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-macos.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-macos.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .= '-' . $package['date'];
			$filename .= '-bin-macos.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-bin-macos.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['atari']) && $package['atari'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/os-atari.png" width="32" height="32" alt="Atari" style="background-color: #ffffff"></img></td>' . "\n";
		echo '<td class="linkdesc">Atari Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint-000.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-000.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf-000.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-000.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";

		echo '<tr><td></td><td></td><td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint-020.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-020.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf-020.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-020.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";

		echo '<tr><td></td><td></td><td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint-v4e.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-v4e.tar.xz';
		gen_link($filename, $text);
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
		if ($package['elf'])
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf-v4e.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf-v4e.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
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

<h1>Library packages</h1>

<p>Note that these packages only contain atari/mint specific files, so there is only one
package of them for all host systems. They have all been built and packaged on linux though
(with a prefix of /usr), so to install them for eg. MinGW you should unpack them using <br />
<code>tar -C &lt;your-install-dir&gt; --strip-components=1 -xf &lt;archive&gt;</code>.
</p>

<p>All of these libraries have been compiled with gcc 7.2, but they can be used with other versions, too.
Also, they all have been compiled also for the elf toolchain. Of these, most where compiled with -flto (link-time-optimization),
a feature that is not available for a.out libraries. For some (notably mintlib) this is not yet possible.
</p>

<p>&nbsp;</p>

<p>For packages that also build binaries, the *-dev packages will have
executables in <code>&lt;sys-root&gt;/usr/bin</code> that where
compiled for 68k.</p>
<p>&nbsp;</p>
<p>For native installation, there will also be *-bin
packages for other machines. <span class="important">Do not install these on
a cross-development environment</span>(at least not to your usual installation
directory), as this may overwrite your system binaries.</p>

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
	echo '<tr>' . "\n";
	echo '<td>';
	$title = isset($package['title']) ? $package['title'] : $package['name'];
	echo '<a href="' . $package['upstream'] . '"' . $target . '>' . $title . "</a>";
	echo '<br />';
	echo last_changetime($package['name']);
	echo "</td>\n";

	echo '<td>';
	echo $package['version'] . ' <br />' . (isset($package['date']) ? $package['date'] : '');
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
		echo '"' . $target . '>';
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
		$filename = $download_dir . 'build-' . $package['name'] . '-' . $package['version'];
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.sh';
		$text = 'build-' . $package['name'] . '-' . $package['version'] . '.sh';
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
		echo '<tr>' . "\n";
		echo '<td class="linkdesc">Devel Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-dev.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>' . "\n";
		echo '<tr><td></td><td class="sourcelink">';
		if (!isset($package['noelf']))
		{
			$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mintelf';
			if (isset($package['date']))
				$filename .='-' . $package['date'];
			$filename .= '-dev.tar.xz';
			$text = $package['name'] . '-' . $package['version'] . '-mintelf.tar.xz';
			gen_link($filename, $text);
		}
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if (isset($package['bin']) && $package['bin'])
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
His work is available <a href="http://vincent.riviere.free.fr/soft/m68k-atari-mint/"<?php echo $target ?>>here</a>.</p>

<p>
<b>Patrice Mandin</b> has made a lot of work for porting GCC and the binutils
to the MiNT platform. His work is available
<a href="http://patrice.mandin.pagesperso-orange.fr/v3/en/patch-utils.html"<?php echo $target ?>>here</a>.</p>

<p>
<b>Olivier Landemarre</b> has made its own port of GCC 4.2 to the the MiNT platform.
He also has <a href="http://gem.lutece.net/discussion/archives/cat_listedeliens.html"<?php echo $target ?>>
a great list of Atari-related stuff</a>.</p>

<p>
<b>Fran&#xe7;ois Le Coat</b> is the author of the
<a href="http://eureka2.12.pagesperso-orange.fr/atari.html"<?php echo $target ?>>ATARI Search Engine</a>.</p>

<p>
<b>Thomas Huth</b> is the author of the <a href="http://hatari.tuxfamily.org/"<?php echo $target ?>>Hatari</a> ST emulator.
He has sucessfully recompiled this GCC port on Linux, on his PowerMac G4,
and has successfully compiled <a href="http://emutos.sourceforge.net/"<?php echo $target ?>>EmuTOS</a> with it!</p>
<!--
<p>
<b>Bohdan Milar</b> has (not yet ?) put a link to this page
on <a href="http://cs.atari.org/"<?php echo $target ?>>the Czech and Slovak Atari portal</a>.</p>
-->
<p>
<b>Keith Scroggins</b> has ported <a href="http://www.scummvm.org/"<?php echo $target ?>>ScummVM</a> to MiNT.
Build instructions are available <a href="http://wiki.scummvm.org/index.php/Compiling_ScummVM/Atari/FreeMiNT"<?php echo $target ?>>here</a>.
He has also made his own native port of GCC 4.0.1 several years before me, his work is available <a href="http://www.radix.net/~kws/mint/old/"<?php echo $target ?>>here</a>.</p>

<p>
<b>Miro Krop&#xe1;&#x010d;ek</b> has compiled the GCC 4.6.4 port for the MiNT host.
That means you can run the latest GCC natively on your Atari/MiNT computer, without cross-compilation!
He also made a nice Makefile for building all the toolchain.
His work is available <a href="http://mikro.atari.org/download.htm"<?php echo $target ?>>here</a>.</p>

<p>
<b>Pawe&#x0142; G&#xf3;ralski</b> has ported <a href="http://nokturnal.pl/home/atari/porty_reminiscence"<?php echo $target ?>>REminiscence</a>
to Falcon using this compiler. It is an interpreter for Delphine Software games, enabling to play Flashback on Falcon.
He also maintains the <a href="http://bus-error.nokturnal.pl/tiki-list_articles.php"<?php echo $target ?>>Bus Error Wiki</a> with a lot of programming tricks using these cross-tools.</p>

<p>
<b>Mark Duckworth</b> has built an RPM package for native MiNT binutils, using the patch available on this page.
He has compiled natively a lot of other RPM packages, his work is available <a href="http://storage.atari-source.org/atari/personal/package_staging/"<?php echo $target ?>>here</a>.</p>

<p>
<b>Dominique B&#xe9;r&#xe9;ziat</b> has written <a href="http://pequan.lip6.fr/~bereziat/softs/tos/cross-compilation/"<?php echo $target ?>>a tutorial for cross-compiling GEM applications</a>.</p>

<p>
<b>Philipp Donz&#xe9;</b> has built the binaries of an older version of these cross-tools for MacOS X (Intel and PowerPC supported).
His binaries as well as installation instructions are available <a href="http://www.xn--donz-epa.ch/atari/articles/cross-compiler/"<?php echo $target ?>>here</a>.</p>

<p>
<b>Rolf Hemmerling</b> has <a href="http://hemmerling.free.fr/doku.php/en/atarist.html"<?php echo $target ?>>a nice page about the current Atari resources on the web</a>.</p>

<p>
<b>DML</b> has <a href="http://www.leonik.net/dml/sec_atari.py"<?php echo $target ?>>a nice page about Atari and engineering</a>.</p>

<p>
<b>Peter Dassow</b> has <a href="http://www.z80.eu/stsoft.html"<?php echo $target ?>>a nice page with a lot of links to ST software</a>.</p>

<p>
<b>George Nakos</b> used the cross-tools for his <a href="http://reboot.atari.org/downloads.html"<?php echo $target ?>>raptorBASIC+</a>.</p>

<p>
<b>Jookie</b> uses the cross-tools for developing <a href="http://joo.kie.sk/?page_id=384"<?php echo $target ?>>CosmosEx</a> software.
CosmosEx is a hardware extension as small as a floppy drive which brings SD-Card, USB, Ethernet and much more to Atari computers.</p>

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

<!--
Build times:
binutils:
	mingw32: 10min
	cygwin:  8min
	macos:   3min (ld does have support for the native platform)
	linux:   30sec

gcc 4.6.4:
	mingw32: 15min
	cygwin:  19min
	macos:   15min
	linux:   2min30sec
	
gcc 7.2:
	mingw32: 32min
	cygwin:  28min
	macos:   23min
	linux:   3min
	
-->
</body>
</html>
