#!/bin/sh

unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

scriptdir=${0%/*}
scriptdir=`cd "${scriptdir}"; pwd`

cd /srv/www/htdocs/cygtest || exit 1

for ARCH in x86 x86_64 noarch; do
	php $scriptdir/mksetupini.php --arch ${ARCH} --releasearea=. || exit 1
	bzip2 -k ${ARCH}/setup.ini
	xz -6e -k ${ARCH}/setup.ini
done
