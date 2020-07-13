#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=coreutils
VERSION=-8.28
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/coreutils/coreutils-i18n.patch
patches/coreutils/coreutils-sysinfo.patch
patches/coreutils/coreutils-invalid-ids.patch
patches/coreutils/coreutils-getaddrinfo.patch
patches/coreutils/coreutils-misc.patch
patches/coreutils/coreutils-skip-some-sort-tests-on-ppc.patch
patches/coreutils/coreutils-skip-gnulib-test-tls.patch
patches/coreutils/coreutils-tests-shorten-extreme-factor-tests.patch
patches/coreutils/coreutils-disable_tests.patch
patches/coreutils/coreutils-test_without_valgrind.patch
patches/coreutils/sh-utils-2.0-getgid.patch
patches/coreutils/sh-utils-2.0-mint.patch
patches/coreutils/coreutils-mint-physmem.patch
patches/coreutils/dummy-man-patch
patches/coreutils/coreutils-mint-mountlist.patch
patches/coreutils/coreutils-mint-procfile.patch
patches/coreutils/mintelf-config.patch
"

# patches/coreutils/coreutils-remove_hostname_documentation.patch
# patches/coreutils/coreutils-remove_kill_documentation.patch
# patches/coreutils/coreutils-build-timeout-as-pie.patch

BINFILES="
${TARGET_BINDIR#/}/*
bin/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4

aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# patch it again in case it was replaced by autoreconf
patch -p1 -i ${BUILD_DIR}/patches/coreutils/mintelf-config.patch || :

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--enable-install-program=arch,kill \
	--localstatedir=/var/run \
	DEFAULT_POSIX2_VERSION=200112 \
	alternative=199209 \
	--config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,256k"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/find'$multilibexecdir

	hack_lto_cflags

	${MAKE} ${JOBS} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	

	mkdir -p ${THISPKG_DIR}${sysroot}/bin
	cd ${THISPKG_DIR}${sysroot}/bin
	for i in arch kill basename cat chgrp chmod chown cp date dd df echo \
	  false ln ls mkdir mknod mktemp mv pwd rm rmdir sleep sort stat \
	  stty sync touch true uname readlink md5sum
	do
	  rm -f $i
	  $LN_S ../usr/bin/$i $i
	done

	# don't supply chroot under MiNT
	cd ${THISPKG_DIR}${sysroot}${prefix}/bin
	rm -f chroot

	# rename hostname so it don't conflict with the hostname rpm
	test ! -x hostname || mv hostname hostname.gnu
	
	# don't ship su; it's in shadow-utils
	rm -f su

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
