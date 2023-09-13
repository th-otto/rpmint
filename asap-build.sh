#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=asap
VERSION=-5.0.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""

BINFILES="
${TARGET_BINDIR}/asapconv
"

unpack_archive

cd "$srcdir"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS} ${CFLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	${MAKE} V=1 \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	CC=${gcc} \
	AR=${ar} \
	RANLIB=${ranlib} \
	|| exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" prefix=${prefix} libdir='${prefix}/lib'$multilibdir install
	
	# we do not use "make clean" here because that removes files
	# which have to be rebuild using xasm
	rm -f *.o *.a asapconv

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
