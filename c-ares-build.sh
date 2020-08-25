#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=c-ares
VERSION=-1.7.5
VERSIONPATCH=

. ${scriptdir}/functions.sh

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man3/*
"

PATCHES="patches/c-ares/c-ares-mintelf-config.patch"

unpack_archive

cd "$MINT_BUILD_DIR"



COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared \
--disable-curldebug \
--disable-debug \
--disable-symbol-hiding \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir || exit 1
	hack_lto_cflags

# sed -i -e 's/#define HAVE_ARPA_INET_H 1/#undef HAVE_ARPA_INET_H/g' ./ares_config.h
# sed -i -e 's/#define HAVE_ARPA_NAMESER_H 1/#undef HAVE_ARPA_NAMESER_H/g' ./ares_config.h

	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	mkdir -p ${THISPKG_DIR}${sysroot}${prefix}/bin
	install -m 755 ahost${TARGET_EXEEXT} adig${TARGET_EXEEXT} acountry${TARGET_EXEEXT} ${THISPKG_DIR}${sysroot}${prefix}/bin
	${MAKE} clean >/dev/null
	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
