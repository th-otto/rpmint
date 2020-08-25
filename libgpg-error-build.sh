#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libgpg-error
VERSION=-1.28
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}
"

PATCHES="
patches/libgpg-error/libgpg-error-fix_aarch64.patch
patches/libgpg-error/libgpg-error-mint.patch
patches/libgpg-error/libgpg-error-mintelf-config.patch
"

unpack_archive

cd "$MINT_BUILD_DIR"

./autogen.sh

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	rm -f ${TARGET_BINDIR#/}/gpg-error-config
	rm -f ${TARGET_BINDIR#/}/gpgrt-config
	# remove useless manpage for gpg-error-config
	rm -rf ${TARGET_PREFIX#/}/share/man
	make_bin_archive $CPU
done

# create pkg-config file
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig
cat > ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig/${PACKAGENAME}.pc <<-EOF
prefix=${TARGET_PREFIX}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: ${PACKAGENAME}
Description: Libgpg-error is a small library that originally defined common error values for all GnuPG components
Version: ${VERSION#-}
URL: http://www.gnupg.org/

Libs: -lgpg-error
Cflags:
EOF

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
