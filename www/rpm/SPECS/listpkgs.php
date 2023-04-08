<?php

$target = "all";
$download_dir = ".";

include(dirname($_SERVER['PHP_SELF']) . '/../../packages.php');
include(dirname($_SERVER['PHP_SELF']) . '/../../licenses.php');

$pkgs = array_merge($basepackages, $libpackages);
ksort($pkgs, SORT_STRING);

if (isset($_SERVER["argv"][1]) && $_SERVER["argv"][1] === "--names")
{
	foreach ($pkgs as $key => $package)
	{
		printf("%s\n", $package['name']);
	}
} else
{
	foreach ($pkgs as $key => $package)
	{
		$license = isset($package['license']) ? $package['license'] : '';
		$summary = isset($package['summary']) ? $package['summary'] : '';
		if ($license !== '')
		{
			License::check($package['name'], $license);
		}
		printf("%-30s %-20s %-20s %s\n", $package['name'], $package['version'], $license, $summary);
	}
}

?>
