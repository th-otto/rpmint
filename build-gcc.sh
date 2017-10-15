#!/bin/sh

# This is an almost automatic script for building the binary packages.
# It is designed to be run on linux, cygwin or mingw,
# but it should run fine on other GNU environments.

me="$0"

PACKAGENAME=gcc
VERSION=-7.2.0
VERSIONPATCH=-20171006
REVISION="MiNT ${VERSIONPATCH#-}"

#
# For which target we build-
# should be either m68k-atari-mint or m68k-atari-mintelf
#
TARGET=${1:-m68k-atari-mint}

#
# The prefix where the executables should
# be installed later. If installed properly,
# this actually does not matter much, since
# all relevant directories are looked up
# relative to the executable
#
TAR=${TAR-tar}
TAR_OPTS=${TAR_OPTS---owner=0 --group=0}
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
	mingw*) PREFIX=${MINGW_PREFIX} ;;
	macos*) PREFIX=/opt/cross-mint ;;
	*) PREFIX=/usr ;;
esac

#
# Where to look for the original source archives
#
case $host in
	mingw* | msys*) here=`pwd` ;;
	*) here=`pwd` ;;
esac
ARCHIVES_DIR="$here"

#
# where to look for mpfr/gmp/mpc/isl etc.
# currently only needed on Darwin, which lacks
# libmpc.
# Should be a static compiled version, so the
# compiler does not depend on non-standard shared libs
#
CROSSTOOL_DIR="$HOME/crosstools"

#
# Where to look for patches, write logs etc.
#
BUILD_DIR="$here"

#
# Where to configure and build gcc. This *must*
# be outside the gcc source directory, ie. it must
# not even be a subdirectory of it
#
MINT_BUILD_DIR="$BUILD_DIR/gcc-build"

#
# Where to put the executables for later use.
# This should be the same as the one configured
# in the binutils script
#
PKG_DIR="$here/binary7-package"

#
# Where to put the binary packages
#
DIST_DIR="$here/pkgs"

#
# Where to look up the source tree.
#
srcdir="$HOME/m68k-atari-mint-gcc"
if test -d "$srcdir"; then
	touch ".patched-${PACKAGENAME}${VERSION}"
else
	srcdir="$here/$PACKAGENAME$VERSION"
fi

#
# this patch can be recreated by
# - cloning https://github.com/th-otto/m68k-atari-mint-gcc.git
# - checking out the gcc-7-mint branch
# - running git diff gcc-7_2_0-release HEAD
#
PATCHES="patches/gcc/$PACKAGENAME$VERSION-mint${VERSIONPATCH}.patch"

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
if test ! -f "${PREFIX}/${TARGET}/sys-root/usr/include/compiler.h"; then
	echo "mintlib headers must be installed in ${PREFIX}/${TARGET}/sys-root/usr/include" >&2
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

BASE_VER=$(cat $srcdir/gcc/BASE-VER)
gcc_dir_version=$(echo $BASE_VER | cut -d '.' -f 1)

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

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD=""
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
LDFLAGS_FOR_TARGET=

enable_lto=--disable-lto
enable_plugin=--disable-plugin
languages=c,c++
ranlib=ranlib
STRIP=${STRIP-strip -p}

case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
		case "${BUILD}" in
        *-*-linux*)
    		enable_plugin=--enable-plugin
    	esac
    	languages="$languages,lto"
		# not here; we are just building it
		# ranlib=gcc-ranlib
		;;
esac
BUILD_EXEEXT=
LN_S="ln -s"
case $host in
	cygwin* | mingw* | msys*) BUILD_EXEEXT=.exe ;;
esac
case $host in
	mingw* | msys*) LN_S="cp -p" ;;
esac

try="${PKG_DIR}/${PREFIX}/bin/${TARGET}-${ranlib}"
if test -x "$try"; then
	ranlib="$try"
	strip="${PKG_DIR}/${PREFIX}/bin/${TARGET}-strip"
	as="${PKG_DIR}/${PREFIX}/bin/${TARGET}-as"
