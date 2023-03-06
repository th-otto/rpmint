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
			$license_check = $license;
			if (preg_match('/(.*) WITH (.*)/', $license, $match))
			{
				$license_check = $match[1];
				if (!array_key_exists($match[2], $license_exceptions))
					fprintf(STDERR, "$key: unknown license exception ${match[2]}\n");
			}
		}
		foreach (preg_split('/( OR | AND | or | and )/', $license_check) as $l)
		{
			$l = str_replace('(', '', $l);
			$l = str_replace(')', '', $l);
			if (!array_key_exists($l, $licenses))
				fprintf(STDERR, "$key: unknown license $l\n");
		}
		printf("%-30s %-20s %-20s %s\n", $package['name'], $package['version'], $license, $summary);
	}
}

?>
