#!/bin/sh

downloads=$HOME/webgo24/home/www/download/mint
date=20200102
here=`pwd`

TAR=${TAR-tar}
TAR_OPTS=${TAR_OPTS---owner=0 --group=0}

for sys in cygwin32 cygwin64 mingw32 linux macos; do
	d=`mktemp -d`
	for pkg in "gcc-4.6.4-mint-*-bin-$sys.tar.xz" \
		"binutils-2.33.1-mint-*-bin-$sys.tar.xz" \
		"binutils-2.33.1-mintelf-*-bin-$sys.tar.xz" \
		"mintbin-*-mint-*-bin-$sys.tar.xz" \
		"gcc-9.2.0-mint-*-bin-$sys.tar.xz" \
		"gcc-9.2.0-mintelf-*-bin-$sys.tar.xz" \
		"gemlib-*-mint-*-dev.tar.xz" \
		"gemlib-*-mintelf-*-dev.tar.xz" \
		"mintlib-*-mint-*-dev.tar.xz" \
		"mintlib-*-mintelf-*-dev.tar.xz" \
		"fdlibm-20200103-mint-dev.tar.xz" \
		"fdlibm-20200103-mintelf-dev.tar.xz" \
		"cflib-*-mint-*-dev.tar.xz" \
		"cflib-*-mintelf-*-dev.tar.xz" ; do
		file=`echo $downloads/$pkg 2>/dev/null`
		if test -f "$file"; then
			if test -s "$file"; then
				: echo "got $file"
				tar -C "$d" -xf "$file"
			else
				echo "empty: $file" >&2
			fi
		else
			echo "missing: $pkg" >&2
			exit 1
		fi
	done
	cd "$d"
	case $sys in
	mingw32)
		cp -ar usr/. mingw32/.
		rm -rf usr
		;;
	mingw64)
		cp -ar usr/. mingw64/.
		rm -rf usr
		;;
	macos)
		cp -ar usr/. opt/cross-mint/.
		rm -rf usr
		;;
	esac
	bigfile="$downloads/m68k-atari-mint-base-$date-$sys.tar.xz"
	${TAR} ${TAR_OPTS} -Jcf "$bigfile" *
	cd "$here"
	rm -rf "$d"
	echo "created $bigfile"
done
