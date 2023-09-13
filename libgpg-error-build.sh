#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libgpg-error
VERSION=-1.46
VERSIONPATCH=

. ${scriptdir}/functions.sh


BINFILES="
${TARGET_BINDIR#/}
"

PATCHES="
patches/libgpg-error/libgpg-error-mint.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

unpack_archive

cd "$MINT_BUILD_DIR"

./autogen.sh

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" build-aux/config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared --disable-threads"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	: hack_lto_cflags
	echo '#undef HAVE_PTHREAD_H' >> config.h
	echo "#undef HAVE_PTHREAD_API" >> config.h
	echo "#undef HAVE_PTHREAD_MUTEX_RECURSIVE" >> config.h
	echo "#undef HAVE_PTHREAD_RWLOCK" >> config.h
	echo "#undef SIZEOF_PTHREAD_MUTEX_T" >> config.h
	echo "#undef USE_POSIX_THREADS" >> config.h

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	rm -f ${TARGET_BINDIR#/}/gpg-error-config
	rm -f ${TARGET_BINDIR#/}/gpgrt-config
	# remove useless manpage for gpg-error-config
	rm -rf ${TARGET_PREFIX#/}/share/man/*/gpg-error-config*
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
