#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=krb5
VERSION=-1.15.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""

BINFILES="
${TARGET_BINDIR#/}/*
patches/krb5/krb5-1.12-pam.patch
patches/krb5/krb5-1.9-manpaths.dif
patches/krb5/krb5-1.12-buildconf.patch
patches/krb5/krb5-1.6.3-gssapi_improve_errormessages.dif
patches/krb5/krb5-1.6.3-ktutil-manpage.dif
patches/krb5/krb5-1.12-api.patch
patches/krb5/krb5-1.12-ksu-path.patch
patches/krb5/krb5-1.12-selinux-label.patch
patches/krb5/krb5-1.9-debuginfo.patch
"

MINT_BUILD_DIR="$srcdir/src"

unpack_archive

cd "$MINT_BUILD_DIR"

# needs to be re-generated
rm -f src/lib/krb5/krb/deltat.c

autoconf || exit 1
autoheader || exit 1
rm -rf autom4te.cache config.h.in.orig

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}/lib/mit \
--libdir=${prefix}/lib \
--includedir=${prefix}/include \
--sysconfdir=/etc \
--mandir=${prefix}/share/man \
--infodir=${prefix}/share/info \
--libexecdir=${prefix}/lib/mit/sbin \
--localstatedir=/var \
--localedir=${prefix}/share/locale \
--docdir=${prefix}/share/doc/${PACKAGENAME} \
--enable-dns-for-realm \
--disable-rpath \
--with-ldap \
--enable-pkinit \
--with-pkinit-crypto-impl=openssl \
--without-pam \
--disable-shared \
--enable-static \
--disable-thread-support \
--config-cache \
SS_LIB=-lss"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
krb5_cv_attr_constructor_destructor=yes
ac_cv_func_regcomp=yes
krb5_cv_system_ss_okay=yes
EOF
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	: hack_lto_cflags
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
