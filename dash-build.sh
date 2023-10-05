#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=dash
VERSION=-0.5.12
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/dash/dash-mint.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"


BINFILES="
${TARGET_BINDIR#/}/*
bin/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"
autoreconf -fiv
cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

export LANG=POSIX
export LC_ALL=POSIX

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--enable-fnmatch \
	--enable-glob \
	--with-libedit \
"
STACKSIZE="-Wl,-stack,128k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	: hack_lto_cflags
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	mkdir -p ${THISPKG_DIR}${sysroot}/bin
	mv ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/dash ${THISPKG_DIR}${sysroot}/bin
	cd ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}
	rm -fv dash
	$LN_S ../../bin/dash dash
	
	cd ${MINT_BUILD_DIR}
	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
