#!/bin/sh

#
# This script is for using the cross-compiler to
# build the native binutils for the target(s)
#

me="$0"

PACKAGENAME=binutils
VERSION=-2.29.1
VERSIONPATCH=-20171011
REVISION="GNU Binutils for MiNT ${VERSIONPATCH#-}"

TARGET=${1:-m68k-atari-mint}
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
MINT_BUILD_DIR="$BUILD_DIR/binutils-build"
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
        patches/binutils/${PACKAGENAME}${VERSION}-0001-binutils-2.29.1-branch.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-mint.patch \
"
ELFPATCHES="patches/binutils/${PACKAGENAME}${VERSION}-mintelf.patch"
ALLPATCHES="$PATCHES $ELFPATCHES"
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
		PATCHES="$PATCHES $ELFPATCHES"
		;;
esac

TAR=${TAR-tar}
TAR_OPTS=${TAR_OPTS---owner=0 --group=0}

LN_S="ln -s"
case `uname -s` in
	MINGW64*) host=mingw64; ;;
	MINGW32*) host=mingw32; ;;
	MINGW*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; ;;
	MSYS*) host=msys ;;
	CYGWIN*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	Darwin*) host=macos; TAR_OPTS= ;;
	*) host=linux ;;
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
for a in "" -1.15 -1.14 -1.13 -1.12 -1.11 -1.10; do
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
ranlib=${TARGET}-ranlib
strip="${TARGET}-strip -p"

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
    	ranlib=${TARGET}-gcc-ranlib
		;;
    *-*-*elf* | *-*-linux* | *-*-darwin*)
    	enable_lto=--enable-lto
		enable_plugins=--enable-plugins
    	ranlib=${TARGET}-gcc-ranlib
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

#
# this could eventually be extracted from gcc -print-multi-lib
#
CPU_CFLAGS_000=-m68000    ; CPU_LIBDIR_000=
CPU_CFLAGS_020=-m68020-60 ; CPU_LIBDIR_020=/m68020-60
CPU_CFLAGS_v4e=-mcpu=5475 ; CPU_LIBDIR_v4e=/m5475
#
# This should list the default target cpu last,
# so that any files left behind are compiled for this
#
ALL_CPUS="020 v4e 000"


THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
rm -rf "${THISPKG_DIR}"

for CPU in ${ALL_CPUS}; do
	cd "$here" || exit 1
	rm -rf "$MINT_BUILD_DIR"
	mkdir -p "$MINT_BUILD_DIR"
	
	cd "$MINT_BUILD_DIR"
	rm -rf "${THISPKG_DIR}-${CPU}"
	
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval libdir=\${CPU_LIBDIR_$CPU}

	CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer ${CPU_CFLAGS}"
	LDFLAGS_FOR_BUILD="-s"
	CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD ${CPU_CFLAGS}"
	
	../$srcdir/configure \
		--target="${TARGET}" --host="${TARGET}" --build="$BUILD" \
		--prefix="${TARGET_PREFIX}" \
		--libdir="${TARGET_PREFIX}/lib" \
		--bindir="${TARGET_PREFIX}/bin" \
		--libexecdir='${libdir}' \
		CFLAGS="$CFLAGS_FOR_BUILD" \
		CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
		LDFLAGS="$LDFLAGS_FOR_BUILD" \
		$bfd_targets \
		--with-pkgversion="$REVISION" \
		--with-stage1-ldflags= \
		--with-boot-ldflags="$LDFLAGS_FOR_BUILD" \
		--with-gcc --with-gnu-as --with-gnu-ld \
		--disable-werror \
		--disable-threads \
		--enable-new-dtags \
		--enable-relro \
		--enable-default-hash-style=both \
		$enable_lto \
		$enable_plugins \
		--disable-nls \
		--with-build-sysroot="${prefix}/${TARGET}/sys-root"
	
	${MAKE} $JOBS || exit 1
	
	cd "$MINT_BUILD_DIR"

	rm -rf "${THISPKG_DIR}${TARGET_BINDIR}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"

	${MAKE} DESTDIR="$THISPKG_DIR" libdir='${exec_prefix}/lib'$libdir install-strip || exit 1
	
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
	
	# move bin directories away wile gathering libraries
	mkdir -p "${THISPKG_DIR}-${CPU}"
	mv "${THISPKG_DIR}${TARGET_BINDIR}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}" "${THISPKG_DIR}-${CPU}"
	
	cd "${THISPKG_DIR}" || exit 1
	rm -f ${TARGET_LIBDIR#/}/libiberty.a
	rm -f ${TARGET_LIBDIR#/}/*.la

	rm -f ${TARGET_PREFIX#/}/share/info/dir
	for f in ${TARGET_PREFIX#/}/share/man/*/* ${TARGET_PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
	
done # for CPU

TARNAME=${PACKAGENAME}${VERSION}
for CPU in ${ALL_CPUS}; do
	cd "${THISPKG_DIR}" || exit 1
	rm -rf "${THISPKG_DIR}${TARGET_BINDIR}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}"
	
	# move bin directories back
	mv "${THISPKG_DIR}-${CPU}/bin" "${THISPKG_DIR}${TARGET_BINDIR}"
	mv "${THISPKG_DIR}-${CPU}/${TARGET}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}"
	rmdir "${THISPKG_DIR}-${CPU}"
	
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-${TARGET##*-}-${CPU}.tar.xz *
done

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi
	
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint.tar.xz ${ALLPATCHES}

cp -p "$me" ${DIST_DIR}/build-crossnative-${PACKAGENAME}${VERSION}.sh
