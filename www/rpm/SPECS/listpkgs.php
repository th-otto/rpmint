<?php

$target = "all";
$download_dir = ".";

include(dirname($_SERVER['PHP_SELF']) . '/../../packages.php');

foreach ($basepackages as $key => $package)
{
	printf("%-30s %20s %s\n", $package['name'], $package['version'], isset($package['summary']) ? $package['summary'] : '');
}

foreach ($libpackages as $key => $package)
{
	printf("%-30s %20s %s\n", $package['name'], $package['version'], isset($package['summary']) ? $package['summary'] : '');
}

?>
