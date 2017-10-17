<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
          "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>m68k-atari-mint cross-tools</title>
<meta name="keywords" content="ORCS, CAT, GC, PBEM, PBM, GC-Ork, GCORK, ARAnyM, UDO, EmuTOS, GCC" />
<link rel="stylesheet" type="text/css" href="home.css" />
<script type="text/javascript" src="moment.min.js" charset="UTF-8"></script>
<script type="text/javascript">
function usertime(time, format)
{
	return moment(time).format(format);
}
</script>
</head>

<?php

error_reporting(E_ALL & ~E_WARNING);
ini_set("display_errors", 1);
date_default_timezone_set('UTC');

/*
 * format here is as expected by moment():
 * http://momentjs.com/docs/#/displaying/
 */
function usertime($time, $format='YYYY/MM/DD hh:mm:ss')
{
	return '<script type="text/javascript">document.write(usertime("' . date('Y-m-d\TH:i:s\.0\Z', $time) . '", "' . $format . '"));</script>';
}

$download_dir = 'download/mint/';
$target = ' target="_blank"';
$target = '';

$basepackages = array(
	'binutils' => array(
		'name' => 'binutils',
		'upstream' => 'http://www.gnu.org/software/binutils/',
		'version' => '2.29.1',
		'date' => '20171011',
		'repo' => 'https://github.com/th-otto/binutils',
		'branch' => 'binutils-2_29-mint',
		'source' => 'https://ftp.gnu.org/gnu/binutils/binutils-2.29.1.tar.xz',
		'patch' => 1,
		'script' => 1,
		'doc' => 1,
		'elf' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
The binutils are a collection of low-level language tools.<br />
The full documentation can be found
<a href="https://sourceware.org/binutils/docs-2.29/" ' . $target . '>here</a>.<br />
		'
	),
	'gcc464' => array(
		'name' => 'gcc',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '4.6.4',
		'date' => '20170518',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'gcc-4_6-mint',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-4.6.4/gcc-4.6.4.tar.bz2',
		'patch' => 1,
		'patchcomment' => 'This archive also contains an (experimental) patch for -mfastcall support.',
		'script' => 1,
		'doc' => 1,
		'elf' => 0,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
<code>m68k-atari-mint-gcc</code> is the C compiler.<br />
<code>m68k-atari-mint-g++</code> is the C++ compiler.<br />
They just work. I only tested the C and C++ languages, but other languages may work, too.<br />
If you want to generate DRI symbols in the final executable, append the option
<code>-Wl,--traditional-format</code> to inform the linker.<br />
I configured this version to generate 68000 code by default, and I enabled multilib.
By default, <code>sizeof(int) == 4</code>, but if you compile with <code>-mshort</code>
then <code>sizeof(int) == 2</code> (unsupported by the current MiNTLib). Every object file and every library must be compiled
with the same option! You can also generate code for the 68020 and higher and for the FPU
by using the <code>-m68020-60</code> option. And you can generate code for ColdFire V4e processors
by using the <code>-mcpu=5475</code> option.<br />
The full documentation can be found
<a href="http://gcc.gnu.org/onlinedocs/gcc-4.6.4/gcc/" ' . $target . '>here</a>.<br />
GCC contains everything to compile C programs, except a standard library and a math library.
'
	),
	'gcc720' => array(
		'name' => 'gcc',
		'title' => 'GCC',
		'upstream' => 'http://gcc.gnu.org/',
		'version' => '7.2.0',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/m68k-atari-mint-gcc',
		'branch' => 'gcc-7-mint',
		'source' => 'https://ftp.gnu.org/gnu/gcc/gcc-7.2.0/gcc-7.2.0.tar.xz',
		'patch' => 1,
		'patchcomment' => 'The patches include necessary support for an elf toolchain.',
		'script' => 1,
		'doc' => 1,
		'elf' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 0,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
This is the currently most recent official version GCC. It comes in two
flavours: one for a.out toolchain (as the previously used version
4.6.4), and one for an elf toolchain. Elf toolchain here means that it
will still produce the same executable format, but works with elf object
files. To support this better, all libraries offered here were also recompiled
using this format (although it is theoretically should be possible to mix them).
'
	),
	'mintbin' => array(
		'name' => 'mintbin',
		'title' => 'MiNTBin',
		'upstream' => 'https://github.com/freemint/mintbin',
		'version' => '0.3',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/mintbin',
		'source' => $download_dir . 'mintbin-0.3.tar.xz',
		'patch' => 0,
		'script' => 1,
		'doc' => 0,
		'elf' => 1,
		'cygwin32' => 1,
		'cygwin64' => 1,
		'mingw32' => 1,
		'mingw64' => 0,
		'linux32' => 0,
		'linux64' => 1,
		'macos32' => 0,
		'macos64' => 1,
		'comment' => '
MiNTBin has been written by Guido Flohr. It is a set of tools for manipulating
the MiNT executables generated by <code>ld</code>. They are a complement to
the binutils. The main tools are <code>stack</code> for setting the stack size
of an executable, and <code>flags</code> for setting the header flags.
'
	),
);

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

