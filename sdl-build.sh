#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=SDL
VERSION=-1.2.16-git
#VERSIONPATCH=-20231222
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sdl/0001-Implement-gemlib-functions-that-are-needed-to-get-ri.patch
patches/sdl/0002-Implement-ldg-functions-that-are-needed-to-get-rid-o.patch
patches/sdl/0003-atari-filter-out-liconv-from-EXTRA_LDFLAGS-since-we-.patch
"
DISABLED_PATCHES="
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh acinclude/libtool.m4 acinclude/lt*
libtoolize --force || exit 1
aclocal -I acinclude || exit 1
autoconf || exit 1
#automake --force --copy --add-missing || exit 1

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build-scripts/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

enable_pth=false
CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-video-opengl
"
if $enable_pth; then
  # the configure script looks up the pth-config script
  mkdir -p bin
  touch bin/pth-config
  chmod 755 bin/pth-config
  export PATH="$PATH:$MINT_BUILD_DIR/bin"
  TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}-pth${VERSIONPATCH}
  CONFIGURE_FLAGS="$CONFIGURE_FLAGS --enable-threads --enable-pth"
else
  CONFIGURE_FLAGS="$CONFIGURE_FLAGS --disable-threads"
fi

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	LIBS="-lm" \
	${srcdir}/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	: hack_lto_cflags
	# ICONV isn't really used
	sed -i 's/ -liconv//' config.status
	./config.status

	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	rm -f "${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/sdl-config"
	
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done


move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