else
	ranlib=`which ${TARGET}-${ranlib} 2>/dev/null`
	strip=`which "${TARGET}-strip"`
	as=`which "${TARGET}-as" 2>/dev/null`
fi
if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$as" -o ! -x "$strip"; then
	echo "cross-binutil tools for ${TARGET} not found" >&2
	exit 1
fi

mpfr_config=

case $host in
	macos*)
		export CC=/usr/bin/clang
		export CXX=/usr/bin/clang++
		export MACOSX_DEPLOYMENT_TARGET=10.6
		CFLAGS_FOR_BUILD="-pipe -O2 -arch x86_64"
		CXXFLAGS_FOR_BUILD="-pipe -O2 -stdlib=libc++ -arch x86_64"
		LDFLAGS_FOR_BUILD="-Wl,-headerpad_max_install_names -arch x86_64"
		mpfr_config="--with-mpc=${CROSSTOOL_DIR} --with-gmp=${CROSSTOOL_DIR} --with-mpfr=${CROSSTOOL_DIR}"
		;;
esac

$srcdir/configure \
	--target="${TARGET}" --build="$BUILD" \
	--prefix="${PREFIX}" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="${PREFIX}/bin" \
	--libexecdir='${libdir}' \
	CFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD" \
	CFLAGS="$CFLAGS_FOR_BUILD" \
	CXXFLAGS_FOR_BUILD="$CXXFLAGS_FOR_BUILD" \
	CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
	BOOT_CFLAGS="$CFLAGS_FOR_BUILD" \
	CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET" \
	CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET" \
	LDFLAGS_FOR_BUILD="$LDFLAGS_FOR_BUILD" \
	LDFLAGS="$LDFLAGS_FOR_BUILD" \
	--with-pkgversion="$REVISION" \
	--disable-libvtv \
	--disable-libmpx \
	--disable-libcc1 \
	--disable-werror \
	--with-gxx-include-dir=${PREFIX}/${TARGET}/sys-root/usr/include/c++/${gcc_dir_version} \
	--with-default-libstdcxx-abi=gcc4-compatible \
	--with-gcc-major-version-only \
	--with-gcc --with-gnu-as --with-gnu-ld \
	--with-system-zlib \
	--disable-libgomp \
	--without-newlib \
	--disable-libstdcxx-pch \
	--disable-threads \
	--disable-win32-registry \
	$enable_lto \
	--enable-ssp \
	--enable-libssp \
	$enable_plugin \
	--enable-decimal-float \
	--disable-nls \
	--with-libiconv-prefix="${PREFIX}" \
	--with-libintl-prefix="${PREFIX}" \
	$mpfr_config \
	--with-sysroot="${PREFIX}/${TARGET}/sys-root" \
	--enable-languages="$languages"

