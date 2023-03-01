<?php

$target = "all";
$download_dir = ".";

include('../../packages.php');

foreach ($basepackages as $key => $package)
{
	printf("%-30s %10s\n", $package['name'], $package['version']);
}

foreach ($libpackages as $key => $package)
{
	printf("%-30s %10s\n", $package['name'], $package['version']);
}

?>
