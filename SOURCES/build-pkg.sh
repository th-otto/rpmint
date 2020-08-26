#!/bin/sh

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
rpmbuild -bb ${spec}
rpmbuild --target m68k-atari-mint --define="buildtype 000" -bb ${spec}
rpmbuild --target m68020-atari-mint --define="buildtype 020" -bb ${spec}
rpmbuild --target m5475-atari-mint --define="buildtype v4e" -bb ${spec}

rm -rf "${topdir}/BUILD/${pkgname}"*
