#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=sed
VERSION=-4.9
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/sed/sed-nothreads.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
bin/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/man/*/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4

aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build-aux/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--sysconfdir=/etc
	--disable-nls
	--disable-threads
	--without-included-regex
	--config-cache
"
STACKSIZE="-Wl,-stack,256k"

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

	: hack_lto_cflags

	${MAKE} ${JOBS} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	

	mkdir -p ${THISPKG_DIR}${sysroot}/bin
	cd ${THISPKG_DIR}${sysroot}/bin
	for i in sed
	do
	  rm -f $i
	  $LN_S ../usr/bin/$i $i
	done

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
