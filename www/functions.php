<?php

$href_target = ' target="_blank"';
$href_target = '';
$linkcount = 0;
$linkstats = array();
$targets = array(
	'all' => array('display' => 'All'),
	'mint' => array('display' => 'MiNT'),
	'mintelf' => array('display' => 'MiNTelf'),
);
$platforms = array(
	'all' => array('display' => 'All'),
	'cygwin32' => array('display' => 'Cygwin32', 'image' => 'os-cygwin.ico'),
	'cygwin64' => array('display' => 'Cygwin64', 'image' => 'os-cygwin.ico'),
	'mingw32' => array('display' => 'MinGW32', 'image' => 'os-mingw.ico'),
	'mingw64' => array('display' => 'MinGW64', 'image' => 'os-mingw.ico'),
	'linux32' => array('display' => 'Linux (x86)', 'image' => 'os-linux.png'),
	'linux64' => array('display' => 'Linux', 'image' => 'os-linux.png'),
	'macos32' => array('display' => 'MacOSX (x86)', 'image' => 'os-macos.png'),
	'macos64' => array('display' => 'MacOSX', 'image' => 'os-macos.png'),
	'atari' => array('display' => 'Atari', 'image' => 'os-atari.png'),
	'amiga' => array('display' => 'Amiga', 'image' => 'os-amigaos.png'),
);

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


function gen_link($filename, $text, $must_exist = true)
{
	global $download_dir;
	global $rpm_dir;
	global $linkcount;
	global $linkstats;
	
	$stat = 0;
	$exists = 0;
	if ($download_dir == '' || substr($filename, 0, strlen($download_dir)) == $download_dir)
	{
		$reporting = error_reporting(E_ALL & ~E_WARNING);
		$stat = stat($filename);
		if ($stat)
		{
			$exists = 1;
		}
		error_reporting($reporting);
	}
	if (!$exists && $rpm_dir !== null && $rpm_dir !== '' && substr($filename, 0, strlen($rpm_dir)) == $rpm_dir)
	{
		$reporting = error_reporting(E_ALL & ~E_WARNING);
		$stat = stat($filename);
		if ($stat)
		{
			$exists = 1;
		}
		error_reporting($reporting);
	}
	if (!$exists)
	{
		$scheme = parse_url($filename, PHP_URL_SCHEME);
		if ($scheme == 'http' || $scheme == 'https' || $scheme == 'ftp' || $scheme == 'ftps')
		{
			/* assume it exists, but avoid stat() on a slow network url */
			$exists = 1;
		}
	}

	++$linkcount;
	$id = 'tippylink' . $linkcount;
	echo '<a class="archive tippybtn"';
	if ($exists)
	{
		echo ' href="' . htmlspecialchars($filename) . '"';
	}
	echo ' id="' . $id. '"';
	if ($exists && $stat)
	{
		echo ' title="size: ' . intdiv($stat['size'], 1024) . 'K&#10;"';
		$stat['id'] = $id;
		$stat['filename'] = $filename;
		$linkstats[$id] = $stat;
	}
	echo '>' . htmlspecialchars($text) . '</a>';
	if ($exists)
	{
		$ext_ok = 0;
		
		if (fnmatch('*.tar.gz', $filename))
			$ext_ok = function_exists('gzopen') || $stat;
		else if (fnmatch('*.tgz', $filename))
			$ext_ok = function_exists('gzopen') || $stat;
		else if (fnmatch('*.tar.bz2', $filename))
			$ext_ok = function_exists('bzopen') || $stat;
		else if (fnmatch('*.tar.xz', $filename))
			$ext_ok = function_exists('xzopen') || $stat;
		if ($ext_ok)
		{
			echo '&nbsp;<a class="listtar" href="listtar.php?filename=' . urlencode($filename) . '&amp;local=' . ($stat ? "1" : "0") . '">&lt;file&nbsp;list&gt;</a>';
		} else if ($stat && !is_null($rpm_dir) && fnmatch('*.rpm', $filename))
		{
			/* Note: $rpm_dir is only set in download area, not in the rpmdetails page,
			   so this is used to check that we don't generate recursive links */
			$rpm_base = implode('/', explode('/', $rpm_dir, -3));
			// echo '&nbsp;<a class="listtar" href="' . $rpm_base . '/rpmdetails.php?file=/' . $filename . '">&lt;details&gt;</a>';
			echo '&nbsp;<a class="listtar" href="' . $rpm_base . '/rpmdetails.php?file=' . urlencode(substr($filename, strlen($rpm_base) + 1)) . '">&lt;details&gt;</a>';
		}
	}
	if (!$exists && $must_exist)
	{
		echo '<div class="error">missing</div>';
	}
}

/*
 * format here is as expected by moment():
 * http://momentjs.com/docs/#/displaying/
 */
function usertime($time, $format='YYYY/MM/DD HH:mm:ss')
{
	return '<script type="text/javascript">document.write(usertime("' . date('Y-m-d\TH:i:s\.0\Z', $time) . '", "' . $format . '"));</script>';
}


function gen_linktitles($timeformat='YYYY/MM/DD HH:mm:ss')
{
	global $linkstats;
	
	foreach ($linkstats as $stat)
	{
		echo '<!-- ' . $stat['filename'] . ': ' . $stat['size'] . " -->\n";
		/* FIXME: do not report size > 0 but < 1K as zero */
		echo "document.getElementById('" . $stat['id'] . "').setAttribute('title',
			'size: " . intdiv($stat['size'], 1024) . "K\\n" .
			"date: ' + usertime('" . date('Y-m-d\TH:i:s\.0\Z', $stat['mtime']) . "', '" . $timeformat . "') + '" .
			"\\n');\n";
	}
}

?>
