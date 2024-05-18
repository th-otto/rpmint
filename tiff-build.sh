#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=tiff
VERSION=-4.5.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/tiff/tiff-4.0.3-seek.patch
patches/tiff/tiff-4.0.3-compress-warning.patch
patches/tiff/tiff-disable-assertions.patch
patches/tiff/tiff-CVE-2023-0795.patch
patches/tiff/tiff-CVE-2023-0800.patch
"

# already applied in 4.10
DISABLED_PATCHES="
patches/tiff/tiff-4.0.9-bsc1046077-CVE-2017-9935.patch
patches/tiff/tiff-4.0.9-bsc1081690-CVE-2018-5784.patch
patches/tiff/tiff-CVE-2018-10963.patch
patches/tiff/tiff-CVE-2017-18013.patch
patches/tiff/tiff-CVE-2018-7456.patch
patches/tiff/tiff-CVE-2018-8905.patch
patches/tiff/tiff-CVE-2022-48281.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

unpack_archive

cd "$srcdir"

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config/config.sub

export LANG=POSIX
export LC_ALL=POSIX

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET}
	--prefix=${prefix}
	--sysconfdir=/etc
	--datadir=${prefix}/share
	--with-doc-dir=${prefix}/share/doc/${PACKAGENAME}
	--disable-nls
	--disable-shared
"

STACKSIZE="-Wl,-stack,128k"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		create_config_cache
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir/mfastcall
		${MAKE} $JOBS || exit 1
	
		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
		
		${MAKE} distclean >/dev/null
	fi

	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} distclean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
