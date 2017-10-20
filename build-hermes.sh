#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=Hermes
VERSION=-1.3.3
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES=""

PATCHES="
patches/hermes/Hermes-1.3.3-64bit.patch
patches/hermes/Hermes-1.3.3-debian.patch
patches/hermes/ns-recipe.patch
patches/hermes/warnings.patch
patches/hermes/mintelf-config.patch
"

unpack_archive

cd "$srcdir"

rm -rf autom4te.cache

# mark asm files as NOT needing execstack
for i in src/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done

cd "$MINT_BUILD_DIR"



COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags

	${MAKE} || exit 1
	# warning: this will try to install headers to /usr/include (no $DESTDIR used there)
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	# now install headers
	(cd src; ${MAKE} includedir="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/include" install-data-local)
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
