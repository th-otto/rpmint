#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=wget
VERSION=-1.21.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/wget/wget-wgetrc.patch
patches/wget/wget-libproxy.patch
patches/wget/wget-1.14-no-ssl-comp.patch
patches/wget/wget-fix-pod-syntax.patch
patches/wget/wget-errno-clobber.patch
patches/wget/wget-remove-env-from-shebang.patch
patches/wget/wget-do-not-propagate-credentials.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"

BINFILES="
etc/wgetrc
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/man/*/*
"

unpack_archive

cd "$srcdir"

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--sysconfdir=/etc
	--disable-nls
	--disable-threads
	--with-ssl=openssl
	--with-cares
	--without-metalink
	--config-cache
"
STACKSIZE="-Wl,-stack,128k"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
EOF
	append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/find'$multilibexecdir

	sed -i 's/\/usr\/bin\/env perl -w/\/usr\/bin\/perl -w/' util/rmold.pl

	echo '#undef HAVE_PTHREAD_H' >> src/config.h
	echo "#undef HAVE_PTHREAD_API" >> src/config.h
	echo "#undef HAVE_PTHREAD_MUTEX_RECURSIVE" >> src/config.h
	echo "#undef HAVE_PTHREAD_RWLOCK" >> src/config.h
	echo "#undef SIZEOF_PTHREAD_MUTEX_T" >> src/config.h
	echo "#undef USE_POSIX_THREADS" >> src/config.h
	echo "#undef SETLOCALE_NULL_ALL_MTSAFE" >> src/config.h
	echo "#define SETLOCALE_NULL_ALL_MTSAFE 1" >> src/config.h
	echo "#undef SETLOCALE_NULL_ONE_MTSAFE" >> src/config.h
	echo "#define SETLOCALE_NULL_ONE_MTSAFE 1" >> src/config.h
	
	: hack_lto_cflags

	${MAKE} ${JOBS} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
