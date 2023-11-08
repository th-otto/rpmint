#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=curl
VERSION=-7.56.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/curl-dont-mess-with-rpmoptflags.diff
patches/${PACKAGENAME}/curl-mint-build.patch
patches/${PACKAGENAME}/curl-secure-getenv.patch
patches/${PACKAGENAME}/curl-staticlibs.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"
# patches/curl/curl-libcurl-ocloexec.patch
# patches/curl/curl-man3.patch
# patches/curl/curl-ppc-build.patch
# patches/curl/curl-http-Don-t-wait-on-CONNECT-when-there-is-no-proxy.patch

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man3/*
${TARGET_PREFIX#/}/share/aclocal
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp $BUILD_DIR/patches/automake/mintelf-config.sub config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

with_openssl=true

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} \
--disable-ipv6 \
--with-gssapi=${TARGET_LIBDIR}/mit \
--with-libidn2 \
--with-libssh2 \
--with-libmetalink \
--disable-shared \
--enable-static \
--disable-threaded-resolver"

if $with_openssl; then
	CONFIGURE_FLAGS+="
	--with-ssl
	--with-ca-fallback
	--without-ca-path
	--without-ca-bundle"
else
	CONFIGURE_FLAGS+=" --without-ssl"
fi

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	: hack_lto_cflags
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	rm -f ${TARGET_BINDIR#/}/curl-config
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
