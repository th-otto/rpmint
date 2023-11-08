#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=opkg
VERSION=-0.6.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/opkg/opkg-0.6.1.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

POST_INSTALL_SCRIPTS="
patches/opkg/opkg-20_migrate-feeds
patches/opkg/opkg-customfeeds.conf
patches/opkg/opkg-key
patches/opkg/opkg-smime.conf
patches/opkg/opkg.conf
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share
"

unpack_archive

cd "$MINT_BUILD_DIR"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" conf/config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix}
	--mandir=${prefix}/share/man
	--infodir=${prefix}/share/info
	--libdir=${prefix}/lib
	--sysconfdir=${TARGET_SYSCONFDIR}
	--localstatedir=/var
	--sharedstatedir=/var/lib
	--with-rundir=/var/run
	--docdir=${TARGET_PREFIX}/share/doc/packages/${PACKAGENAME}
	--enable-libopkg-api
	--enable-sha256
	--disable-shared
	--disable-python
	--disable-plugins
	--disable-gpg
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -DLUA_COMPAT_MODULE=1" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir
	: hack_lto_cflags

	rm -rf autom4te.cache config.h.in.orig

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}$multilibdir/charset.alias

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
