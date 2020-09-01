<?php
error_reporting(E_ALL);
ini_set("display_errors", 1);

require_once('RPM.php');
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
          "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>m68k-atari-mint cross-tools</title>
<meta name="keywords" content="ARAnyM, EmuTOS, GCC, Atari, MiNT" />
<link rel="stylesheet" type="text/css" href="rpm.css" />
</head>

<body>

<?php
if (!isset($_GET['file']))
	exit(1);
$filename = $_GET['file'];
?>

<div class="container">

<div class="header">
<h1 class="text-break">php70-php-pecl-rpminfo-0.5.0-1.el7.remi.x86_64.rpm</h1>
<hr/>
</div>

<div class="content">
<div class="d-flex">
<div class="flex-grow-1 mw-0">
<div id="view_packages_info">

<h2>Description</h2>
<div class="alert">
<p><b>php70-php-pecl-rpminfo - RPM information</b></p>
</div>

<table class="table table-bordered table-hover table-sm1 table-striped">
<tbody>
<tr>
<th scope="row">Operating system</th>
<td class="text-break"><strong>Linux</strong></td>
</tr>
<tr>
<th scope="row">Package filename</th>
<td class="text-break">php70-php-pecl-rpminfo-0.5.0-1.el7.remi.x86_64.rpm</td>
</tr>
<tr>
</tbody>
</table>

<div class="alert">
<pre>Retrieve RPM information using librpm.
Available functions:
- rpmvercmp to compare 2 EVRs
- rpminfo to retrieve information from a RPM file
- rpmdbinfo to rerieve information from an installed RPM
- rpmdbsearch to search installed RPMs
Documentation: https://www.php.net/rpminfo
Package built for PHP 7.0 as Software Collection (php70 by remi).
</pre>
</div>

<h2>Requires</h2>
<table class="table table-bordered table-hover table-sm1 table-striped">
<tbody class="text-break">
<tr>
<td>libc.so.6(GLIBC_2.14)(64bit)</td>
<td class="mono">-</td>
</tr>
<tr>
<td>librpm.so.3()(64bit)</td>
<td class="mono">-</td>
</tr>
<tr>
<td>librpmio.so.3()(64bit)</td>
<td class="mono">-</td>
</tr>
</tbody>
</table>

<h2>Provides</h2>
<table class="table table-bordered table-hover table-sm1 table-striped">
<tbody class="mono text-break">
<tr>
<td class="bold">config(php70-php-pecl-rpminfo)</td>
<td>= 0.5.0-1.el7.remi</td>
</tr>
<tr>
<td class="bold">php70-php-pecl(rpminfo)(x86-64)</td>
<td>= 0.5.0</td>
</tr>
<tr>
<td class="bold">php70-php-pecl-rpminfo</td>
<td>= 0.5.0-1.el7.remi</td>
</tr>
</tbody>
</table>

<h2 id="download">Download</h2>
<table class="table table-bordered table-hover table-sm1">
<tbody>
<th class="text-nowrap" scope="row">Binary Package</th>
<td class="text-break">https://rpms.remirepo.net/enterprise/7/remi/x86_64/php70-php-pecl-rpminfo-0.5.0-1.el7.remi.x86_64.rpm</td>
</tr>
<tr>
<th class="text-nowrap" scope="row">Source Package</th>
<td class="text-break">
php70-php-pecl-rpminfo-0.5.0-1.el7.remi.src.rpm
</td>
</tr>
</tbody>
</table>

<h2>Files</h2>
<table class="table table-bordered table-hover table-sm1 table-striped">
<tbody class="mono text-break">
<tr>
<td>/etc/opt/remi/php70/php.d/40-rpminfo.ini</td>
</tr>
</tbody>
</table>

<h2>Changelog</h2>
<div class="alert alert-secondary bg-light2 pb-0">
<div id="changelog">
<pre><b>2020-04-07</b> - Remi Collet &lt;remi@remirepo.net&gt; - 0.5.0-1
- update to 0.5.0</pre>
<pre><b>2020-03-25</b> - Remi Collet &lt;remi@remirepo.net&gt; - 0.4.2-1
- update to 0.4.2</pre>
<pre><b>2020-03-18</b> - Remi Collet &lt;remi@remirepo.net&gt; - 0.4.1-1
- update to 0.4.1</pre>
</div>
</div>


</div>
</div>
</div>
</div>
</div>

<p></p>
<p></p>

<div style="text-align:center">
<p>
<a href="../.."> <img src="../../../../images/home1.png" width="180" height="60" style="border:0" alt="Back" /></a>
</p>
</div>

</body>
</html>
