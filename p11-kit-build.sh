#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=p11-kit
VERSION=-0.23.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/p11-kit/p11-kit-biarch.patch
"

BINFILES="
${TARGET_SYSCONFDIR#/}/*
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/*
${TARGET_PREFIX#/}/share/*
${TARGET_PREFIX#/}/libexec/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

autoreconf -f -i || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer -Wall"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--disable-shared \
	--localstatedir=/var/lib \
	--config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

make_args=""

pkidir_cfg=${TARGET_SYSCONFDIR}/pki
pkidir_static=${TARGET_PREFIX}/share/pki
trustdir_cfg=${pkidir_cfg}/trust
trustdir_static=${pkidir_static}/trust

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	STACKSIZE="-Wl,-stack,128k"

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--with-trust-paths=${trustdir_cfg}:${trustdir_static} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1
	
	all_make_args="${make_args} privatedir=${prefix}/libexec/${PACKAGENAME}$multilibexecdir"
	hack_lto_cflags

	${MAKE} ${all_make_args} || exit 1

	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} ${all_make_args} DESTDIR="${buildroot}" install
	
	${MAKE} ${all_make_args} clean >/dev/null

	install -d m 755 ${buildroot}${trustdir_cfg}/{anchors,blacklist}
	install -d m 755 ${buildroot}${trustdir_static}/{anchors,blacklist}
	install -d ${buildroot}${TARGET_SYSCONFDIR}/pkcs11/modules
	rm ${buildroot}%{TARGET_SYSCONFDIR}/pkcs11/pkcs11.conf.example

	install -d -m 755 ${buildroot}${_sysconfdir}/rpm/
cat <<'FIN' >${buildroot}${TARGET_SYSCONFDIR}/rpm/macros.${PACKAGENAME}
# Macros from p11-kit package
%pkidir_cfg             %{pkidir_cfg}
%pkidir_static          %{pkidir_static}
%trustdir_cfg           %{trustdir_cfg}
%trustdir_static        %{trustdir_static}
FIN
	ln -s ${TARGET_LIBDIR}/pkcs11/p11-kit-trust.so ${buildroot}${TARGET_LIBDIR}/libnssckbi.so
	rm ${buildroot}%{_libexecdir}/%{name}/trust-extract-compat
	ln -s ../../sbin/update-ca-certificates ${buildroot}${prefix}/libexec/${PACKAGENAME}/p11-kit-extract-trust

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
