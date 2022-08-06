#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libyuv
VERSION=-1837
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/${PACKAGENAME}-1837-mint.patch
"
BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CC="${TARGET}-gcc" \
	CXX="${TARGET}-g++" \
	AR="${ar}" \
	ARFLAGS=rcs \
	RANLIB=${ranlib} \
	NM=${TARGET}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	${MAKE} -f linux.mk V=1 $JOBS || exit 1

	# there is no install target :/
	DESTDIR="${THISPKG_DIR}${sysroot}/usr"
	mkdir -p "$DESTDIR/bin" "$DESTDIR/include" "$DESTDIR/lib$multilibdir"
	cp -pr include/. "$DESTDIR/include"
	cp libyuv.a "$DESTDIR/lib$multilibdir"
	for i in i444tonv12_eg cpuid yuvconvert yuvconstants psnr; do
		cp $i "$DESTDIR/bin"
	done

	${MAKE} -f linux.mk clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
