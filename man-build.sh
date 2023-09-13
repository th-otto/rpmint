#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=man
VERSION=-1.5g
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/man/man-1.5a-manpath.patch
patches/man/man-1.5g-buildroot.patch
patches/man/man-1.5-manconf.patch
patches/man/man-1.5g-make.patch
patches/man/man-1.5g-mint.patch
"
DISABLED_PATHES="
"
POST_INSTALL_SCRIPTS="
patches/man/man-makewhatis.cronweekly
patches/man/man-makewhatis.crondaily
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/sbin/*
${TARGET_MANDIR#/}/man1/*
etc
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -D_GNU_SOURCE -DNONLS ${ELF_CFLAGS}"

CONFIGURE_FLAGS="-default +fsstnd +sgid"

./configure ${CONFIGURE_FLAGS}
sed -i 's/-Tlatin1/-Tascii/' conf_script
sed -i 's@usr/lib@etc@' conf_script
sed -i 's@/man\.conf@/man.config@' conf_script

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	${MAKE} CC="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" || exit 1

	mkdir -p  ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/bin
	mkdir -p  ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/man
	mkdir -p  ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/sbin
	mkdir -p  ${THISPKG_DIR}${sysroot}/etc/cron.daily
	mkdir -p  ${THISPKG_DIR}${sysroot}/etc/cron.weekly
	
	make install PREFIX=${THISPKG_DIR}${sysroot}
	
	# install -m 755 %{S:1} ${THISPKG_DIR}${sysroot}/etc/cron.weekly/makewhatis.cron
	# install -m 755 %{S:2} ${THISPKG_DIR}${sysroot}/etc/cron.daily/makewhatis.cron
	
	mkdir -p ${THISPKG_DIR}${sysroot}/var/catman
	mkdir -p ${THISPKG_DIR}${sysroot}/var/catman/local
	mkdir -p ${THISPKG_DIR}${sysroot}/var/catman/X11
	for i in 1 2 3 4 5 6 7 8 9 n; do
		mkdir -p ${THISPKG_DIR}${sysroot}/var/catman/cat$i
		mkdir -p ${THISPKG_DIR}${sysroot}/var/catman/local/cat$i
		mkdir -p ${THISPKG_DIR}${sysroot}/var/catman/X11R6/cat$i
	done
	
	# added man2html stuff
	cd man2html
	make install PREFIX=${THISPKG_DIR}${sysroot}
	cd ..
	
	# symlinks for manpath
	ln -sf man ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/manpath
	ln -sf man.1.gz ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/man/man1/manpath.1.gz


	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
