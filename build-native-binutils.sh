#!/bin/sh

#
# This script is for recompiling the native binutils on the target
#

me="$0"

PACKAGENAME=binutils
VERSION=-2.29.1
VERSIONPATCH=-20171011
REVISION="GNU Binutils for MiNT ${VERSIONPATCH#-}"

TARGET=${1:-m68k-atari-mint}
prefix=/usr
libdir=${prefix}/lib
bindir=${prefix}/bin

BUILD=${TARGET}

case `uname -s` in
	*MiNT | *mint | *TOS)
		here=`pwd`
		host=mint
		;;
	*)
		echo "this script must be run native on MiNT" >&2
		;;
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

JOBS=
MAKE=${MAKE:-make}


# we don't want the build target in a native build
bfd_targets=""
enable_plugins=--disable-plugins
enable_lto=--disable-lto
ranlib=ranlib
strip="strip -p"

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
		# plugin does not work because of missing dlopen
		# enable_plugins=--enable-plugins
    	ranlib=gcc-ranlib
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
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer ${CPU_CFLAGS}"
	LDFLAGS_FOR_BUILD="-s"
	CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD ${CPU_CFLAGS}"
	
	../$srcdir/configure \
		--target="${TARGET}" --host="${TARGET}" --build="${BUILD}" \
		--prefix="${prefix}" \
		--libdir="${libdir}" \
		--bindir="${bindir}" \
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
		--disable-nls
	
	${MAKE} $JOBS || exit 1
	
	cd "$MINT_BUILD_DIR"

	rm -rf "${THISPKG_DIR}${bindir}" "${THISPKG_DIR}${prefix}/${TARGET}/bin"

	${MAKE} DESTDIR="$THISPKG_DIR" libdir='${exec_prefix}/lib'$multilibdir install-strip || exit 1
	
	mkdir -p "${THISPKG_DIR}${prefix}/${TARGET}/bin"

	cd "${THISPKG_DIR}" || exit 1
	${strip} ${bindir#/}/*

	for i in addr2line ar as nm ld ld.bfd objcopy objdump ranlib strip readelf dlltool dllwrap size strings; do
		cd "${THISPKG_DIR}${bindir}"
		test -f "$i" || continue
		rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
		mv $i ${TARGET}-$i
		$LN_S ${TARGET}-$i $i
		cd "${THISPKG_DIR}${prefix}/${TARGET}/bin"
		rm -f ${i} ${i}${TARGET_EXEEXT}
		$LN_S ../../bin/$i${TARGET_EXEEXT} $i
	done
	
	# move bin directories away wile gathering libraries
	mkdir -p "${THISPKG_DIR}-${CPU}"
	mv "${THISPKG_DIR}${bindir}" "${THISPKG_DIR}${prefix}/${TARGET}" "${THISPKG_DIR}-${CPU}"
	
	cd "${THISPKG_DIR}" || exit 1
	rm -f ${libdir#/}/libiberty.a
	rm -f ${libdir#/}/*.la

	rm -f ${prefix#/}/share/info/dir
	for f in ${prefix#/}/share/man/*/* ${prefix#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
	
done # for CPU

TARNAME=${PACKAGENAME}${VERSION}
for CPU in ${ALL_CPUS}; do
	cd "${THISPKG_DIR}" || exit 1
	rm -rf "${THISPKG_DIR}${bindir}" "${THISPKG_DIR}${prefix}/${TARGET}"
	
	# move bin directories back
	mv "${THISPKG_DIR}-${CPU}/bin" "${THISPKG_DIR}${bindir}"
	mv "${THISPKG_DIR}-${CPU}/${TARGET}" "${THISPKG_DIR}${prefix}/${TARGET}"
	rmdir "${THISPKG_DIR}-${CPU}"
	
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-${TARGET##*-}-${CPU}.tar.xz *
done

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi
	
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint.tar.xz ${ALLPATCHES}

cp -p "$me" ${DIST_DIR}/build-native-${PACKAGENAME}${VERSION}.sh
