#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=jpeg
VERSION=-8d
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

PATCHES="
patches/jpeg/jpeg-8d-0007-mintslb.patch 
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

srcarchive=${PACKAGENAME}src.v${VERSION#-}

unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"



COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared \
"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir/mfastcall ${CONFIGURE_FLAGS_AMIGAOS}
		${MAKE} $JOBS || exit 1
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
		${MAKE} distclean >/dev/null
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" "$srcdir/configure" ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	: hack_lto_cflags

	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	${MAKE} distclean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
