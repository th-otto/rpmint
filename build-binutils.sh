#!/bin/sh

me="$0"

PACKAGENAME=binutils
VERSION=-2.29.1
VERSIONPATCH=20171006
REVISION="GNU Binutils for MiNT $VERSIONPATCH"

TARGET=${1:-m68k-atari-mint}
PREFIX=/usr

case `uname -s` in
	MINGW* | MSYS*) here=/`pwd -W | tr '\\\\' '/' | tr -d ':'` ;;
	*) here=`pwd` ;;
esac

ARCHIVES_DIR=$HOME/packages
BUILD_DIR="$here"
MINT_BUILD_DIR="$BUILD_DIR/mint7-build"
PKG_DIR="$here/binary7-package"
DIST_DIR="$here/pkgs"

srcdir="${PACKAGENAME}${VERSION}"

PATCHES="\
        patches/binutils/${PACKAGENAME}${VERSION}-0001-binutils-2.29.1-branch.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0005-x86-64-biarch.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0007-ld-dtags.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0008-ld-relro.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0011-use-hashtype-both-by-default.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0022-binutils-bfd_h.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0201-aout.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0202-ldfile.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-0203-config-rpath.patch \
        patches/binutils/${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}.patch \
"
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
		PATCHES="$PATCHES patches/binutils/${PACKAGENAME}${VERSION}-mintelf.patch"
		;;
esac

EXEEXT=
LN_S="ln -s"
case `uname -s` in
	CYGWIN* | MINGW* | MSYS*) EXEEXT=.exe ;;
esac
case `uname -s` in
	MINGW* | MSYS*) LN_S="cp -p" ;;
esac
case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) host=msys ;;
	CYGWIN*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	*) host=linux ;;
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

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
BUILD=`/usr/share/automake/config.guess 2>/dev/null`
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`

bfd_targets="--enable-targets=$BUILD"
enable_plugins=--disable-plugins
enable_lto=--disable-lto
ranlib=ranlib

# add opposite of default mingw32 target for binutils,
# and also host target
case "${TARGET}" in
    x86_64-*-mingw32*)
	    bfd_targets="$bfd_targets,i686-pc-mingw32"
    	;;
    i686-*-mingw*)
    	bfd_targets="$bfd_targets,x86_64-w64-mingw64"
		;;
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
		enable_plugins=--enable-plugins
    	ranlib=gcc-ranlib
		;;
esac
case "${TARGET}" in
    m68k-atari-mintelf*)
    	bfd_targets="$bfd_targets,m68k-atari-mint"
		;;
    m68k-atari-mint*)
    	bfd_targets="$bfd_targets,m68k-atari-mintelf"
		;;
esac

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD="-s"
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"


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
    --with-stage1-ldflags=-s \
    --with-boot-ldflags="$LDFLAGS_FOR_BUILD" \
	--with-gcc --with-gnu-as --with-gnu-ld \
    --disable-werror \
	--disable-threads \
	$enable_lto \
	$enable_plugins \
	--disable-nls \
	--with-sysroot="${PREFIX}/${TARGET}/sys-root"

make $JOBS || exit 1


case `uname -s` in
	MINGW*) if test "${PREFIX}" = /usr; then PREFIX=${MINGW_PREFIX}; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
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
	make DESTDIR="$INSTALL_DIR" prefix="${PREFIX}" bindir="${PREFIX}/bin" install-strip || exit 1
	
	mkdir -p "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	cd "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	for i in addr2line ar arconv as c++ nm cpp csize cstrip flags g++ gcc gcov gfortran ld ld.bfd mintbin nm objcopy objdump ranlib stack strip symex readelf dlltool dllwrap; do
		if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
			rm -f ${i} ${i}${EXEEXT}
			$LN_S ../../bin/${TARGET}-$i${EXEEXT} $i
		fi
	done
	
	cd "${INSTALL_DIR}/${PREFIX}/bin"
	
	rm -f ${TARGET}-ld ${TARGET}-ld${EXEEXT}
	$LN_S ${TARGET}-ld.bfd${EXEEXT} ${TARGET}-ld${EXEEXT}
	cd "${INSTALL_DIR}" || exit 1
	
	strip -p ${PREFIX#/}/bin/*
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

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}-${VERSIONPATCH}

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-doc.tar.xz ${PREFIX#/}/share/info ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz ${PREFIX#/}

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint-${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}-${VERSIONPATCH}.sh
