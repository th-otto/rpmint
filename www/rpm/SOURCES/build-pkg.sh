#!/bin/sh

quiet=
nodeps=
valgrind=
target=m68k-atari-mint
while test $# -gt 0; do
	case $1 in
	--quiet)
		quiet=--quiet
		shift
		;;
	--nodeps)
		nodeps=--nodeps
		shift
		;;
	--valgrind)
		valgrind=valgrind
		shift
		;;
	--elf)
		target=m68k-atari-mintelf
		shift
		;;
	--*)
		echo "unknown option $1" >&2
		exit 1
		;;
	*)
		pkgname="$1"
		shift
		;;
	esac
done

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

case ${pkgname} in
gnucobol*)
	# gnucobol is not a cross-compiler
	;;
*)
	$valgrind rpmbuild $quiet $nodeps --define="_rpmint_target $target" -ba ${spec}
	;;
esac
$valgrind rpmbuild $quiet --nodeps --define="_rpmint_target $target" --target m68k-atari-mint --define="buildtype 000" -ba ${spec}
$valgrind rpmbuild $quiet --nodeps --define="_rpmint_target $target" --target m68020-atari-mint --define="buildtype 020" -bb ${spec}
$valgrind rpmbuild $quiet --nodeps --define="_rpmint_target $target" --target m5475-atari-mint --define="buildtype v4e" -bb ${spec}

rm -rf "${topdir}/BUILD/${pkgname}"*
