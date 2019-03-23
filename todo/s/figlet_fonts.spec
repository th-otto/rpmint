Summary: Fonts for Figlet
Name: figlet_fonts
Version: 1
Release: 1
Group: Applications/Text
Prefix: /usr
Source: %{name}-%{version}.tar
Copyright: public domain
BuildArchitectures: noarch
Vendor: Sparemint
Packager: Jan Krupka <jkrupka@volny.cz>
Prereq: figlet
BuildRoot: /var/tmp/figlet_fonts

%description
Additional fonts for Figlet package

%prep
%setup
%build
%install
mkdir -p $RPM_BUILD_ROOT/usr/games/lib/figlet.dir
mkdir -p $RPM_BUILD_ROOT/usr/doc/%{name}-%{version}
cp *fl[fc] $RPM_BUILD_ROOT/usr/games/lib/figlet.dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc eftichessChart eftiwall.txt eftiwall-chart.txt
/usr/games/lib/figlet.dir/acrobatic.flf
/usr/games/lib/figlet.dir/alligator.flf
/usr/games/lib/figlet.dir/alligator2.flf
/usr/games/lib/figlet.dir/alphabet.flf
/usr/games/lib/figlet.dir/avatar.flf
/usr/games/lib/figlet.dir/banner3-D.flf
/usr/games/lib/figlet.dir/banner3.flf
/usr/games/lib/figlet.dir/banner4.flf
/usr/games/lib/figlet.dir/barbwire.flf
/usr/games/lib/figlet.dir/basic.flf
/usr/games/lib/figlet.dir/bell.flf
/usr/games/lib/figlet.dir/bigchief.flf
/usr/games/lib/figlet.dir/binary.flf
/usr/games/lib/figlet.dir/broadway.flf
/usr/games/lib/figlet.dir/bulbhead.flf
/usr/games/lib/figlet.dir/calgphy2.flf
/usr/games/lib/figlet.dir/caligraphy.flf
/usr/games/lib/figlet.dir/catwalk.flf
/usr/games/lib/figlet.dir/coinstak.flf
/usr/games/lib/figlet.dir/colossal.flf
/usr/games/lib/figlet.dir/computer.flf
/usr/games/lib/figlet.dir/contessa.flf
/usr/games/lib/figlet.dir/contrast.flf
/usr/games/lib/figlet.dir/cosmic.flf
/usr/games/lib/figlet.dir/cosmike.flf
/usr/games/lib/figlet.dir/crawford.flf
/usr/games/lib/figlet.dir/cricket.flf
/usr/games/lib/figlet.dir/cyberlarge.flf
/usr/games/lib/figlet.dir/cybermedium.flf
/usr/games/lib/figlet.dir/cybersmall.flf
/usr/games/lib/figlet.dir/decimal.flf
/usr/games/lib/figlet.dir/diamond.flf
/usr/games/lib/figlet.dir/doh.flf
/usr/games/lib/figlet.dir/doom.flf
/usr/games/lib/figlet.dir/dotmatrix.flf
/usr/games/lib/figlet.dir/double.flf
/usr/games/lib/figlet.dir/drpepper.flf
/usr/games/lib/figlet.dir/eftifont.flf
/usr/games/lib/figlet.dir/eftichess.flf
/usr/games/lib/figlet.dir/eftipiti.flf
/usr/games/lib/figlet.dir/eftirobot.flf
/usr/games/lib/figlet.dir/eftitalic.flf
/usr/games/lib/figlet.dir/eftiwall.flf
/usr/games/lib/figlet.dir/eftiwater.flf
/usr/games/lib/figlet.dir/epic.flf
/usr/games/lib/figlet.dir/fender.flf
/usr/games/lib/figlet.dir/fourtops.flf
/usr/games/lib/figlet.dir/fuzzy.flf
/usr/games/lib/figlet.dir/goofy.flf
/usr/games/lib/figlet.dir/gothic.flf
/usr/games/lib/figlet.dir/graffiti.flf
/usr/games/lib/figlet.dir/hex.flf
/usr/games/lib/figlet.dir/hollywood.flf
/usr/games/lib/figlet.dir/chunky.flf
/usr/games/lib/figlet.dir/invita.flf
/usr/games/lib/figlet.dir/isometric1.flf
/usr/games/lib/figlet.dir/isometric2.flf
/usr/games/lib/figlet.dir/isometric3.flf
/usr/games/lib/figlet.dir/isometric4.flf
/usr/games/lib/figlet.dir/italic.flf
/usr/games/lib/figlet.dir/jazmine.flf
/usr/games/lib/figlet.dir/katakana.flf
/usr/games/lib/figlet.dir/kban.flf
/usr/games/lib/figlet.dir/larry3d.flf
/usr/games/lib/figlet.dir/lcd.flf
/usr/games/lib/figlet.dir/letters.flf
/usr/games/lib/figlet.dir/linux.flf
/usr/games/lib/figlet.dir/lockergnome.flf
/usr/games/lib/figlet.dir/lower.flc
/usr/games/lib/figlet.dir/madrid.flf
/usr/games/lib/figlet.dir/marquee.flf
/usr/games/lib/figlet.dir/maxfour.flf
/usr/games/lib/figlet.dir/mike.flf
/usr/games/lib/figlet.dir/mirror.flf
/usr/games/lib/figlet.dir/nancyj-fancy.flf
/usr/games/lib/figlet.dir/nancyj.flf
/usr/games/lib/figlet.dir/nancyj-underlined.flf
/usr/games/lib/figlet.dir/nipples.flf
/usr/games/lib/figlet.dir/null.flc
/usr/games/lib/figlet.dir/octal.flf
/usr/games/lib/figlet.dir/ogre.flf
/usr/games/lib/figlet.dir/os2.flf
/usr/games/lib/figlet.dir/o8.flf
/usr/games/lib/figlet.dir/pawp.flf
/usr/games/lib/figlet.dir/peaks.flf
/usr/games/lib/figlet.dir/pebbles.flf
/usr/games/lib/figlet.dir/pepper.flf
/usr/games/lib/figlet.dir/poison.flf
/usr/games/lib/figlet.dir/puffy.flf
/usr/games/lib/figlet.dir/pyramid.flf
/usr/games/lib/figlet.dir/rectangles.flf
/usr/games/lib/figlet.dir/relief.flf
/usr/games/lib/figlet.dir/relief2.flf
/usr/games/lib/figlet.dir/rev.flf
/usr/games/lib/figlet.dir/roman.flf
/usr/games/lib/figlet.dir/rot13.flc
/usr/games/lib/figlet.dir/rot13.flf
/usr/games/lib/figlet.dir/rounded.flf
/usr/games/lib/figlet.dir/rowancap.flf
/usr/games/lib/figlet.dir/rozzo.flf
/usr/games/lib/figlet.dir/sblood.flf
/usr/games/lib/figlet.dir/serifcap.flf
/usr/games/lib/figlet.dir/short.flf
/usr/games/lib/figlet.dir/slide.flf
/usr/games/lib/figlet.dir/slscript.flf
/usr/games/lib/figlet.dir/smisome1.flf
/usr/games/lib/figlet.dir/smkeyboard.flf
/usr/games/lib/figlet.dir/speed.flf
/usr/games/lib/figlet.dir/stacey.flf
/usr/games/lib/figlet.dir/stampatello.flf
/usr/games/lib/figlet.dir/starwars.flf
/usr/games/lib/figlet.dir/stellar.flf
/usr/games/lib/figlet.dir/stop.flf
/usr/games/lib/figlet.dir/straight.flf
/usr/games/lib/figlet.dir/swap.flc
/usr/games/lib/figlet.dir/tanja.flf
/usr/games/lib/figlet.dir/thick.flf
/usr/games/lib/figlet.dir/thin.flf
/usr/games/lib/figlet.dir/threepoint.flf
/usr/games/lib/figlet.dir/ticks.flf
/usr/games/lib/figlet.dir/ticksslant.flf
/usr/games/lib/figlet.dir/tinker-toy.flf
/usr/games/lib/figlet.dir/tombstone.flf
/usr/games/lib/figlet.dir/trek.flf
/usr/games/lib/figlet.dir/twopoint.flf
/usr/games/lib/figlet.dir/univers.flf
/usr/games/lib/figlet.dir/usaflag.flf
/usr/games/lib/figlet.dir/weird.flf
/usr/games/lib/figlet.dir/whimsy.flf
/usr/games/lib/figlet.dir/3-d.flf
/usr/games/lib/figlet.dir/3x5.flf
/usr/games/lib/figlet.dir/5lineoblique.flf

%changelog
* Thu Oct 29 2001 Jan Krupka <jkrupka@volny.cz>
- first release for SpareMiNT (new package)
