#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=dhcp
VERSION=-3.0.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/dhcp/dhcp-3.0.3-mint-20111009.patch
"

# patches/dhcp/0001-dhcp-4.1.1-default-paths.patch
# patches/dhcp/0002-dhcp-4.1.1-paranoia.patch
# patches/dhcp/0003-dhcp-4.2.2-man-includes.patch
# patches/dhcp/0004-dhcp-4.1.1-tmpfile.patch
# patches/dhcp/0005-dhcp-4.1.1-dhclient-exec-filedes.patch
# patches/dhcp/0006-dhcp-4.3.2-dhclient-send-hostname-or-fqdn.patch
# patches/dhcp/0007-dhcp-4.1.1-P1-lpf-bind-msg-fix.patch
# patches/dhcp/0009-dhcp-4.2.6-close-on-exec.patch
# patches/dhcp/0010-dhcp-4.2.2-quiet-dhclient.patch
# patches/dhcp/0011-Fixed-linux-interface-discovery-using-getifaddrs.patch
# patches/dhcp/0013-dhcp-4.2.x-dhcpv6-decline-on-DAD-failure.872609.patch
# patches/dhcp/0015-Expose-next-server-DHCPv4-option-to-dhclient-script.patch
# patches/dhcp/0016-infiniband-support.patch
# patches/dhcp/0017-server-no-success-report-before-send.919959.patch
# patches/dhcp/0018-client-fail-on-script-pre-init-error-bsc-912098.patch
# patches/dhcp/0019-dhcp-4.2.4-P1-interval.patch
# patches/dhcp/0020-dhcp-4.x.x-fixed-improper-lease-duration-checking.patch
# patches/dhcp/dhcp-4.3-mint.patch


BINFILES="
sbin/*
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/sbin/*
"

MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$srcdir"

sed -i 's:^#sysname=\$1$:sysname=freemint:g' configure
sed -i 's:^\tar :\t$(AR) :g' */Makefile.dist
sed -i 's:^CROSSPREFIX=\(.*\):CROSSPREFIX='${TARGET}-':' Makefile.conf

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

with_ldap=false
with_ldapcase=false
CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--disable-dhcpv6 \
	--enable-failover \
	--enable-paranoia \
	--enable-early-chroot \
	--with-cli-pid-file=/var/run/dhclient.pid \
	--with-cli-lease-file=/var/lib/dhcp/dhclient.leases \
	--with-cli6-pid-file=/var/run/dhclient6.pid \
	--with-cli6-lease-file=/var/lib/dhcp6/dhclient.leases \
	--with-srv-pid-file=/var/run/dhcpd.pid \
	--with-srv-lease-file=/var/lib/dhcp/db/dhcpd.leases \
	--with-srv6-pid-file=/var/run/dhcpd6.pid \
	--with-srv6-lease-file=/var/lib/dhcp6/db/dhcpd6.leases \
"
if $with_ldap; then
	CONFIGURE_FLAGS="${CONFIGURE_FLAGS} --with-ldap --with-ldapcrypto"
	if $with_ldapcasa; then
		CONFIGURE_FLAGS="${CONFIGURE_FLAGS} --with-ldapcasa"
	fi
fi

cat <<EOF >> site.conf
USERBINDIR=${TARGET_BINDIR}
BINDIR=${TARGET_PREFIX}/sbin
LIBDIR = ${TARGET_LIBDIR}
INCDIR = ${TARGET_PREFIX}/include
CLIENTBINDIR=/sbin
ADMMANDIR = ${TARGET_MANDIR}/cat8
ADMMANEXT = .8
FFMANDIR = ${TARGET_MANDIR}/cat5
FFMANEXT = .5
LIBMANDIR = ${TARGET_MANDIR}/cat3
LIBMANEXT = .3
USRMANDIR = ${TARGET_MANDIR}/cat1
USRMANEXT = .1
EOF

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	./configure ${CONFIGURE_FLAGS}
	M68K_ATARI_MINT_CFLAGS="${CPU_CFLAGS} $COMMON_CFLAGS ${LTO_CFLAGS} ${STACKSIZE}" CROSSPREFIX="${TARGET}-" ${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	mkdir -p ${THISPKG_DIR}${sysroot}/sbin
	install -m 755 work.freemint/server/dhcpd ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/sbin
	install -m 755 work.freemint/relay/dhcrelay ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/sbin
	${MAKE} clean > /dev/null
	make_bin_archive $CPU
done

make_archives
