#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=x3270
VERSION=-4.2ga9
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/x3270-mknod.patch
patches/${PACKAGENAME}/x3270-usr_local_bin.patch
patches/${PACKAGENAME}/x3270-mint.patch
"

EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
etc/x3270/*
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
${TARGET_PREFIX#/}/share/fonts/X11/misc/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"
export LIBX3270DIR=/etc/x3270
CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=${TARGET_PREFIX}/share/doc/packages/%{pkgname}
	--enable-c3270
	--enable-x3270
	--enable-s3270
	--enable-b3270
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	LIBS="-lSM -lICE -lXpm -lXext -lX11 -lz" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	${MAKE} ${JOBS} LIBX3270DIR=${LIBX3270DIR} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" LIBX3270DIR=${LIBX3270DIR} install
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" LIBX3270DIR=${LIBX3270DIR} install.man
	
	# make install does a mkfontdir, that creates a fonts.dir we don't
	# want in the package.  remove that:
	rm -f ${THISPKG_DIR}${sysroot}/${TARGET_PREFIX}/share/fonts/X11/misc/fonts.dir

	${MAKE} clean >/dev/null
	rm -rf obj

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
make_archives
