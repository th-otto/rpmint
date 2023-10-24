#!/bin/bash

#
# This script is for using the cross-compiler to
# build the native binutils for the target(s)
#

me="$0"

PACKAGENAME=binutils
VERSION=-2.41
VERSIONPATCH=-20230926
REVISION="GNU Binutils for MiNT ${VERSIONPATCH#-}"

TARGET=${1:-m68k-atari-mint}
if test "$TARGET" = m68k-atari-mintelf; then
REVISION="GNU Binutils for MiNT ELF ${VERSIONPATCH#-}"
fi

prefix=/usr
TARGET_PREFIX=/usr
TARGET_LIBDIR=${TARGET_PREFIX}/lib
TARGET_BINDIR=${TARGET_PREFIX}/bin

case `uname -s` in
	MINGW* | MSYS*) here=/`pwd -W | tr '\\\\' '/' | tr -d ':'` ;;
	*) here=`pwd` ;;
esac

ARCHIVES_DIR=$HOME/packages
BUILD_DIR="$here"
MINT_BUILD_DIR="$BUILD_DIR/binutils-build-cross"
DIST_DIR="$here/pkgs"

srcdir="${PACKAGENAME}${VERSION}"

#
# The branch patch was created by
# BINUTILS_SUPPORT_DIRS="bfd gas include libiberty opcodes ld elfcpp gold gprof intl setup.com makefile.vms cpu zlib"
# git diff binutils-2_29_1.1 binutils-2_29-branch -- $BINUTILS_SUPPORT_DIRS
# BINUTILS_SUPPORT_DIRS is from src-release.sh
#
# The mint patch can be recreated by running
# git diff binutils-2_29-branch binutils-2_29-mint
# in my fork (https://github.com/th-otto/binutils/tree/binutils-2_29-mint)
#
PATCHES="\
        patches/binutils/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch \
"
ALLPATCHES="$PATCHES \
        patches/binutils/binutils-m68k-segmentalign.patch \
"

TAR=${TAR-tar}
TAR_OPTS=${TAR_OPTS---owner=0 --group=0}

LN_S="ln -s"
GCC=${GCC-gcc}
GXX=${GXX-g++}
case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) host=msys ;;
	CYGWIN*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	Darwin*) host=macos; STRIP=strip; TAR_OPTS= ;;
	*) host=linux64 ;;
esac
case $host in
	cygwin* | mingw* | msys*) BUILD_EXEEXT=.exe ;;
esac
case $host in
	mingw* | msys*) LN_S="cp -p" ;;
esac

if test ! -f ".patched-${PACKAGENAME}${VERSION}"; then
	for f in "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.xz" \
	         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.bz2" \
	         "${PACKAGENAME}${VERSION}.tar.xz" \
	         "${PACKAGENAME}${VERSION}.tar.bz2"; do
		if test -f "$f"; then tar xvf "$f" || exit 1; fi
	done
	if test ! -d "$srcdir"; then
		echo "$srcdir: no such directory" >&2
		exit 1
	fi
	for f in $PATCHES; do
	  if test -f "$f"; then
	    cd "$srcdir" && patch -p1 < "$BUILD_DIR/$f" || exit 1
	  else
	    echo "missing patch $f" >&2
	    exit 1
	  fi
	  cd "$BUILD_DIR"
	done
	touch ".patched-${PACKAGENAME}${VERSION}"
fi

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi

JOBS=`rpm --eval '%{?jobs:%jobs}' 2>/dev/null`
P=$(getconf _NPROCESSORS_CONF 2>/dev/null || nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null)
if test -z "$P"; then P=$NUMBER_OF_PROCESSORS; fi
if test -z "$P"; then P=1; fi
if test -z "$JOBS"; then
  JOBS=$P
else
  test 1 -gt "$JOBS" && JOBS=1
fi
JOBS=-j$JOBS
MAKE=${MAKE:-make}

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
for a in "" -1.16 -1.15 -1.14 -1.13 -1.12 -1.11 -1.10; do
	BUILD=`/usr/share/automake${a}/config.guess 2>/dev/null`
	test "$BUILD" != "" && break
	test "$host" = "macos" && BUILD=`/opt/local/share/automake${a}/config.guess 2>/dev/null`
	test "$BUILD" != "" && break