function last_changetime($filename)
{
	global $download_dir;
	$files = scandir($download_dir);
	$date = 0;
	foreach ($files as $file)
	{
		if (substr($file, 0, strlen($filename)) == $filename)
		{
			$time = filemtime("$download_dir/$file");
			if ($time > $date)
				$date = $time;
		}
	}
	if ($date == 0)
	{
		return "";
	}
	return usertime($date);
}


function gen_link($filename, $text)
{
	global $download_dir;
	$stat = 0;
	$exists = 1;
	if (substr($filename, 0, strlen($download_dir)) == $download_dir)
	{
		$stat = stat($filename);
		if (!$stat)
		{
			$exists = 0;
		}
	}
	echo '<a class="archive" href="' . $filename . '"';
	if ($exists && $stat)
	{
		echo ' title="size: ' . intdiv($stat['size'], 1024) . 'K&#10;"';
		
	}
	echo '>' . $text . '</a>';
	if (!$exists)
	{
		echo '<div class="error">missing</div>';
	}
}

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
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc">GitHub repository:</td>';
		echo '<td class="sourcelink">';
		echo '<a href="' . $package['repo'];
		if (isset($package['branch']))
			echo '/tree/' . $package['branch'];
		echo '"' . $target . '>';
		$repo = str_replace('https://github.com/', '', $package['repo']);
		echo $repo;
		echo '</a>';
		echo '</td>';
		echo '</tr>';
	}

	if (isset($package['source']))
	{
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc">Original sources:</td>';
		echo '<td class="sourcelink">';
		echo '<a class="archive" href="' . $package['source'] . '">' . basename($package['source']) . '</a>';
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['patch'])
	{
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc">MiNT patch:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint.tar.xz';
		gen_link($filename, $text);
		echo '</td>';
		echo '</tr>';
	}
	
	if (isset($package['patchcomment']))
	{
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc"></td>';
		echo '<td class="sourcelink" colspan="2">' . $package['patchcomment'] . '</td>';
		echo '</tr>';
	}
	
	if ($package['script'])
	{
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc">Build script:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . 'build-' . $package['name'] . '-' . $package['version'];
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '.sh';
		$text = 'build-' . $package['name'] . '-' . $package['version'] . '-sh';
		gen_link($filename, $text);
		echo '</td>';
		echo '</tr>';
	}
	
	if (isset($package['doc']) && $package['doc'])
	{
		echo '<tr>';
		echo '<td class="icon"></td>';
		echo '<td class="linkdesc">Documentation:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-doc.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-doc.tar.xz';
		gen_link($filename, $text);
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['cygwin32'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-cygwin.ico" width="32" height="32" alt="Cygwin"></img></td>';
		echo '<td class="linkdesc">Cygwin Package:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-cygwin32.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-cygwin32.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>';
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
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['cygwin64'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-cygwin.ico" width="32" height="32" alt="Cygwin"></img></td>';
		echo '<td class="linkdesc">Cygwin Package:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-cygwin64.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-cygwin64.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>';
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
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['mingw32'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-mingw.ico" width="32" height="32" alt="MinGW"></img></td>';
		echo '<td class="linkdesc">MinGW Package:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-mingw32.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-mingw32.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>';
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
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['mingw64'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-mingw.ico" width="32" height="32" alt="MinGW"></img></td>';
		echo '<td class="linkdesc">MinGW Package:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-mingw64.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-mingw64.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>';
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
		echo '</td>';
		echo '</tr>';
	}

	if (!$package['mingw32'] && !$package['mingw64'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-mingw.ico" width="32" height="32" alt="MinGW"></img></td>';
		echo '<td class="linkdesc">MinGW Package:</td>';
		echo '<td class="sourcelink">(not yet available)</td>';
		echo '</tr>';
	}
	
	if ($package['linux64'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-linux.png" width="32" height="32" alt="Linux"></img></td>';
		echo '<td class="linkdesc">Linux Package:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
 		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-linux.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-linux.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>';
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
		echo '</td>';
		echo '</tr>';
	}
	
	if ($package['macos64'])
	{
		echo '<tr>';
		echo '<td class="icon"><img src="images/os-macos.png" width="32" height="32" alt="MacOSX"></img></td>';
		echo '<td class="linkdesc">MacOSX Package:</td>';
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-bin-macos.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint-bin-macos.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>';
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
		echo '</td>';
		echo '</tr>';
	}
	
	echo '</table></td>';

	echo '<td>';
	if (isset($package['comment']))
		echo $package['comment'];
	echo '</td>';
	
	echo '</tr>';
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
compiled for 68k. For native installation, there will also be *-bin
packages for other machines.</p>

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

$libpackages = array(
	'mintlib' => array(
		'name' => 'mintlib',
		'title' => 'MiNTLib',
		'upstream' => 'https://github.com/freemint/mintlib',
		'version' => '0.60.1',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/mintlib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
MiNTLib is a standard C library. It allows to build software which runs on MiNT and TOS
operating systems. Unlike other packages, I used the latest sources from the CVS repository
instead of the latest official release.
'
	),
	'pml' => array(
		'name' => 'pml',
		'title' => 'PML',
		'upstream' => 'http://ftp.funet.fi/pub/atari/programming/',
		'version' => '2.03',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/pml',
		'branch' => 'master',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
PML stands for Portable Math Library.<br />
It works, but of course it is really slow on a 68000 without FPU.'
	),
	'gemlib' => array(
		'name' => 'gemlib',
		'title' => 'GEMlib',
		'upstream' => 'https://github.com/freemint/lib',
		'version' => '0.44.0',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/lib',
		'branch' => 'master/gemlib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
The GEMlib allows to write graphical programs using GEM.<br />
It is maintained by Arnaud Bercegeay, the official releases are available
on the <a href="http://arnaud.bercegeay.free.fr/gemlib/"' . $target . '>GEMlib&apos;s homepage</a>.
However, the latest sources are available
on the <a href="https://github.com/freemint/lib"' . $target . '>FreeMiNT&apos;s GitHub repository</a>.
'
	),
	'cflib' => array(
		'name' => 'cflib',
		'title' => 'CFLIB',
		'upstream' => 'https://github.com/freemint/lib',
		'version' => '21',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/lib',
		'branch' => 'master/cflib',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
CFLIB is Christian Felsch&apos;s GEM utility library. It provide advanced controls,
such as check boxes, radio buttons, combo boxes... It also allows windowed
dialogs.<br />
BUG: On plain TOS, the CFLIB makes intensive usage of the GEM USERDEF feature.
Due to bad GEM design, USERDEF callbacks are called in supervisor mode using
the very small internal AES stack. Unfortunately, some GemLib functions such
as v_gtext() needs an insane amout of stack (more than 2 KB). So some USERDEF
callbacks quickly produces an AES internal stack overflow, and crashes all the
system.<br />
Concretely, due to this issue, programs using the CFLIB work fine on XaAES
and TOS 4.04, but crashes on TOS 1.62 and EmuTOS.
'
	),
	'gemma' => array(
		'name' => 'gemma',
		'upstream' => 'https://github.com/freemint/lib',
		'version' => 'git',
		'date' => '20171006',
		'repo' => 'https://github.com/th-otto/lib',
		'branch' => 'master/gemma',
		'patch' => 0,
		'script' => 1,
		'dev' => 1,
		'comment' => '
Gemma is a support library for GEM application programs.
'
	),
	'zlib' => array(
		'name' => 'zlib',
		'upstream' => 'http://www.zlib.net/',
		'source' => 'http://www.zlib.net/zlib-1.2.11.tar.xz',
		'version' => '1.2.11',
		'date' => '20171006',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
zlib is a compression library implementing the Deflate algorithm, used by gzip and PKZIP.
'
	),
	'libpng' => array(
		'name' => 'libpng',
		'upstream' => 'http://www.libpng.org/pub/png/libpng.html',
		'source' => 'https://ftp-osl.osuosl.org/pub/libpng/src/libpng16/libpng-1.6.34.tar.xz',
		'version' => '1.6.34',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
Portable Network Graphics
<br />
An Open, Extensible Image Format with Lossless Compression 
'
	),
	'bzip2' => array(
		'name' => 'bzip2',
		'upstream' => 'http://www.bzip.org/',
		'source' => 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz',
		'version' => '1.0.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
bzip2 is a freely available, patent free (see below), high-quality data
compressor. It typically compresses files to within 10% to 15% of the
best available techniques (the PPM family of statistical compressors),
whilst being around twice as fast at compression and six times faster
at decompression.
'
	),
	'ldg' => array(
		'name' => 'ldg',
		'title' => 'LDG',
		'upstream' => 'http://ldg.sourceforge.net/',
		'version' => 'svn-20171014',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
LDG stands for Gem Dynamical Libraries (actually Librairies Dynamiques
GEM in french). It&apos;s a system allowing GEM applications to load and to
share externals modules. 
<br />
Only the libraries are compiled. To use modules, you also have to
install the auto folder programs from <a href="http://ldg.sourceforge.net/#download">http://ldg.sourceforge.net/</a>. 
'
	),
	'windom' => array(
		'name' => 'windom',
		'title' => 'WinDom',
		'upstream' => 'http://windom.sourceforge.net/',
		'version' => '2.0.1',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Windom is a C library to make GEM programming very easy. With the help
of windom, you can focus on programming the real job of your
application, and let windom handle complex and "automatic" GEM stuff
(toolbar, forms, menu in windows...). 
'
	),
	'sdl' => array(
		'name' => 'SDL',
		'upstream' => 'https://www.libsdl.org/',
		'version' => '1.2.15-hg',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
SDL is the Simple DirectMedia Layer library. It is a low-level and cross-platform
library for building games or similar programs.<br />
Thanks to Patrice Mandin, SDL is available on Atari platforms. SDL programs can
run either in full screen or in a GEM window, depending on the SDL_VIDEODRIVER
environment variable.
'
	),
	'ncurses6' => array(
		'name' => 'ncurses',
		'upstream' => 'http://invisible-island.net/ncurses/ncurses.html',
		'source' => 'ftp://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.0.tar.gz',
		'version' => '6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
Ncurses is a library which allows building full-screen text mode programs,
such as <code>vim</code>, <code>less</code>, or the GDB text UI.
'
	),
	'readline' => array(
		'name' => 'readline',
		'upstream' => 'https://cnswww.cns.cwru.edu/php/chet/readline/rltop.html',
		'source' => 'ftp://ftp.gnu.org/gnu/readline/readline-7.0.tar.gz',
		'version' => '7.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'comment' => '
The GNU Readline library provides a set of functions for use by
applications that allow users to edit command lines as they are typed
in. Both Emacs and vi editing modes are available. The Readline library
includes additional functions to maintain a list of previously-entered
command lines, to recall and perhaps reedit those lines, and perform
csh-like history expansion on previous commands.
'
	),
	'openssl' => array(
		'name' => 'openssl',
		'title' => 'OpenSSL',
		'upstream' => 'https://www.openssl.org/',
		'source' => 'https://www.openssl.org/source/openssl-1.0.2l.tar.gz',
		'version' => '1.0.2l',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
OpenSSL is a robust, commercial-grade, and full-featured toolkit for
the Transport Layer Security (TLS) and Secure Sockets Layer (SSL)
protocols. It is also a general-purpose cryptography library. 
'
	),
	'arc' => array(
		'name' => 'arc',
		'upstream' => 'http://arc.sourceforge.net/',
		'source' => $download_dir . 'arc-5.21p.tar.gz',
		'version' => '5.21p',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
ARC is used to create and maintain file archives. An archive is a group
of files collected together into one file in such a way that the
individual files may be recovered intact.
'
	),
	'arj' => array(
		'name' => 'arj',
		'upstream' => 'http://arj.sourceforge.net/',
		'source' => $download_dir . 'arj-3.10.22.tar.gz',
		'version' => '3.10.22',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
A portable version of the ARJ archiver, available for a growing number
of DOS-like and UNIX-like platforms on a variety of architectures.
'
	),
	'lha' => array(
		'name' => 'lha',
		'upstream' => 'http://lha.sourceforge.jp/',
		'source' => $download_dir . 'lha-1.14i-ac20050924p1.tar.gz',
		'version' => '1.14i-ac20050924p1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
LHa for UNIX - Note: This software is licensed under the ORIGINAL
LICENSE. It is written in man/lha.n in Japanese 
'
	),
/*
	'unrar' => array(
		'name' => 'unrar',
		'title' => 'UnRAR',
		'upstream' => 'http://www.rarlab.com/',
		'source' => 'https://www.rarlab.com/rar/unrarsrc-5.5.8.tar.gz',
		'version' => '5.5.8',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
Unarchiver for .rar files (non-free version)
Unrar can extract files from .rar archives. If you want to create .rar
archives, install package rar.
'
	),
*/
	'xz' => array(
		'name' => 'xz',
		'upstream' => 'http://tukaani.org/xz/',
		'version' => '5.2.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 1,
		'comment' => '
XZ Utils is free general-purpose data compression software with a high
compression ratio. XZ Utils were written for POSIX-like systems, but
also work on some not-so-POSIX systems. XZ Utils are the successor to
LZMA Utils. 
'
	),
	'zip' => array(
		'name' => 'zip',
		'upstream' => 'http://www.info-zip.org/Zip.html',
		'source' => 'ftp://ftp.info-zip.org/pub/infozip/src/zip30.tgz',
		'version' => '3.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
Zip is a compression and file packaging utility. It is compatible with
PKZIP(tm) 2.04g (Phil Katz ZIP) for MS-DOS systems.
'
	),
	'unzip' => array(
		'name' => 'unzip',
		'upstream' => 'http://www.info-zip.org/UnZip.html',
		'source' => 'ftp://ftp.info-zip.org/pub/infozip/src/unzip60.tgz',
		'version' => '6.0',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
UnZip is an extraction utility for archives compressed in .zip format
(known as &quot;zip files&quot;).  Although highly compatible both with PKWARE&apos;s
PKZIP(tm) and PKUNZIP utilities for MS-DOS and with Info-ZIP&apos;s own Zip
program, our primary objectives have been portability and non-MS-DOS
functionality. This version can also extract encrypted archives.
'
	),
	'zoo' => array(
		'name' => 'zoo',
		'upstream' => 'http://ftp.math.utah.edu/pub/zoo/',
		'source' => 'http://ftp.math.utah.edu/pub/zoo/zoo-2-10-1.tar.bz2',
		'version' => '2-10-1',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
Zoo is a packer based on the Lempel-Ziv algorithm. Lots of files on
DOS/AmigaDOS and TOS systems used this packer for their archives. The
compression rate of gzip is not reached, and thus zoo should only be used
for decompressing old archives.
'
	),
	'gmp' => array(
		'name' => 'gmp',
		'upstream' => 'https://gmplib.org/',
		'source' => 'https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz',
		'version' => '6.1.2',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
A library for calculating huge numbers (integer and floating point).
'
	),
	'mpfr' => array(
		'name' => 'mpfr',
		'upstream' => 'http://www.mpfr.org/',
		'source' => 'http://www.mpfr.org/mpfr-current/mpfr-3.1.6.tar.xz',
		'version' => '3.1.6',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
The MPFR library is a C library for multiple-precision floating-point
computations with exact rounding (also called correct rounding). It is
based on the GMP multiple-precision library.
'
	),
	'mpc' => array(
		'name' => 'mpc',
		'upstream' => 'http://www.multiprecision.org/mpc/',
		'source' => 'ftp://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz',
		'version' => '1.0.3',
		'patch' => 1,
		'script' => 1,
		'dev' => 1,
		'bin' => 0,
		'comment' => '
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as MPFR.
'
	),
	'tar' => array(
		'name' => 'tar',
		'upstream' => 'http://www.gnu.org/software/tar/',
		'source' => 'https://ftp.gnu.org/gnu/tar/tar-1.29.tar.xz',
		'version' => '1.29',
		'patch' => 1,
		'script' => 1,
		'dev' => 0,
		'bin' => 1,
		'comment' => '
GNU Tar is an archiver program. It is used to create and manipulate files
that are actually collections of many other files; the program provides
users with an organized and systematic method of controlling a large amount
of data. Despite its name, that is an acronym of "tape archiver", GNU Tar
is able to direct its output to any available devices, files or other programs,
it may as well access remote devices or files.
'
	),
);

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
		$source = $package['source'];
	} else
	{
		$source = $download_dir . $package['name'] . '-' . $package['version'] . '.tar.xz';
	}
	if (1)
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
		echo '<td class="linkdesc">Original sources:</td>' . "\n";
		echo '<td class="sourcelink">';
		gen_link($source, basename($source));
		echo '</td>' . "\n";
		echo '</tr>' . "\n";
	}
	
	if ($package['patch'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"></td>' . "\n";
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
		$text = 'build-' . $package['name'] . '-' . $package['version'] . '.sh';
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
	
	if (isset($package['dev']) && $package['dev'])
	{
		echo '<tr>' . "\n";
		echo '<td class="icon"><img src="images/empty.png" width="32" height="32" alt=""></img></td>' . "\n";
		echo '<td class="linkdesc">Devel Package:</td>' . "\n";
		echo '<td class="sourcelink">';
		$filename = $download_dir . $package['name'] . '-' . $package['version'] . '-mint';
		if (isset($package['date']))
			$filename .= '-' . $package['date'];
		$filename .= '-dev.tar.xz';
		$text = $package['name'] . '-' . $package['version'] . '-mint.tar.xz';
		gen_link($filename, $text);
		echo '</td></tr>' . "\n";
		echo '<tr><td></td><td></td><td class="sourcelink">';
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
		echo '<td class="icon"><img src="images/empty.png" width="32" height="32" alt=""></img></td>' . "\n";
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
		echo '<td class="icon"><img src="images/empty.png" width="32" height="32" alt=""></img></td>' . "\n";
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
		echo '<td class="icon"><img src="images/empty.png" width="32" height="32" alt=""></img></td>' . "\n";
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
He has compiled natively a lot of other RPM packages, his work is available <a href="http://storage.atari-source.org:8000/atari/personal/package_staging/"<?php echo $target ?>>here</a>.</p>

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
