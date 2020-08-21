#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=groff
VERSION=-1.22.3
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/groff/groff-1.22.3-1.debian.diff
patches/groff/groff-1.20.1-destbufferoverflow.patch
patches/groff/groff-1.20.1-nroff-empty-LANGUAGE.patch
patches/groff/groff-1.20.1-deunicode.patch
patches/groff/groff-1.21-CVE-2009-5044.patch
patches/groff/groff-1.21-CVE-2009-5080.patch
patches/groff/groff-1.21-CVE-2009-5081.patch
patches/groff/groff-0001-locale-support-in-papersize-definition.patch
patches/groff/groff-0002-documentation-for-the-locale-keyword.patch
patches/groff/groff-force-locale-usage.patch
patches/groff/groff-multi-thread.patch
patches/groff/groff-mintelf-config.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
${TARGET_MANDIR#/}/man7/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/${PACKAGENAME}/*
${TARGET_PREFIX#/}/share/doc/packages/${PACKAGENAME}/*
${TARGET_PREFIX#/}/libexec/${PACKAGENAME}/*
etc/profile.d
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--docdir=${prefix}/share/doc/packages/${PACKAGENAME} \
	--disable-nls"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_func_strnlen_working=yes
EOF
	append_gnulib_cache
}

export GROFF_COMMAND_PREFIX=
export GROFF_TMAC_PATH=$srcdir/tmac:$srcdir/src/roff/troff
	
#
# we need an executable for the host
#
HOST_BUILD_DIR="$srcdir/build-host"
mkdir -p "$HOST_BUILD_DIR"
cd "${HOST_BUILD_DIR}"
CFLAGS="-O2" $srcdir/configure
${MAKE} ${JOBS} || exit 1

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,160k"

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	$srcdir/configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/libexec' \
		--with-appresdir=${prefix}/share/X11/app-defaults \
		--with-grofferdir='${exec_prefix}/libexec/groff/groffer'
	hack_lto_cflags
	${MAKE} ${JOBS} \
		GROFF_BIN_DIR="${HOST_BUILD_DIR}/src/roff/groff" \
		GROFF_BIN_PATH="${HOST_BUILD_DIR}/src/roff/groff" \
		GROFFBIN="${HOST_BUILD_DIR}/src/roff/groff/groff" \
		|| exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" \
		GROFF_BIN_DIR="${HOST_BUILD_DIR}/src/roff/groff" \
		GROFF_BIN_PATH="${HOST_BUILD_DIR}/src/roff/groff" \
		GROFFBIN="${HOST_BUILD_DIR}/src/roff/groff/groff" \
		install
	
	${MAKE} clean >/dev/null
	rm -fv ${THISPKG_DIR}${sysroot}${prefix}/libexec/charset.alias

	install -d -m 755 ${THISPKG_DIR}${sysroot}/etc/profile.d/
	install -m 644 ${BUILD_DIR}/patches/groff/groff-zzz-groff.csh ${THISPKG_DIR}${sysroot}/etc/profile.d/zzz-groff.csh
	install -m 644 ${BUILD_DIR}/patches/groff/groff-zzz-groff.sh ${THISPKG_DIR}${sysroot}/etc/profile.d/zzz-groff.sh
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

PATCHES="$PATCHES
patches/groff/groff-zzz-groff.csh
patches/groff/groff-zzz-groff.sh
"

make_archives
