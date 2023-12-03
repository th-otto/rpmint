<?php

$sdlpackages = array(
	'2048' => array(
		'name' => '2048',
		'version' => 'git',
		'upstream' => 'https://github.com/markblre/2048game',
		'repo' => 'https://github.com/markblre/2048game',
		'patch' => 0,
		'script' => 1,
		'category' => 'Games',
		'summary' => '2048 with GUI',
		'comment' => '
<img src="' . $download_dir . '2048.png">
'
	),
	'airball' => array(
		'name' => 'airball',
		'version' => '',
		'upstream' => 'https://oldschoolprg.x10.mx/projets.php#airball',
		'source' => $download_dir . '%{name}.tar.xz',
		'category' => 'Games',
		'summary' => 'Little remake of this Atari ST classic. This time almost in pure SDL.',
		'comment' => '
Little remake of this Atari ST classic. This time almost in pure SDL.
</br></br>
<img src="' . $download_dir . 'airball0.png">
</br></br>
To leave the editor, press "x"
'
	),
	'airstrike' => array(
		'name' => 'airstrike',
		'version' => 'pre6a',
		'title' => 'Airstrike',
		'upstream' => 'http://icculus.org/airstrike/',
		'category' => 'Games',
		'summary' => 'Airstrike is a 2d dogfighting game',
		'comment' => '
Airstrike is a 2d dogfighting game being slowly developed by various people around the net
</br></br>
<img src="' . $download_dir . 'airstrike.png" width="400" height="300">
'
	),
	'alienblaster' => array(
		'name' => 'alienblaster',
		'version' => '1.1.0',
		'title' => 'Alien Blaster',
		'upstream' => 'https://www.schwardtnet.de/alienblaster/',
		'source' => 'https://www.schwardtnet.de/alienblaster/archives/%{name}-%{version}.tgz',
		'category' => 'Games',
		'summary' => 'Your mission is simple: stop the invasion of the aliens and blast them!',
		'comment' => '
Your mission is simple: stop the invasion of the aliens and blast them!
</br></br>
<img src="' . $download_dir . 'alienblaster.jpg" width="320" height="240">
'
	),
	'griffon' => array(
		'name' => 'griffon',
		'version' => '',
		'title' => 'The Griffon Legend',
		'upstream' => 'https://github.com/dmitrysmagin/griffon_legend',
		'repo' => 'https://github.com/dmitrysmagin/griffon_legend',
		'source' => $download_dir . '%{name}.tar.xz',
		'category' => 'Games',
		'summary' => 'The Griffon Legend is an action RPG with screen-to-screen map',
		'comment' => '
The Griffon Legend is an action RPG with screen-to-screen map
</br></br>
<img src="' . $download_dir . 'griffon.png" width="320" height="240">
<ul>
<li>do not press alt(fullscreen results to bus error)</li>
<li>press esc to pass the intro</li>
<li>press ctrl+arrow to hit</li>
</ul>
'
	),
	'amphetamine' => array(
		'name' => 'amphetamine',
		'version' => '0.8.10',
		'title' => 'Amphetamine',
		'upstream' => 'https://archivegame.org/amphetamine/',
		'category' => 'Games',
		'summary' => 'Amphetamine is a cool Jump&apos;n Run game',
		'comment' => '
Amphetamine is a cool Jump&apos;n Run game offering some unique visual effects. It was created by Jonas Spillmann.
</br></br>
<img src="' . $download_dir . 'amphetamine.webp" width="320" height="240">
'
	),
	'blobwars' => array(
		'name' => 'blobwars',
		'version' => '1.14',
		'title' => 'BlobWars',
		'upstream' => 'https://hak.binaryriot.org/',
		'repo' => 'https://sourceforge.net/projects/blobwars/',
		'source' => $download_dir . '%{name}-%{version}.tar.xz',
		'category' => 'Games',
		'summary' => 'Metal Blob Solid is a 2D platform game',
		'comment' => '
Metal Blob Solid is a 2D platform game, the first in the Blobwars
series. You take on the role of a fearless Blob agent, Bob, who&apos;s
mission is to infiltrate various enemy bases and rescue as many MIAs as
possible, while battling many vicious aliens.
</br></br>
<img src="' . $download_dir . 'blobwars.png" width="320" height="240">
'
	),
	'breaker' => array(
		'name' => 'breaker',
		'version' => '',
		'title' => 'Breaker',
		'upstream' => 'https://codes-sources.commentcamarche.net/source/50067-breaker-arkanoid-like-c-sdl',
		'repo' => 'https://sourceforge.net/projects/breaker10/',
		'source' => $download_dir . '%{name}.tar.gz',
		'category' => 'Games',
		'summary' => 'Arkanoid like game',
		'comment' => '
Brick breaker (Arkanoid like), C language, SDL. See the README.TXT file in breaker.tar.xz
</br></br>
<img src="' . $download_dir . 'breaker.png" width="320" height="240">
'
	),
	'grafx2' => array(
		'name' => 'grafx2',
		'version' => '2.8.3200',
		'title' => 'GrafX2',
		'upstream' => 'https://grafx2.eu/',
		'repo' => 'https://gitlab.com/GrafX2/grafX2/',
		'source' => $download_dir . '%{name}-%{version}.tgz',
		'category' => 'Productivity/Graphics/Bitmap Editors',
		'summary' => 'GrafX2 is a bitmap paint program',
		'comment' => '
GrafX2 is a bitmap paint program inspired by the Amiga programs Deluxe
Paint and Brilliance. Specialized in 256-color drawing, it includes a
very large number of tools and effects that make it particularly
suitable for pixel art, game graphics, and generally any detailed
graphics painted with a mouse.
'
	),
);

?>
