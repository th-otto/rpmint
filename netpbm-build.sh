#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=netpbm
VERSION=-10.91.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/netpbm/netpbm-0000-make.patch
patches/netpbm/netpbm-0003-tmpfile.patch
patches/netpbm/netpbm-0004-security-code.patch
patches/netpbm/netpbm-0005-security-scripts.patch
patches/netpbm/netpbm-0006-gcc-warnings.patch
patches/netpbm/netpbm-0007-makeman-py3.patch
patches/netpbm/netpbm-0008-signed-char.patch
patches/netpbm/netpbm-0009-big-endian.patch
patches/netpbm/netpbm-0010-disable-jasper.patch
patches/netpbm/netpbm-0012-mint.patch
patches/netpbm/netpbm-namespace.patch
"
DISABLED_PATCHES="
patches/netpbm/netpbm-0001-asan.patch
patches/netpbm/netpbm-0011-pbmtonokia-cmdline-txt-null.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/netpbm
"

unpack_archive

cd "$srcdir"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS"
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -lm ${STACKSIZE}"

	# netpbm has _interactive_ configure perl script
	cp config.mk.in config.mk # recomended by upstream, see doc/INSTALL
	sed -i 's:NETPBMLIBTYPE = unixshared:NETPBMLIBTYPE = unixstatic:' config.mk
	sed -i 's:NETPBMLIBSUFFIX = so:NETPBMLIBSUFFIX = a:' config.mk
	sed -i 's:TIFFLIB = -ltiff:TIFFLIB = -ltiff -llzma -lzstd:' config.mk
	sed -i 's:PNGLIB = NONE:PNGLIB = -lpng -lz:' config.mk
	sed -i 's:STRIPFLAG = -s:STRIPFLAG =:' config.mk

	sed -i "s:CC = cc:CC = ${TARGET}-${GCC}:" config.mk
	sed -i "s:AR = ar:AR = ${ar}:" config.mk
	sed -i "s:RANLIB = ranlib:RANLIB = ${ranlib}:" config.mk
	sed -i "s:\#CFLAGS= -O2 -std1:CFLAGS = $CFLAGS:" config.mk
	sed -i "s:\#LDFLAGS += -noshare:LDFLAGS = $LDFLAGS:" config.mk
	sed -i 's:CC_FOR_BUILD = \$(CC):CC_FOR_BUILD = gcc:' config.mk
	sed -i 's:LD_FOR_BUILD = \$(LD):LD_FOR_BUILD = gcc:' config.mk
	sed -i 's:CFLAGS_FOR_BUILD = \$(CFLAGS_CONFIG):CFLAGS_FOR_BUILD = :' config.mk
	sed -i 's:LDFLAGS_FOR_BUILD = \$(LDFLAGS):LDFLAGS_FOR_BUILD = :' config.mk

	${MAKE} ${JOBS} || exit 1

	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/lib$multilibdir
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/lib/pkgconfig
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/include/netpbm
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/share/netpbm
	rm -rf package
	make pkgdir=`pwd`/package package
	
	rm -f package/bin/g3topbm # conflict with g3utils
	# rm -f package/bin/pstopnm # disable due security reasons, e. g. [bsc#1105592]
	mv  package/bin/* 		${THISPKG_DIR}${sysroot}${prefix}/bin
	mv	package/staticlink/*.a 	${THISPKG_DIR}${sysroot}${prefix}/lib$multilibdir
	mv	package/misc/* 		${THISPKG_DIR}${sysroot}${prefix}/share/netpbm

	sed -e "s/@VERSION@/${VERSION#-}/" -e 's/-I@INCLUDEDIR@//' -e 's/-L@LINKDIR@//' package/pkgconfig_template > ${THISPKG_DIR}${sysroot}${prefix}/lib/pkgconfig/netpbm.pc
	
	cp -prd package/include/netpbm/. 	${THISPKG_DIR}${sysroot}${prefix}/include/netpbm
	
	${MAKE} clean >/dev/null

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
