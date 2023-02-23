#!/bin/sh

unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

gpg_name=CC2E22F1B6492FD3EACFF8BF3C9569A568969A28

dir=$1
test "$dir" = "" && dir=/srv/www/htdocs/download/cygwin

scriptdir=${0%/*}
scriptdir=`cd "${scriptdir}"; pwd`

for ARCH in x86 x86_64 noarch; do
	cd "$dir" || exit 1
	
	for d in `find ${ARCH}/release -type d`; do
		cd "$dir/$d"
		files=`find -L . -maxdepth 1 ! -name sha512.sum -type f -printf '%P\n'`
		if test "$files" != ""; then
			sha512sum $files > sha512.sum
		fi
	done

	cd "$dir" || exit 1
	
	# our repo only contains the additional packages, so we have to disable dependency checks
	php $scriptdir/mksetupini.php --arch ${ARCH} --disable-check missing-depended-package || exit 1
# ~/cygwin/calm/calm-tool.sh mksetupini --arch ${ARCH} --inifile=${ARCH}/setup.ini --disable-check missing-depended-package --releasearea=.

    # compress and re-sign
	gpg --default-key ${gpg_name} --batch --yes --detach-sign ${ARCH}/setup.ini
	bzip2 -z -c ${ARCH}/setup.ini > ${ARCH}/setup.bz2
	gpg --default-key ${gpg_name} --batch --yes --detach-sign ${ARCH}/setup.bz2
	xz -z -c -6e ${ARCH}/setup.ini > ${ARCH}/setup.xz
	gpg --default-key ${gpg_name} --batch --yes --detach-sign ${ARCH}/setup.xz
	zstd -z -c -q ${ARCH}/setup.ini > ${ARCH}/setup.zst
	gpg --default-key ${gpg_name} --batch --yes --detach-sign ${ARCH}/setup.zst
	
	sha512sum ${ARCH}/setup* > ${ARCH}/sha512.sum
done
