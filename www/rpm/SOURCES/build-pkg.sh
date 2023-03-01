#!/bin/sh

quiet=
if test "$1" = "--quiet"; then
	quiet=--quiet
	shift
fi

pkgname="$1"
if test "${pkgname}" = ""; then
	echo "missing package name" >&2
	exit 1
fi

set -e

topdir=`rpm --eval '%{_topdir}'`

if test -f ${pkgname}.spec; then
	spec=${pkgname}.spec
else
	spec=${topdir}/SPECS/${pkgname}.spec
fi
rpmbuild $quiet -ba ${spec}
rpmbuild $quiet --target m68k-atari-mint --define="buildtype 000" -ba ${spec}
rpmbuild $quiet --target m68020-atari-mint --define="buildtype 020" -bb ${spec}
rpmbuild $quiet --target m5475-atari-mint --define="buildtype v4e" -bb ${spec}

rm -rf "${topdir}/BUILD/${pkgname}"*
