#!/bin/sh

#
# This script is for building the binutils
# for the cross-compiler
#

me="$0"

PACKAGENAME=binutils
VERSION=-2.29.1
VERSIONPATCH=-20171011
REVISION="GNU Binutils for MiNT ${VERSIONPATCH#-}"

TARGET=${1:-m68k-atari-mint}
PREFIX=/usr

case `uname -s` in
	MINGW* | MSYS*) here=/`pwd -W | tr '\\\\' '/' | tr -d ':'` ;;
	*) here=`pwd` ;;
esac

ARCHIVES_DIR=$HOME/packages
BUILD_DIR="$here"
MINT_BUILD_DIR="$BUILD_DIR/binutils-build"
PKG_DIR="$here/binary7-package"
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
        patches/binutils/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch \
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

BUILD_EXEEXT=
LN_S="ln -s"
case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) host=msys ;;
	CYGWIN*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	Darwin*) host=macos; STRIP=strip; TAR_OPTS= ;;
	*) host=linux ;;
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

if test -d /usr/lib64; then
	BUILD_LIBDIR=${PREFIX}/lib64
else
	BUILD_LIBDIR=${PREFIX}/lib
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

bfd_targets="--enable-targets=$BUILD"
enable_plugins=--disable-plugins
enable_lto=--disable-lto
ranlib=ranlib
STRIP=${STRIP-strip -p}

# binutils ld does not have support for darwin target anymore
test "$host" = "macos" && bfd_targets=""

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

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD="-s"
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"

case $host in
	macos*)
		export CC=/usr/bin/clang
		export CXX=/usr/bin/clang++
		export MACOSX_DEPLOYMENT_TARGET=10.6
		CFLAGS_FOR_BUILD="-pipe -O2 -arch x86_64"
		CXXFLAGS_FOR_BUILD="-pipe -O2 -stdlib=libc++ -arch x86_64"
		LDFLAGS_FOR_BUILD="-Wl,-headerpad_max_install_names -arch x86_64"
		;;
esac

../$srcdir/configure \
	--target="${TARGET}" --build="$BUILD" \
	--prefix="${PREFIX}" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="${PREFIX}/bin" \
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
	--with-sysroot="${PREFIX}/${TARGET}/sys-root"

${MAKE} $JOBS || exit 1


case $host in
	mingw*) if test "${PREFIX}" = /usr; then PREFIX=${MINGW_PREFIX}; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
	macos*) if test "${PREFIX}" = /usr; then PREFIX=/opt/cross-mint; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
esac

#
# install this package twice:
# - once for building the binary archive for this pacakge only.
# - once for building a complete package.
#   This directory is also kept for later stages,
#   eg. compiling the C-library and gcc
#
THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
rm -rf "${THISPKG_DIR}"
for INSTALL_DIR in "${PKG_DIR}" "${THISPKG_DIR}"; do
	
	cd "$MINT_BUILD_DIR"
	${MAKE} DESTDIR="$INSTALL_DIR" prefix="${PREFIX}" bindir="${PREFIX}/bin" install-strip >/dev/null || exit 1
	
	mkdir -p "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	cd "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	for i in addr2line ar as nm ld ld.bfd objcopy objdump ranlib strip readelf dlltool dllwrap size strings; do
		if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
			rm -f ${i} ${i}${BUILD_EXEEXT}
			$LN_S ../../bin/${TARGET}-$i${BUILD_EXEEXT} $i
		fi
	done
	
	cd "${INSTALL_DIR}/${PREFIX}/bin"
	
	rm -f ${TARGET}-ld ${TARGET}-ld${BUILD_EXEEXT}
	$LN_S ${TARGET}-ld.bfd${BUILD_EXEEXT} ${TARGET}-ld${BUILD_EXEEXT}
	cd "${INSTALL_DIR}" || exit 1
	
	pwd
	exit 0
	${STRIP} ${PREFIX#/}/bin/*
	rm -f ${BUILD_LIBDIR#/}/libiberty.a

	rm -f ${PREFIX#/}/share/info/dir
	for f in ${PREFIX#/}/share/man/*/* ${PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
done

cd "${THISPKG_DIR}" || exit 1

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}${VERSIONPATCH}

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-doc.tar.xz ${PREFIX#/}/share/info ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz ${PREFIX#/}

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.tar.xz ${ALLPATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
