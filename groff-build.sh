#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=groff
VERSION=-1.22.4
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/groff/groff-bash-scripts.patch
patches/groff/groff-1.20.1-destbufferoverflow.patch
patches/groff/groff-1.20.1-nroff-empty-LANGUAGE.patch
patches/groff/groff-1.20.1-deunicode.patch
patches/groff/groff-1.21-CVE-2009-5044.patch
patches/groff/groff-1.21-CVE-2009-5081.patch
patches/groff/groff-0001-locale-support-in-papersize-definition.patch
patches/groff/groff-0002-documentation-for-the-locale-keyword.patch
patches/groff/groff-0004-don-t-use-usr-bin-env-in-shebang.patch
patches/groff/groff-force-locale-usage.patch
patches/groff/groff-1.23-forward-compatibility.patch
patches/groff/groff-sort-perl-hash-keys.patch
patches/groff/groff-gnulib.patch
patches/groff/groff-xditview.patch
"
DISABLED_PATCHES="
patches/groff/groff-multi-thread.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
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
if test "$TARGET" = m68k-atari-mint; then
BINFILES+="
${TARGET_PREFIX#/}/share/X11/app-defaults/*
${TARGET_PREFIX#/}/X11R6/bin/*
"
fi

unpack_archive

cd "$srcdir"

# remove hardcoded docdir
sed -i \
    -e '/^docdir=/d' \
    Makefile.am

autoreconf -fiv

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing ${ELF_CFLAGS}"

# libdir redefined as it is just bunch of scripts
CONFIGURE_FLAGS="--host=${TARGET}
	--prefix=${prefix}
	--docdir=${prefix}/share/doc/packages/${PACKAGENAME}
	--libdir=${prefix}/libexec
	--with-appresdir=${prefix}/share/X11/app-defaults
	--with-grofferdir=${prefix}/libexec/groff/groffer
	--disable-nls
"

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
	$srcdir/configure ${CONFIGURE_FLAGS}
	hack_lto_cflags

	${MAKE} ${JOBS} \
		GROFF_BIN_DIR="${HOST_BUILD_DIR}" \
		GROFF_BIN_PATH="${HOST_BUILD_DIR}" \
		GROFFBIN="${HOST_BUILD_DIR}/groff" \
		|| exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" \
		GROFF_BIN_DIR="${HOST_BUILD_DIR}" \
		GROFF_BIN_PATH="${HOST_BUILD_DIR}" \
		GROFFBIN="${HOST_BUILD_DIR}/groff" \
		install
	
	${MAKE} clean >/dev/null
	rm -fv ${THISPKG_DIR}${sysroot}${prefix}/libexec/charset.alias

	${TARGET}-stack --fix=384k ${THISPKG_DIR}${sysroot}/${TARGET_BINDIR#/}/grops

	if test "$TARGET" = m68k-atari-mint; then
		mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/X11R6/bin
		mv ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/{gxditview,xtotroff} ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/X11R6/bin
	fi

	# install profiles to disable the use of ANSI colour sequences by default:
	install -d -m 755 ${THISPKG_DIR}${sysroot}/etc/profile.d/
	install -m 644 ${BUILD_DIR}/patches/groff/groff-zzz-groff.csh ${THISPKG_DIR}${sysroot}/etc/profile.d/zzz-groff.csh
	install -m 644 ${BUILD_DIR}/patches/groff/groff-zzz-groff.sh ${THISPKG_DIR}${sysroot}/etc/profile.d/zzz-groff.sh
	
	# fix a symlink
	ln -s -f ../examples/mom/mom-pdf.pdf ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}share/doc/packages/${PACKAGENAME}/pdf/mom-pdf.pdf

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

PATCHES="$PATCHES
patches/groff/groff-zzz-groff.csh
patches/groff/groff-zzz-groff.sh
"

make_archives
