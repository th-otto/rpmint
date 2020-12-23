#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=unzip
VERSION=-6.0
VERSIONPATCH=
srcarchive="${PACKAGENAME}60"

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/unzip-config.dif
patches/${PACKAGENAME}/unzip-iso8859_2.patch
patches/${PACKAGENAME}/unzip-optflags.patch
patches/${PACKAGENAME}/unzip-5.52-filename_too_long.patch
patches/${PACKAGENAME}/unzip-no_file_name_translation.patch
patches/${PACKAGENAME}/unzip-open_missing_mode.patch
patches/${PACKAGENAME}/unzip-no-build-date.patch
patches/${PACKAGENAME}/unzip-dont_call_isprint.patch
patches/${PACKAGENAME}/unzip-Fix-CVE-2014-8139-unzip.patch
patches/${PACKAGENAME}/unzip-Fix-CVE-2014-8140-and-CVE-2014-8141.patch
patches/${PACKAGENAME}/unzip-CVE-2015-7696.patch
patches/${PACKAGENAME}/unzip-CVE-2015-7697.patch
patches/${PACKAGENAME}/unzip-CVE-2016-9844.patch
patches/${PACKAGENAME}/unzip-CVE-2014-9913.patch
patches/${PACKAGENAME}/unzip-CVE-2018-1000035.patch
patches/${PACKAGENAME}/unzip-atari-chmod-0.patch
patches/${PACKAGENAME}/unzip-symlinks.patch
"
# patches/unzip/unzip-5.52-use_librcc.patch


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
"

srcdir="$here/$srcarchive"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O3 -fomit-frame-pointer \
-D_GNU_SOURCE -DRCC_LAZY -DWILD_STOP_AT_DIR \
-DUNICODE_WCHAR -DNO_LCHMOD \
-DDATE_FORMAT=DF_YMD -I. -fno-strict-aliasing \
-DUSE_BZIP2 \
$LTO_CFLAGS"

export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} -f unix/Makefile prefix=${prefix} CC="${TARGET}-gcc" CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LD="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS" unix_make || exit 1
	${MAKE} -f unix/Makefile prefix=${prefix} CC="${TARGET}-gcc" CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LD="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS" L_BZ2=-lbz2 unzips || exit 1
	${MAKE} -f unix/Makefile prefix="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" MANDIR=${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1 \
		INSTALL=install INSTALL_D="install -d" install
	${MAKE} -f unix/Makefile clean
	(cd "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}"; rm -f zipinfo; $LN_S unzip zipinfo)
	make_bin_archive $CPU
done

make_archives
