#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ca-certificates
VERSION=-10b2785
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES=""
# make-ca.sh from http://anduin.linuxfromscratch.org/BLFS/other/make-ca.sh-20170119
# certdata.txt from http://anduin.linuxfromscratch.org/BLFS/other/certdata.txt
POST_INSTALL_SCRIPTS="
patches/ca-certificates/make-ca.sh
patches/ca-certificates/certdata.txt
"

BINFILES="
etc/*
var/*
${TARGET_LIBDIR#/}/*
${TARGET_PREFIX#/}/share
${TARGET_PREFIX#/}/sbin/*
${TARGET_MANDIR#/}/man8/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -Wall ${ELF_CFLAGS}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

cd "$MINT_BUILD_DIR"

buildroot="${THISPKG_DIR}${sysroot}"
${MAKE} DESTDIR="${buildroot}" install

ssletcdir=${TARGET_SYSCONFDIR#/}/ssl
sslcerts=${ssletcdir}/certs
cabundle=var/lib/ca-certificates/ca-bundle.pem
trustdir_cfg=${TARGET_SYSCONFDIR#/}/pki/trust
trustdir_static=${TARGET_PREFIX#/}/share/pki/trust

cd "${buildroot}"
install -d -m 755 ${trustdir_cfg}/{anchors,blacklist}
install -d -m 755 ${trustdir_static}/{anchors,blacklist}
install -d -m 755 ${ssletcdir}
install -d -m 755 ${TARGET_SYSCONFDIR#/}/ca-certificates/update.d
install -d -m 755 ${TARGET_PREFIX#/}/lib/ca-certificates/update.d
install -d -m 555 var/lib/ca-certificates/pem
install -d -m 555 var/lib/ca-certificates/openssl
install -d -m 755 ${TARGET_PREFIX#/}/lib/systemd/system
ln -s /var/lib/ca-certificates/pem ${sslcerts}
install -D -m 644 /dev/null ${cabundle}
ln -s /${cabundle} ${ssletcdir}/ca-bundle.pem
install -D -m 644 /dev/null var/lib/ca-certificates/java-cacerts

# should be done in git.
mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,50}java.run
mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,70}openssl.run
mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,80}etc_ssl.run
# certbundle.run must be run after etc_ssl.run as it uses a timestamp from it
mv ${TARGET_PREFIX#/}/lib/ca-certificates/update.d/{,99}certbundle.run

make_bin_archive noarch

move_prefix
configured_prefix="${prefix}"

make_archives