make $JOBS all-gcc || exit 1
make $JOBS all-target-libgcc || exit 1
make $JOBS || exit 1

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
rm -rf "${THISPKG_DIR}"
for INSTALL_DIR in "${PKG_DIR}" "${THISPKG_DIR}"; do
	
	cd "$MINT_BUILD_DIR"
	make DESTDIR="${INSTALL_DIR}" install || exit 1
	
	mkdir -p "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	cd "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	for i in addr2line ar arconv as c++ nm cpp csize cstrip flags g++ gcc gcov gfortran ld ld.bfd mintbin objcopy objdump ranlib stack strip symex readelf dlltool dllwrap; do
		if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
			rm -f ${i} ${i}${BUILD_EXEEXT}
			$LN_S ../../bin/${TARGET}-$i${BUILD_EXEEXT} $i
		fi
	done
	
	cd "${INSTALL_DIR}/${PREFIX}/bin"
	${STRIP} *
	
	if test -x ${TARGET}-g++ && test ! -h ${TARGET}-g++; then
		rm -f ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}
		mv ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++
	fi
	if test -x ${TARGET}-c++ && test ! -h ${TARGET}-c++; then
		rm -f ${TARGET}-c++${BUILD_EXEEXT} ${TARGET}-c++
		$LN_S ${TARGET}-g++ ${TARGET}-c++
	fi
	if test -x ${TARGET}-gcc && test ! -h ${TARGET}-gcc; then
		rm -f ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-gcc-${BASE_VER}
		mv ${TARGET}-gcc${BUILD_EXEEXT} ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-gcc
	fi
	if test ${BASE_VER} != ${gcc_dir_version} && test -x ${TARGET}-gcc-${gcc_dir_version} && test ! -h ${TARGET}-gcc-${gcc_dir_version}; then
		rm -f ${TARGET}-gcc-${gcc_dir_version}${BUILD_EXEEXT} ${TARGET}-gcc-${gcc_dir_version}
		$LN_S ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-gcc-${gcc_dir_version}
	fi
	if test -x ${TARGET}-cpp && test ! -h ${TARGET}-cpp; then
		rm -f ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-cpp-${BASE_VER}
		mv ${TARGET}-cpp${BUILD_EXEEXT} ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-cpp
	fi
	
	cd "${INSTALL_DIR}"
	
	rm -f ${PREFIX#/}/share/info/dir
	for f in ${PREFIX#/}/share/man/*/* ${PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
	
	case $host in
		cygwin*) LTO_PLUGIN=cyglto_plugin-0.dll; MY_LTO_PLUGIN=cyglto_plugin_mintelf.dll ;;
		mingw* | msys*) LTO_PLUGIN=liblto_plugin-0.dll; MY_LTO_PLUGIN=liblto_plugin_mintelf.dll ;;
		macos*) LTO_PLUGIN=liblto_plugin.dylib; MY_LTO_PLUGIN=liblto_plugin_mintelf.dylib ;;
		*) LTO_PLUGIN=liblto_plugin.so.0.0.0; MY_LTO_PLUGIN=liblto_plugin_mintelf.so.0.0.0 ;;
	esac
	
	rm -f */*/libiberty.a
	rm -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/*.la
	rm -f ${PREFIX#/}/lib/${TARGET}/lib/*.la ${PREFIX#/}/lib/${TARGET}/lib/*/*.la
	${STRIP} ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/{cc1,cc1plus,cc1obj,cc1objplus,f951,collect2,lto-wrapper,lto1}${BUILD_EXEEXT}
	${STRIP} ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/${LTO_PLUGIN}
	${STRIP} ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/plugin/gengtype${BUILD_EXEEXT}
	${STRIP} ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/install-tools/fixincl${BUILD_EXEEXT}
	rmdir ${PREFIX#/}/include
	
	if test -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN}; then
		mkdir -p ${PREFIX#/}/lib/bfd-plugins
		cd ${PREFIX#/}/lib/bfd-plugins
		rm -f ${MY_LTO_PLUGIN}
		$LN_S ../../${BUILD_LIBDIR##*/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN} ${MY_LTO_PLUGIN}
		cd "${INSTALL_DIR}"
	fi
	
	find ${PREFIX#/} -name "*.a" -exec "${strip}" -S -x '{}' \;
	find ${PREFIX#/} -name "*.a" -exec "${ranlib}" '{}' \;
	
	cd ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/include-fixed && {
		for i in `find . -type f`; do
			case $i in
			./README | ./limits.h | ./syslimits.h) ;;
			*) echo "removing fixed include file $i"; rm -f $i ;;
			esac
		done
		for i in `find . -depth -type d`; do
			test "$i" = "." || rmdir "$i"
		done
	}
done

cd "${THISPKG_DIR}" || exit 1

TARNAME=$PACKAGENAME$VERSION-${TARGET##*-}${VERSIONPATCH}
BINTARNAME=${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-doc.tar.xz ${PREFIX#/}/share/info ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz ${PREFIX#/}

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
