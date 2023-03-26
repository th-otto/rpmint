<?php
include('rpmvars.php');
$document_root = '../';
include($document_root . 'licenses.php');

require_once('RPM.php');

$files = array();

function find_rpms(string $dirname)
{
	global $files;
	
	if ($dir = opendir($dirname))
	{
		while (false !== ($file = readdir($dir)))
		{
			if ($file == ".") continue;
			if ($file == "..") continue;
			if (substr($file, 0, 1) == '.') continue;
			$filename = $dirname . '/' . $file;
			if (substr($file, strlen($file) - 4) == '.rpm')
			{
				array_push($files, $filename);
			}
			$reporting = error_reporting(E_ALL & ~E_WARNING);
			$stat = stat($filename);
			error_reporting($reporting);
			if ($stat)
			{
				if (($stat['mode'] & 0170000) == 0040000)
				{
					// printf("$filename\n");
					find_rpms($filename);
				}
			}
		}
	 	closedir($dir);
 	}
}


find_rpms('.');

foreach ($files as $file)
{
	if ($rpm = rpm_open($file))
	{
		$license = $rpm->get_tag_as_string(RPMTAG_LICENSE);
		License::check($file, $license);
		unset($rpm);
	}
}

?>
