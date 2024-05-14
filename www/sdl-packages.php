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
For further instruction just use the included Docs and/or visit the
original website at
<a href="https://www.parallelrealities.co.uk/projects/blobWars.php">https://www.parallelrealities.co.uk/</a>
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
	'circuslinux' => array(
		'name' => 'circuslinux',
		'version' => '1.0.3',
		'title' => 'Circus Linux!',
		'upstream' => 'http://www.newbreedsoftware.com/circus-linux/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => '"Circus Linux!" is a clone of the Atari 2600 game "Circus Atari',
		'comment' => '
"Circus Linux!" is a clone of the Atari 2600 game "Circus Atari,"
produced by Atari, Inc. (which is itself a clone of an earlier arcade
game named, simply "Circus").
</br></br>
<img src="' . $download_dir . 'circus-linux.gif" width="320" height="240">
'
	),
	'lbreakout2' => array(
		'name' => 'lbreakout2',
		'version' => '2.6.5',
		'title' => 'LBreakout2',
		'upstream' => 'https://lgames.sourceforge.io/LBreakout2/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'Successor to LBreakout',
		'comment' => '
The successor to LBreakout offers you a new challenge in more than 50
levels with loads of new bonuses (goldshower, joker, explosive balls,
bonus magnet ...), maluses (chaos, darkness, weak balls, malus magnet
...) and special bricks (growing bricks, explosive bricks, regenerative
bricks ...). If you are hungry for more you can create your own
levelsets with the integrated level editor. There is also an
experimental two player mode (via LAN) available.
</br></br>
<img src="' . $download_dir . 'lbreakout2.jpg" width="320" height="240">
'
	),
	'deathris' => array(
		'name' => 'deathris',
		'version' => '',
		'upstream' => 'https://github.com/portalrat/deathris',
		'repo' => 'https://github.com/portalrat/deathris',
		'category' => 'Games',
		'summary' => 'Simple Tetris clone',
		'comment' => '
</br></br>
<img src="' . $download_dir . 'deathris.png" width="320" height="240">
'
	),
	'digger' => array(
		'name' => 'digger',
		'version' => '',
		'upstream' => 'https://aminet.net/package/game/misc/digger-68k',
		'category' => 'Games',
		'summary' => 'Digger - the SDL version of old DOS game',
		'comment' => '
Digger was originally created by Windmill software in 1983 and released as a
copy-protected, bootable 5.25" floppy disk for the IBM PC. As it requires a
genuine CGA card, it didn&apos;t work on modern PCs.
</br></br>
<img src="' . $download_dir . 'digger1.png" width="320" height="240">
'
	),
	'xpired' => array(
		'name' => 'xpired',
		'version' => '',
		'upstream' => 'https://aminet.net/package/game/shoot/Xpired_m68k',
		'category' => 'Games',
		'summary' => 'X-pired + level editor',
		'comment' => '
Xpired is sokoban inspired logic adventure game.
There is an editor and another set of levels included
</br></br>
<img src="' . $download_dir . 'xpired.png" width="300" height="300">
'
	),
	'fillets-ng' => array(
		'name' => 'fillets-ng',
		'version' => '1.0.1',
		'upstream' => 'https://fillets.sourceforge.net/index.php',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'Solve the puzzle and help the fish escape',
		'comment' => '
Fish Fillets NG is strictly a puzzle game. The goal in every of the
seventy levels is always the same: find a safe way out. The fish utter
witty remarks about their surroundings, the various inhabitants of
their underwater realm quarrel among themselves or comment on the
efforts of your fish. The whole game is accompanied by quiet,
comforting music.
</br></br>
Tips: Tab to pass the intro, space to swap between fishes
</br></br>
<a href="' . $download_dir . 'fillets-ng-data-1.0.1.tar.gz">data are needed</a> for both the binary and the source version (~146MB).
</br></br>
<img src="' . $download_dir . 'fillets-ng.png" width="300" height="300">
'
	),
	'gemdropx' => array(
		'name' => 'gemdropx',
		'title' => 'Gem Drop X',
		'version' => '0.9',
		'upstream' => 'http://www.newbreedsoftware.com/gemdropx/',
		'source' => 'https://tuxpaint.org/ftp/unix/x/gemdropx/src/%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'A Catch the droping gems game! Betcha can&apos;t!',
		'comment' => '
    "Gem Drop X" is an interesting one-player puzzle game using the
    Simple DirectMedia Layer (SDL) libraries.
    It is a direct port of "Gem Drop," an Atari 8-bit game written in Action!
    (a very fast C- and Pascal-like compiled language for the Atari).
    It was originally ported to X11, using SDL for sound and music.
    Eventually, the Xlib graphics calls were removed and replaced with
    SDL calls.
    The concept of the game "Gem Drop" is based on an arcade game for the
    NeoGeo system called "Magical Drop III" by SNK.
    If you&apos;re familiar with games like Jewels, Klax, Bust-A-Move or Tetris,
    this game is similar to them all.  I consider it closest to Klax.
    Some people have compared it to "Tetris meets Space Invaders."
</br></br>
<img src="' . $download_dir . 'gemdropx.gif" width="240" height="300">
'
	),
	'zeldaroth' => array(
		'name' => 'zeldaroth',
		'title' => 'Zelda ROTH',
		'version' => '',
		'upstream' => 'http://www.zeldaroth.fr/us/zroth.php',
		'category' => 'Games',
		'summary' => 'Zelda Return Of The Hylian',
		'comment' => '
Story : After Link&apos;s victory over Ganon (in "A Link to the Past"), no
one knows what Link&apos;s wish to the Triforce was. But this wish reunified
the Light World and the Dark World and brought the 7 wise men&apos;s
descendants back to life. Peace was back in Hyrule. But unfortunately,
this wish also ressurected Ganon and his henchmen. He was preparing his
revenge, but he couldn&apos;t do anything without the Triforce. One night, a
familiar voice speaks to Link in his sleep?
</br></br>
This version includes some rework to select english/french texts
at runtime.
The patch makes it start in windowed mode; press CTRL+Return to toggle fullscreen.
</br></br>
<img src="' . $download_dir . 'zeldaroth.png" width="320" height="240">
'
	),
	'zeldansq' => array(
		'name' => 'zeldansq',
		'title' => 'Zelda NSQ',
		'version' => '',
		'upstream' => 'http://www.zeldaroth.fr/dlnsq.php',
		'category' => 'Games',
		'summary' => 'Zelda Navi&apos;s Quest',
		'comment' => '
Zelda Navi&apos;s Quest is an Open Source game.
</br></br>
Use the option dialog to select french dialogs. </br>
The patch makes it start in windowed mode; press CTRL+Return to toggle fullscreen.
</br></br>
<img src="' . $download_dir . 'zeldansq.png" width="400" height="300">
'
	),
	'zelda3t' => array(
		'name' => 'zelda3t',
		'title' => 'Zelda 3T',
		'version' => '',
		'upstream' => 'http://www.zeldaroth.us/z3t.php',
		'category' => 'Games',
		'summary' => 'Zelda Time To Triumph',
		'comment' => '
Story : After the events that occured in Termina and the victory of the
hero on his evil alter-ego, Zelda and Link knew that, from the bottom
of hell, Ganon the immortal drawed his power from his wish to the
Triforce, and rounded up his army with a view to invade Hyrule. Until
the day when, after months spent watching out for an attack, an event
came up and put an end to this endless waiting...
</br></br>
This version includes some rework to select english/french texts
at runtime.
</br></br>
The patch makes it start in windowed mode; press CTRL+Return to toggle fullscreen.
</br></br>
<img src="' . $download_dir . 'zelda3t.png" width="320" height="240">
'
	),
	'zeldapicross' => array(
		'name' => 'zeldapicross',
		'title' => 'Zelda Picross',
		'version' => '',
		'upstream' => 'http://www.zeldaroth.fr/us/dlpicross.php',
		'category' => 'Games',
		'summary' => 'Zelda Picross',
		'comment' => '
Scenario: Following a wish to the Triforce made by Ganon on a sad rainy
day, the kingdom of Hyrule changed into Picross grids. Gathering his
courage and his pencil, Link set off to try this new challenge.
</br></br>
This version includes some rework to select english/french texts
at runtime.
</br></br>
The patch makes it start in windowed mode; press CTRL+Return to toggle fullscreen.
</br></br>
<img src="' . $download_dir . 'zeldapicross.png" width="320" height="240">
'
	),
	'zeldaolb' => array(
		'name' => 'zeldaolb',
		'title' => 'Zelda OLB',
		'version' => '',
		'upstream' => 'http://www.zeldaroth.fr/us/dlolb.php',
		'category' => 'Games',
		'summary' => 'Zelda Oni Link Begins',
		'comment' => '
Story : Brought down by a terrible curse since his recent victory on
the Dark Lord, Link is changing, day by day, into a powerful creature
with a destructive nature named Oni-Link. Bannished from Hyrule, the
young hylian asks the princess Zelda some help. She shows him his last
hope: a portal to a secret world.
</br></br>
This version includes some rework to select english/french texts
at runtime.
</br></br>
The patch makes it start in windowed mode; press CTRL+Return to toggle fullscreen.
</br></br>
<img src="' . $download_dir . 'zeldaolb.jpg" width="320" height="240">
'
	),
	'gnurobbo' => array(
		'name' => 'gnurobbo',
		'title' => 'GNU Robbo',
		'version' => '0.66',
		'upstream' => 'https://gnurobbo.sourceforge.net/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'GNU Robbo',
		'comment' => '
GNU Robbo is a free open source reimplementation of Janusz Pelc&apos;s Robbo
(->) for the Atari XE/XL (->) which was distributed by LK Avalon (->)
in 1989.
</br></br>
<img src="' . $download_dir . 'gnurobbo.png" width="320" height="240">
'
	),
	'hcl' => array(
		'name' => 'hcl',
		'title' => 'Hydra Castle Labyrinth',
		'version' => '',
		'upstream' => 'https://github.com/ptitSeb/hydracastlelabyrinth/',
		'repo' => 'https://github.com/ptitSeb/hydracastlelabyrinth/',
		'category' => 'Games',
		'summary' => 'This version of Hydra Castle Labyrinth is based on the 3DS port',
		'comment' => '
SDL port of a fan-made port of Hydra Castle Labyrinth for 3DS.
</br></br>
Anything related to the PSP and Wii are unfinished.
</br>
(Yes, it does look like a 3rd grader programmed this.)
</br>
The game&apos;s originally done by E.Hashimoto (a.k.a. Buster). You can download some of his works <a href="http://hp.vector.co.jp/authors/VA025956/">here</a>.
</br></br>
<img src="' . $download_dir . 'hcl.png" width="400" height="240">
'
	),
	'hocoslamfy' => array(
		'name' => 'hocoslamfy',
		'version' => '',
		'upstream' => 'https://github.com/Nebuleon/hocoslamfy',
		'repo' => 'https://github.com/Nebuleon/hocoslamfy',
		'category' => 'Games',
		'summary' => 'You are a small bee and you must fly to avoid the bamboo shoots!',
		'comment' => '
hocoslamfy
</br></br>
You are a small bee and you must fly to avoid the bamboo shoots!
</br></br>
<img src="' . $download_dir . 'hocoslamfy.png" width="400" height="300">
'
	),
	'kobo-deluxe' => array(
		'name' => 'kobo-deluxe',
		'version' => '0.5.1',
		'upstream' => 'http://olofson.net/kobodl/',
		'category' => 'Games',
		'summary' => 'You are a small bee and you must fly to avoid the bamboo shoots!',
		'comment' => '
Kobo Deluxe is an enhanced version of Akira Higuchi&apos;s game XKobo for
Un*x systems with X11. Kobo Deluxe adds sound, smoother animation, high
resolution support, OpenGL acceleration (optional), an intuitive menu
driven user interface, joystick support and other features. Recent
versions also add a number of alternative skill levels with slightly
modernized gameplay.
</br></br>
If you use a screen depth &lt; 32bpp then pass -noalpha args to the bin.
You should try --help to get a complete list of args.
There&apos;s also the possibility to set the samplerate via arg -samplerate 24585...
</br></br>
<img src="' . $download_dir . 'kobo-deluxe.png" width="400" height="300">
'
	),
	'lmarbles' => array(
		'name' => 'lmarbles',
		'version' => '1.0.8',
		'upstream' => 'https://lgames.sourceforge.io/LMarbles/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'LMarbles is an Atomix clone with a slight change in concept',
		'comment' => '
LMarbles is an Atomix clone with a slight change in concept. Instead of
assembling molecules you create figures out of marbles. Nevertheless,
the basic game play is the same: If a marble starts to move it will not
stop until it hits a wall or another marble. To make it more
interesting there are obstacles like one-way streets, crumbling walls
and portals.</br>
As Marbles is meant as a puzzle game you play against a
move limit and not a time limit. This way you have as much time as you
need to think.

</br></br>
<img src="' . $download_dir . 'lmarbles.jpg" width="400" height="300">
'
	),
	'megamario' => array(
		'name' => 'megamario',
		'version' => '1.7',
		'upstream' => 'https://sourceforge.net/projects/mmario/',
		'category' => 'Games',
		'summary' => 'Mega Mario is a Super Mario Bros. 1 clone',
		'comment' => '
Mega Mario is a Super Mario Bros. 1 clone. It features everything the
original features - with better graphics, higher resolution, smoother
movement and new levels. The story of Mario and Luigi continues, in
old-school style. Also visit the <a href="http://www.megamario.de/">official HP</a>.
</br></br>
<img src="' . $download_dir . 'megamario.jpeg" width="320" height="240">
'
	),
	'metrocross' => array(
		'name' => 'metrocross',
		'version' => '',
		'upstream' => 'https://oldschoolprg.x10.mx/projets.php#metrocross',
		'source' => $download_dir . '%{name}.tar.xz',
		'category' => 'Games',
		'summary' => 'Another remake of a good little game from the Atari ST.',
		'comment' => '
Another remake of a good little game from the Atari ST. Score to beat: 401750 (^_^)
</br></br>
<img src="' . $download_dir . 'metrocross0.png">
'
	),
	'starfighter' => array(
		'name' => 'starfighter',
		'version' => '1.2',
		'upstream' => 'https://pr-starfighter.github.io/',
		'repo' => 'https://sourceforge.net/projects/pr-starfighter/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'Project: Starfighter is a space shoot &apos;em up game',
		'comment' => '
In the year 2579, the intergalactic weapons corporation, WEAPCO, has
dominated the galaxy. Guide Chris Bainfield and his friend Sid Wilson
on their quest to liberate the galaxy from the clutches of WEAPCO.
Along the way, you will encounter new foes, make new allies, and assist
local rebels in strikes against the evil corporation.
</br></br>
<img src="' . $download_dir . 'starfighter.png" width="320" height="240">
'
	),
	'openjazz' => array(
		'name' => 'openjazz',
		'title' => 'OpenJazz',
		'version' => '20231028',
		'upstream' => 'http://www.alister.eu/jazz/oj/',
		'repo' => 'https://github.com/AlisterT/openjazz',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'OpenJazz is a free, open-source version of the classic Jazz Jackrabbit games.',
		'comment' => '
OpenJazz is a free, open-source version of the classic Jazz Jackrabbit?
games.
</br></br>
To play, you will need the files from one of the original games
(shareware version included in the archive).
</br></br>
<img src="' . $download_dir . 'openjazz.png" width="320" height="200">
</br></br>
Another OpenJazz port for Atari: <a href="https://insane.tscc.de/">https://insane.tscc.de/</a>
'
	),
	'opentyrian' => array(
		'name' => 'opentyrian',
		'title' => 'OpenTyrian',
		'version' => '',
		'upstream' => 'http://www.alister.eu/jazz/oj/',
		'repo' => 'https://github.com/opentyrian/opentyrian/tree/sdl1',
		'category' => 'Games',
		'summary' => 'Tyrian is an arcade-style vertical scrolling shooter',
		'comment' => '
OpenTyrian is an open-source port of the DOS game Tyrian.
</br>
Tyrian is an arcade-style vertical scrolling shooter.  The story is set
in 20,031 where you play as Trent Hawkins, a skilled fighter-pilot employed
to fight MicroSol and save the galaxy.
</br>
Tyrian features a story mode, one- and two-player arcade modes, and networked
multiplayer.
</br></br>
To play, you will need the files from one of the original games
(freeware version included in the archive).
</br></br>
<img src="' . $download_dir . 'opentyrian.png" width="320" height="200">
'
	),
	'sdlbomber' => array(
		'name' => 'sdlbomber',
		'title' => 'SDL-Bomber',
		'version' => '1.0.4',
		'upstream' => 'https://github.com/HerbFargus/SDL-Bomber',
		'category' => 'Games',
		'summary' => 'A basic clone of the fantastic game Atomic Bomberman',
		'comment' => '
You&apos;ve got to blow up other players to win. Spacebar drops a bomb. Get away
and hope your enemy gets hit by the flame. The &apos;b&apos; key is a 2nd control
for when you are lucky enough to pick up the bomb control--looks like a
bomb with a timer on it. When you have that the bomb won&apos;t go off until
detonated by another bomb, you are killed, or you press &apos;b&apos;.
</br></br>
<img src="' . $download_dir . 'sdlbomber.png" width="320" height="200">
'
	),
	'gnuboy' => array(
		'name' => 'gnuboy',
		'version' => '1.0.4',
		'upstream' => 'https://github.com/rofl0r/gnuboy',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'gnuboy is one of the fastest GB/GBC emulator available.',
		'comment' => '
</br></br>
<img src="' . $download_dir . 'gnuboy.png" width="320" height="200">
</br></br>
Roms can be found for example on <a href="https://www.emulatorgames.net/roms/gameboy-color/">www.emulatorgames.net</a>
'
	),
	'stargun' => array(
		'name' => 'stargun',
		'version' => '0.2',
		'upstream' => 'https://stargun.sourceforge.net/',
		'category' => 'Games',
		'summary' => 'Stargun is a space shooter, vertical scroller game',
		'comment' => '
Stargun is a space shooter, vertical scroller game. It&apos;s platform
independent (or at least it is the objetive). The target OS are Windows
and Linux. There are plans to port Stargun to BeOs, FreeBSD and Amiga.
</br>
Stargun is written in C++ and uses SDL library.
</br></br>
<img src="' . $download_dir . 'stargun.png" width="320" height="300">
'
	),
	'symphyla' => array(
		'name' => 'symphyla',
		'version' => '',
		'upstream' => 'https://github.com/tondeur-h/symphyla/',
		'category' => 'Games',
		'summary' => 'A clone game (limited) of the Atari Centipede',
		'comment' => '
A clone game (limited) of the Atari Centipede under SDL 1.2 library
</br>
Work under Linux, not trested with other OS.
</br></br>
<img src="' . $download_dir . 'symphyla.png" width="320" height="240">
'
	),
	'tetris' => array(
		'name' => 'tetris',
		'version' => '',
		'upstream' => 'https://codes-sources.commentcamarche.net/source/51325-tetris-c-sdl',
		'category' => 'Games',
		'summary' => 'Another Tetris clone',
		'comment' => '
Little Tetris in C (no C++) and SDL. Works on Windows and Linux. I think it&apos;s pretty simple to "get into" the code.
</br></br>
<img src="' . $download_dir . 'tetris.png" width="320" height="240">
'
	),
	'ltris' => array(
		'name' => 'ltris',
		'version' => '1.2.7',
		'upstream' => 'https://lgames.sourceforge.io/LTris/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'LTris is a tetris clone',
		'comment' => '
LTris is a tetris clone. Pieces consisting of four blocks are dropping
down and need to be stacked in the playing field so that lines get
completed. Pieces can be shifted left/right or rotated. Completed lines
get removed. The more lines at once the more score you get. When the
next piece cannot be placed on top of the playing field the game ends.
</br>
There are different game modes (Normal: Regular game starting with an
empty playing field. Figures: Each level has a new figure that needs to
be cleared, later on new blocks and lines suddenly appear. Multiplayer:
You can play either against up to two other human or computer players.)
and two game styles (Classic: Follows the classic hardcore rules of NES
tetris. Modern: Adds stuff like 7-bag, piece shadow, lock delay, wall
kicks, ... for a more casual way to play).
</br></br>
<img src="' . $download_dir . 'ltris.jpg" width="320" height="240">
'
	),
	'xgalaga' => array(
		'name' => 'xgalaga',
		'version' => '2.1.1.0',
		'upstream' => 'http://rumsey.org/xgal.html',
		'repo' => 'https://github.com/frank-zago/xgalaga-sdl',
		'category' => 'Games',
		'summary' => 'Clone of the classic game Galaga',
		'comment' => '
Galaga is a game based on classic shoot &apos;em up games like Galaga and
Galaxian. The goal of the game is to destroy each wave of aliens while
avoiding the bullets they hurl your way. Each wave gets more and more
difficult, and you can only get hit once before losing a life.
</br></br>
<img src="' . $download_dir . 'xgalaga.png" width="300" height="400">
'
	),
	'jetpac' => array(
		'name' => 'jetpac',
		'version' => '0.2.5',
		'upstream' => 'https://web.archive.org/web/20060405190513/http://web.ukonline.co.uk/james.blewitt/jetpac.html',
		'category' => 'Games',
		'summary' => 'Jetpac - The Return is a remake of the original game Jetpac for the ZX Spectrum',
		'comment' => '
Jetpac - The Return is a remake of the original game Jetpac for the ZX
Spectrum and (I believe) the BBC.  The old version was about a space
man with a rocket pack who had to construct his rocket and fill it with
fuel before taking off to reach the next level.  It wasn&apos;t quite this
simple however because aliens and asteroids and all sorts of nasties
hindered the space man&apos;s mission.
</br>
This remake will attempt to stay true to the original formula whilst at
the same time improving the graphics and adding lots more baddies,
upgrades, features, levels etc, etc, etc.
</br></br>
<img src="' . $download_dir . 'jetpac.png" width="320" height="240">
'
	),
	'pegs' => array(
		'name' => 'pegs',
		'version' => '',
		'upstream' => 'http://aminet.net/package/game/think/pegs',
		'category' => 'Games',
		'summary' => 'SDL puzzle game',
		'comment' => '
The object of the game is to eliminate all of the blocks.
</br></br>
<img src="' . $download_dir . 'pegs.png" width="320" height="240">
'
	),
	'lgeneral' => array(
		'name' => 'lgeneral',
		'version' => '1.4.4',
		'title' => 'LGeneral',
		'upstream' => 'https://lgames.sourceforge.io/LGeneral/',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'LGeneral is a turn-based strategy engine heavily inspired by Panzer General',
		'comment' => '
LGeneral is a turn-based strategy engine heavily inspired by Panzer
General. You play single scenarios or whole campaigns turn by turn
against a human player or the AI. Entrenchment, rugged defense,
defensive fire, surprise contacts, surrender, unit supply, weather
influence, reinforcements and other implementations contribute to the
tactical and strategic depth of the game.
</br></br>
Converted data of <a href="' . $download_dir . 'pg-data.tar.gz">pg-data.tar.gz</a> of the original DOS version of Panzer General
is already included in the archive. The installation of the data is explained in the file README.lgc-pg.
</br></br>
Free stand-alone WWI scenario package by Steve McGuba, maintained by
Markus Koschany at Debian. Does not require conversion of original PG
Data: <a href="' . $download_dir . 'kukgen-data-1.1.1.zip">kukgen-data-1.1.1.zip</a>
</br></br>
<img src="' . $download_dir . 'lgeneral.jpg" width="320" height="240">
'
	),
	'cavestory' => array(
		'name' => 'cavestory',
		'version' => '1.0.0.6',
		'title' => 'Cave Story',
		'upstream' => 'https://www.cavestory.org/',
		'repo' => 'https://nxengine.sourceforge.io/',
		'category' => 'Games',
		'summary' => 'Cave Story is a Japanese freeware PC side-scrolling platformer game',
		'comment' => '
Cave Story, or Doukutsu Monogatari, is a Japanese freeware PC
side-scrolling platformer game developed by Studio Pixel. It has
been translated into English by Aeon Genesis Translations and has an
official translation for commercial releases such as Cave Story+.
</br></br>
<img src="' . $download_dir . 'cavestory.png" width="320" height="240">
</br>
Original MiNT-Patch by medmed.
'
	),
	'freecraft' => array(
		'name' => 'freecraft',
		'version' => '1.18',
		'upstream' => 'https://www.mobygames.com/game/72336/freecraft/',
		'category' => 'Games',
		'summary' => 'Freecraft is a free clone of Blizzard&apos;s famous realtime strategy game, WarCraft II.',
		'comment' => '
Freecraft is an open source 2D real-time top-down strategy game and a
clone of Warcraft II: Tides of Darkness. The engine allows users to
import Warcraft II files. The basic gameplay is almost identical to the
game that provided the inspiration. The player controls one of two
armies (Alliance and Mythical - based on humans and orcs), collects
resources (like gold and wood from mines and forests) with peasants,
builds farms and other buildings, and produces military units to
conquer enemies. The game has its own set of maps and new graphics.
</br></br>
<img src="' . $download_dir . 'freecraft.png" width="320" height="240">
</br>
Original MiNT-Patch by medmed.</br>
Data was orginally taken from <a href="http://dasixk.free.fr/freecraft-1.18.lzx">http://dasixk.free.fr/freecraft-1.18.lzx</a>
'
	),
	'vanilla-conquer' => array(
		'name' => 'vanilla-conquer',
		'version' => '',
		'repo' => 'https://github.com/TheAssemblyArmada/Vanilla-Conquer',
		'category' => 'Games',
		'summary' => 'Vanilla Conquer is a fully portable version of the first generation C&C engine ',
		'comment' => '
Vanilla Conquer is a fully portable version of the first generation C&amp;C
engine and is capable of running both Tiberian Dawn and Red Alert on
multiple platforms. It can also be used for mod development for the
Remastered Collection.
</br></br>
The main focus of Vanilla Conquer is to keep the default out-of-box
experience faithful to what the games were back when they were released
and work as a drop-in replacement for the original executables while
also providing bug fixes, compatiblity and quality of life
improvements.
</br></br>
<a href="' . $download_dir . 'tiberian-dawn-data.tar.xz">data needed for Tiberian Dawn</a> (GDI, NOD &amp; COVERTOPS discs) (~857MB).</br>
<a href="' . $download_dir . 'red-alert-data.tar.xz">data needed for Red Alert</a> (Allied, Soviet, Counterstrike &amp; Aftermath expansions) (~1033MB).</br>
'
	),
	'fanwor' => array(
		'name' => 'fanwor',
		'version' => '1.16',
		'upstream' => 'https://fanwor.tuxfamily.org/',
		'repo' => 'https://git.tuxfamily.org/fanwor/fanwor.git',
		'category' => 'Games',
		'summary' => 'Fanwor is an action-adventures in the style of the game "The Legend of Zelda"',
		'comment' => '
Fanwor is an action-adventures in the style of the game "The Legend of
Zelda" (&copy; by Nintendo). The source code of this game is available under
the terms of the GNU PUBLIC LICENSE version 2. A copy of this license
is included in the source code tarball.
</br></br>
Fanwor has originally been written for the "Magic Game Contest", a
programming contest held in 1999 for the now ancient Atari TOS
computers. Some years later, I&apos;ve adapted the source code to Linux,
using the SDL library as the graphical interface. Please note that the
game has been written very long ago, and there haven&apos;t been any more
real changes during the last years, so there are certainly better
Zelda-style action adventures available nowadays. This game is mainly
provided here for historical reasons. 
</br></br>
<img src="' . $download_dir . 'fanwor.png" width="320" height="240">
</br>
'
	),
	'ceferino' => array(
		'name' => 'ceferino',
		'version' => '0.97.8',
		'upstream' => 'https://web.archive.org/web/20160201062400/http://www.losersjuegos.com.ar/juegos/ceferino',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'Ceferino is fun game similar to "super pang"',
		'comment' => '
Ceferino is fun game similar to "super pang"
</br></br>
<img src="' . $download_dir . 'ceferino.jpg" width="320" height="240">
</br>
'
	),
	'afternoonstalker' => array(
		'name' => 'afternoonstalker',
		'version' => '1.1.6',
		'upstream' => 'http://perso.b2b2c.ca/~sarrazip/dev/afternoonstalker.html',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'Afternoon Stalker is a robot-killing video game.',
		'comment' => '
Afternoon Stalker is a robot-killing video game.  It is a clone of the 1982 Night Stalker video game for the Intellivision, from Mattel Electronics. 
</br></br>
<img src="' . $download_dir . 'afternoonstalker.png" width="320" height="240">
</br>
'
	),
	'batrachians' => array(
		'name' => 'batrachians',
		'version' => '0.1.7',
		'upstream' => 'http://perso.b2b2c.ca/~sarrazip/dev/batrachians.html',
		'source' => $download_dir . '%{name}-%{version}.tar.gz',
		'category' => 'Games',
		'summary' => 'Batrachians, a fly-eating frog video game',
		'comment' => '
Batrachians is a fly-eating frog video game. It is a clone of the 1982 Frog Bog video game for the Intellivision, from Mattel. 
</br></br>
<img src="' . $download_dir . 'batrachians.png" width="320" height="240">
</br>
'
	),
);

?>
