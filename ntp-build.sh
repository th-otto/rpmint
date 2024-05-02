#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ntp
VERSION=-4.2.8p17
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/ntp-segfault_on_invalid_device.patch
patches/${PACKAGENAME}/ntp-strcat.patch
patches/${PACKAGENAME}/ntp-4.2.6p2-seed_file.patch
patches/${PACKAGENAME}/ntp-bnc#506908.patch
patches/${PACKAGENAME}/ntp-MOD_NANO.patch
patches/${PACKAGENAME}/ntp-bnc#574885.patch
patches/${PACKAGENAME}/ntp-openssl-version.patch
patches/${PACKAGENAME}/ntp-netlink.patch
patches/${PACKAGENAME}/ntp-move-kod-file.patch
patches/${PACKAGENAME}/ntp-sntp-libevent.patch
patches/${PACKAGENAME}/ntp-testdcf-gude.patch
patches/${PACKAGENAME}/ntp-clarify-interface.patch
patches/${PACKAGENAME}/ntp-mint.patch
"
DISABLED_PATCHES="
patches/${PACKAGENAME}/ntp-pathfind.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
patches/${PACKAGENAME}/ntptime.8.gz
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
${TARGET_PREFIX#/}/share/doc/ntp
${TARGET_PREFIX#/}/share/doc/sntp
${TARGET_PREFIX#/}/share/ntp
var/lib/ntp
"

unpack_archive

cd "$MINT_BUILD_DIR"
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" sntp/libevent/build-aux/config.sub
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" sntp/libevent/config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--with-yielding-select=yes
	--disable-shared
	--with-hardenfile=/dev/null
	--without-threads
"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} $JOBS || exit 1
	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install || exit 1

	mkdir -p "${buildroot}/var/lib/ntp"
	touch "${buildroot}/var/lib/ntp/kod"
	
	${MAKE} clean
	make_bin_archive $CPU
done

make_archives