done
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`

# we don't want the build target in a native build
bfd_targets=""
enable_plugins=--disable-plugins
enable_lto=--disable-lto
enable_tui=
ranlib=ranlib
STRIP=${STRIP-strip -p}

# add opposite of default mingw32 target for binutils,
# and also host target
case "${TARGET}" in
    x86_64-*-mingw32*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
	    bfd_targets="${bfd_targets}i686-pc-mingw32"
    	;;
    i686-*-mingw*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
    	bfd_targets="${bfd_targets}x86_64-w64-mingw64"
		;;
    *-*-*mintelf*)
    	enable_lto=--enable-lto
    	ranlib=gcc-ranlib
		# explictly --enable-tui for gdb so we get error early if curses is not found
		enable_tui=--enable-tui
		;;
    *-*-*elf* | *-*-linux* | *-*-darwin*)
    	enable_lto=--enable-lto
		enable_plugins=--enable-plugins
    	ranlib=gcc-ranlib
		;;
esac
case "${TARGET}" in
    m68k-atari-mintelf*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
    	bfd_targets="${bfd_targets}m68k-atari-mint"
		;;
    m68k-atari-mint*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
    	bfd_targets="${bfd_targets}m68k-atari-mintelf"
		;;
esac

ranlib=`which ${TARGET}-${ranlib}`
strip=`which "${TARGET}-strip"`
as=`which "${TARGET}-as"`
if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$as" -o ! -x "$strip"; then
	echo "cross-binutil tools for ${TARGET} not found" >&2
	exit 1
fi

#
# this could eventually be extracted from gcc -print-multi-lib
#
CPU_CFLAGS_000=-m68000    ; CPU_LIBDIR_000=/m68000    ; WITH_CPU_000=m68000
CPU_CFLAGS_020=-m68020-60 ; CPU_LIBDIR_020=/m68020-60 ; WITH_CPU_020=m68020-60
CPU_CFLAGS_v4e=-mcpu=5475 ; CPU_LIBDIR_v4e=/m5475     ; WITH_CPU_v4e=5475
CPU_CFLAGS_000=-m68000    ; CPU_LIBDIR_000=           ; WITH_CPU_000=m68000
CPU_CFLAGS_020=-m68020-60 ; CPU_LIBDIR_020=           ; WITH_CPU_020=m68020-60
CPU_CFLAGS_v4e=-mcpu=5475 ; CPU_LIBDIR_v4e=           ; WITH_CPU_v4e=5475
#
# This should list the default target cpu last,
# so that any files left behind are compiled for this
#
ALL_CPUS="020 v4e 000"


THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
rm -rf "${THISPKG_DIR}"
TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}

create_config_cache_helper()
{
cat <<EOF
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
ac_cv_func_pthread_setname_np=no
ac_cv_func_pthread_sigmask=no
ax_cv_PTHREAD_PRIO_INHERIT=no
gl_pthread_in_glibc=yes
EOF
}

create_config_cache()
{
case $TARGET in
*-*-mintelf*)
	mkdir -p gdb gdbsupport gnulib gdbserver
	create_config_cache_helper >gdb/config.cache
	create_config_cache_helper >gdbsupport/config.cache
	create_config_cache_helper >gdbserver/config.cache
	create_config_cache_helper >gnulib/config.cache
	;;
esac
}

for CPU in ${ALL_CPUS}; do
	cd "$here" || exit 1
	rm -rf "$MINT_BUILD_DIR"
	mkdir -p "$MINT_BUILD_DIR"
	
	cd "$MINT_BUILD_DIR" || exit 1
	rm -rf "${THISPKG_DIR}-${CPU}"
	
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval with_cpu=\${WITH_CPU_$CPU}
	STACKSIZE="-Wl,-stack,512k"

	CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer ${CPU_CFLAGS}"
	LDFLAGS_FOR_BUILD="-s ${CPU_CFLAGS}"
	CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD ${CPU_CFLAGS}"

	create_config_cache

	../$srcdir/configure \
		--target="${TARGET}" --host="${TARGET}" --build="$BUILD" \
		--prefix="${TARGET_PREFIX}" \
		--libdir="${TARGET_LIBDIR}" \
		--bindir="${TARGET_BINDIR}" \
		--libexecdir='${libdir}' \
		CFLAGS="$CFLAGS_FOR_BUILD" \
		CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
		LDFLAGS="$LDFLAGS_FOR_BUILD ${STACKSIZE}" \
		$bfd_targets \
		--with-pkgversion="$REVISION" \
		--with-bugurl='https://github.com/freemint/m68k-atari-mint-binutils-gdb/issues' \
		--with-stage1-ldflags= \
		--with-boot-ldflags="$LDFLAGS_FOR_BUILD" \
		--with-gcc --with-gnu-as --with-gnu-ld \
		--disable-werror \
		--disable-threads \
		--enable-new-dtags \
		--enable-relro \
		--enable-default-hash-style=both \
		$enable_lto \
		$enable_tui \
		$enable_plugins \
		--disable-nls \
		--with-system-zlib \
		--with-system-readline \
		--disable-bracketed-paste-default \
		--with-cpu=$with_cpu \
		--with-build-sysroot="${prefix}/${TARGET}/sys-root"
	
	${MAKE} $JOBS || exit 1
	
	cd "$MINT_BUILD_DIR"

	rm -rf "${THISPKG_DIR}${TARGET_BINDIR}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin" "${THISPKG_DIR}${TARGET_LIBDIR}"

	${MAKE} DESTDIR="$THISPKG_DIR" libdir='${exec_prefix}/lib'$multilibdir install-strip >/dev/null || exit 1
	
	mkdir -p "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"

	cd "${THISPKG_DIR}" || exit 1
	${strip} ${TARGET_BINDIR#/}/*

	for i in addr2line ar as nm ld ld.bfd objcopy objdump ranlib strip readelf dlltool dllwrap size strings; do
		cd "${THISPKG_DIR}${TARGET_BINDIR}"
		test -f "$i" || continue
		rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
		mv $i ${TARGET}-$i
		$LN_S ${TARGET}-$i $i
		cd "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
		rm -f ${i} ${i}${TARGET_EXEEXT}
		$LN_S ../../bin/$i${TARGET_EXEEXT} $i
	done
	
	cd "${THISPKG_DIR}" || exit 1
	rm -f ${TARGET_LIBDIR#/}/libiberty.a
	find . -type f -name "*.la" -delete -printf "rm %p\n"

	rm -f ${TARGET_PREFIX#/}/share/info/dir
	for f in ${TARGET_PREFIX#/}/share/man/*/* ${TARGET_PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done

	# create separate archive for gdb
	if test -f ${TARGET_PREFIX#/}/bin/gdb; then
		gdb=${TARGET_PREFIX#/}/bin/gdb*
		gdb="$gdb "${TARGET_PREFIX#/}/share/gdb
		gdb="$gdb "${TARGET_PREFIX#/}/share/info/*gdb*
		gdb="$gdb "${TARGET_PREFIX#/}/share/man/*/*gdb*
		gdb="$gdb "${TARGET_PREFIX#/}/include/gdb
		gdb_version=`cat $MINT_BUILD_DIR/../$srcdir/gdb/version.in`
		gdb_version=${gdb_version//.DATE-git/}
		gdb_version=$(echo ${gdb_version} | cut -d '.' -f 1-2)
		${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/gdb-${gdb_version}-${TARGET##*-}-${CPU}.tar.xz $gdb || exit 1
		rm -rf $gdb
	fi

	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-${CPU}.tar.xz *
	
	rm -rf ${TARGET_PREFIX#/}/lib
done # for CPU

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi
	
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint.tar.xz ${ALLPATCHES}

cp -p "$me" ${DIST_DIR}/cross-${PACKAGENAME}${VERSION}${VERSIONPATCH}-build.sh
