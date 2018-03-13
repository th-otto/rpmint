<?php

$target = ' target="_blank"';
$target = '';
$linkcount = 0;
$linkstats = array();

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
	global $linkcount;
	global $linkstats;
	
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
	++$linkcount;
	$id = 'tippylink' . $linkcount;
	echo '<a class="archive tippybtn" href="' . $filename . '" id="' . $id. '"';
	if ($exists && $stat)
	{
		echo ' title="size: ' . intdiv($stat['size'], 1024) . 'K&#10;"';
		$stat['id'] = $id;
		$stat['filename'] = $filename;
		$linkstats[$id] = $stat;
	}
	echo '>' . $text . '</a>';
	if ($exists)
	{
		$ext_ok = 0;
		
		if (fnmatch('*.tar.gz', $filename))
			$ext_ok = function_exists('gzopen') || $stat;
		else if (fnmatch('*.tar.bz2', $filename))
			$ext_ok = function_exists('bzopen') || $stat;
		else if (fnmatch('*.tar.xz', $filename))
			$ext_ok = function_exists('xzopen') || $stat;
		if ($ext_ok)
		{
			echo '&nbsp;<a class="listtar" href="listtar.php?filename=' . $filename . '&local=' . ($stat != null) . '">&lt;file&nbsp;list&gt;</a>';
		}
	}
	if (!$exists)
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
		echo '<!-- ' . $stat['filename'] . ': ' . $stat['size'] . " --!>\n";
		echo "document.getElementById('" . $stat['id'] . "').setAttribute('title',
			'size: " . intdiv($stat['size'], 1024) . "K\\n" .
			"date: ' + usertime('" . date('Y-m-d\TH:i:s\.0\Z', $stat['mtime']) . "', '" . $timeformat . "') + '" .
			"\\n');\n";
	}
}

?>
