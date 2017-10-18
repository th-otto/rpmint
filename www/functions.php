<?php

$target = ' target="_blank"';
$target = '';

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

/*
 * format here is as expected by moment():
 * http://momentjs.com/docs/#/displaying/
 */
function usertime($time, $format='YYYY/MM/DD HH:mm:ss')
{
	return '<script type="text/javascript">document.write(usertime("' . date('Y-m-d\TH:i:s\.0\Z', $time) . '", "' . $format . '"));</script>';
}

?>
