#!/bin/sh

# This is an almost automatic script for building the binary packages.
# It is designed to be run on linux, cygwin or mingw,
# but it should run fine on other GNU environments.

me="$0"

PACKAGENAME=gcc
VERSION=-2.95.3
VERSIONPATCH=-20200907
REVISION="MiNT ${VERSIONPATCH#-}"

#
# For which target we build-
# should be either m68k-atari-mint or m68k-atari-mintelf
#
TARGET=m68k-atari-mint
PREFIX=/opt/gcc2
sys_root=/usr/${TARGET}/sys-root

#
# the hosts compiler
#
GCC=${GCC-gcc}
GXX=${GXX-g++}

unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

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
	MINGW64*)
		host=mingw64
		MINGW_PREFIX=/mingw64
		BUILD=x86_64-w64-mingw32
		;;
	MINGW32*)
		host=mingw32
		MINGW_PREFIX=/mingw32
		BUILD=i686-pc-mingw32
		;;
	MINGW*)
		if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then
			host=mingw32
			BUILD=i686-pc-mingw32
		else
			host=mingw64
			BUILD=x86_64-w64-mingw32
		fi
		MINGW_PREFIX=/$host
		;;
	MSYS*)
		if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then
			host=mingw32
			BUILD=i686-pc-mingw32
		else
			host=mingw64
			BUILD=x86_64-w64-mingw32
		fi
		MINGW_PREFIX=/$host
		;;
	CYGWIN*)
		if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then
			host=cygwin32
			BUILD=i686-pc-cygwin
		else
			host=cygwin64
			BUILD=x64_64-pc-cygwin
		fi
		;;
	Darwin*)
		host=macos
		STRIP=strip
		TAR_OPTS=
		BUILD=x86_64-apple-darwin
		;;
	Linux*)
		host=linux64
		BUILD=x86_64-pc-linux
		if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then
			host=linux32
		fi
		;;
	*)
		echo "Build on $host not supported!" >&2
		exit 1
		;;
esac

export PATH="${PREFIX}/bin:$PATH"
case $host in
macos*)
	CC=clang
	CXX=clang++
	;;
*)
	CC=${GCC}
	CXX=${GXX}
	;;
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
	srcdir="$here/${PACKAGENAME}${VERSION}"
fi

#
# whether to include the fortran backend
#
with_fortran=false

#
# whether to include the D backend
#
with_D=false

#
# this patch can be recreated by
# - cloning https://github.com/th-otto/m68k-atari-mint-gcc.git
# - checking out the mint/gcc-10 branch
# - running git diff releases/gcc-10.2.0 HEAD
#
# when a new GCC is released:
#   cd <directory where m68k-atari-mint-gcc.git> has been cloned
#   fetch new commits from upstream:
#      git checkout master
#      git pull --rebase upstream master
#      git push
#   fetch new tags etc:
#      git fetch --all
#      git push --tags
#   merge new release into our branch:
#      git checkout mint/gcc-10
#      git merge releases/gcc-10.2.0 (& commit)
#      git push
#
PATCHES="patches/gcc/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch"

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
if test ! -f "${sys_root}/usr/include/compiler.h"; then
	echo "mintlib headers must be installed in ${sys_root}/usr/include" >&2
	exit 1
fi

BUILD_LIBDIR=${PREFIX}/lib

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

BASE_VER=${VERSION#-}
if ! grep -q 'version_string.*2\.95\.3' "$srcdir/gcc/version.c"; then
	echo "version mismatch: this script is for gcc ${VERSION#-}, but gcc source is version "`grep version_string $srcdir/gcc/version.c` >&2
	exit 1
fi
gcc_dir_version=$BASE_VER
gccsubdir=${BUILD_LIBDIR}/gcc-lib/${TARGET}/${gcc_dir_version}

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD=""
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
LDFLAGS_FOR_TARGET=

languages=c,c++
$with_fortran && languages="$languages,fortran"
$with_D && languages="$languages,d"
ranlib=ranlib
STRIP=${STRIP-strip}

BUILD_EXEEXT=
LN_S="ln -s"
case $host in
	cygwin* | mingw* | msys*) BUILD_EXEEXT=.exe ;;
esac
case $host in
	mingw* | msys*) LN_S="cp -p" ;;
esac

try="${PREFIX}/bin/${TARGET}-${ranlib}"
if test -x "$try"; then
	ranlib="$try"
	strip="${PREFIX}/bin/${TARGET}-strip"
	as="${PREFIX}/bin/${TARGET}-as"
else
	ranlib=`which ${TARGET}-${ranlib} 2>/dev/null`
	strip=`which "${TARGET}-strip" 2>/dev/null`
	as=`which "${TARGET}-as" 2>/dev/null`
fi
if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$as" -o ! -x "$strip"; then
	echo "cross-binutil tools for ${TARGET} not found" >&2
	exit 1
fi

mpfr_config=

case $host in
	macos*)
		GCC=/usr/bin/clang
		GXX=/usr/bin/clang++
		export MACOSX_DEPLOYMENT_TARGET=10.6
		CFLAGS_FOR_BUILD="-pipe -O2 -arch x86_64"
		CXXFLAGS_FOR_BUILD="-pipe -O2 -stdlib=libc++ -arch x86_64"
		LDFLAGS_FOR_BUILD="-Wl,-headerpad_max_install_names -arch x86_64"
		mpfr_config="--with-mpc=${CROSSTOOL_DIR} --with-gmp=${CROSSTOOL_DIR} --with-mpfr=${CROSSTOOL_DIR}"
		;;
esac

case $BUILD in
	i686-*-msys* | x86_64-*-msys*)
		mpfr_config="--with-mpc=${MINGW_PREFIX} --with-gmp=${MINGW_PREFIX} --with-mpfr=${MINGW_PREFIX}"
		;;
esac

# On 64-bit architecture GNU Assembler crashes writing out an object, due to
# (probably) miscalculated structure sizes.  There could be some other bugs
# lurking there in 64-bit mode, but I have little incentive chasing them.
# Just compile everything in 32-bit mode and forget about the issues.
case `uname -m` in
  x86_64)
    ARCH=" -m32"
    BUILD=i686-${BUILD#*-}
    test "$host" = linux64 && host=linux32
    ;;
esac
CC="$CC$ARCH"
CXX="$CXX$ARCH"

rm -f ${PREFIX}/${TARGET}/sys-include ${PREFIX}/${TARGET}/sys-root

	CC="$CC" \
	CXX="$CXX" \
	CFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD" \
	CFLAGS="$CFLAGS_FOR_BUILD" \
	CXXFLAGS_FOR_BUILD="$CXXFLAGS_FOR_BUILD" \
	CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
	BOOT_CFLAGS="$CFLAGS_FOR_BUILD" \
	CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET" \
	CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET" \
	LDFLAGS_FOR_BUILD="$LDFLAGS_FOR_BUILD" \
	LDFLAGS="$LDFLAGS_FOR_BUILD" \
$srcdir/configure \
	--target="${TARGET}" --build="$BUILD" --host=$BUILD \
	--prefix="${PREFIX}" \
	--libdir="$BUILD_LIBDIR" \
	--bindir="${PREFIX}/bin" \
	--libexecdir='${libdir}' \
	--infodir=${PREFIX}/share/info \
	--mandir=${PREFIX}/share/man \
	--with-gcc --with-gnu-as --with-gnu-ld \
	--disable-threads \
	--disable-nls \
	$mpfr_config \
	--with-headers="${sys_root}/usr/include" \
	--enable-languages="$languages" \
	|| exit 1

ln -sf ${sys_root} ${PREFIX}/${TARGET}/sys-root

${MAKE} all-gcc || exit 1
${MAKE} install-gcc || exit 1

rm -rf ${PREFIX}/${TARGET}/sys-include
rm -rf ${PREFIX}/${TARGET}/lib
ln -s sys-root/usr/include ${PREFIX}/${TARGET}/sys-include

${MAKE}

${MAKE} install

rm -f ${PREFIX}/share/info/dir
for f in ${PREFIX}/share/man/*/* ${PREFIX}/share/info/*; do
	case $f in
	*.gz) ;;
	*) rm -f ${f}.gz; gzip -9 $f ;;
	esac
done
	
for i in c++ cpp g++ gcc gcov gfortran gdc; do
	if test -x ../../bin/${TARGET}-$i; then
		rm -f ${i} ${i}${BUILD_EXEEXT}
		$LN_S ../../bin/${TARGET}-$i${BUILD_EXEEXT} $i
	fi
done
	
cd "${PREFIX}/bin"
${STRIP} *
	
gcc_major_version=$(echo $BASE_VER | cut -d '.' -f 1)

if test -x ${TARGET}-g++ && test ! -h ${TARGET}-g++; then
	rm -f ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}
	rm -f ${TARGET}-g++-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-g++-${gcc_major_version}
	mv ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT}
	$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++${BUILD_EXEEXT}
	$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${gcc_major_version}${BUILD_EXEEXT}
fi
if test -x ${TARGET}-c++ && test ! -h ${TARGET}-c++; then
	rm -f ${TARGET}-c++${BUILD_EXEEXT} ${TARGET}-c++
	$LN_S ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-c++${BUILD_EXEEXT}
fi
for tool in gcc gfortran gdc gccgo go gofmt; do
	if test -x ${TARGET}-${tool} && test ! -h ${TARGET}-${tool}; then
		rm -f ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}-${BASE_VER}
		rm -f ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}
		mv ${TARGET}-${tool}${BUILD_EXEEXT} ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}${BUILD_EXEEXT}
		if test ${BASE_VER} != ${gcc_major_version}; then
			rm -f ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}
			rm -f ${tool}-${gcc_major_version}${BUILD_EXEEXT} ${tool}-${gcc_major_version}${BUILD_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT}
		fi
	fi
done
if test -x ${TARGET}-cpp && test ! -h ${TARGET}-cpp; then
	rm -f ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-cpp-${BASE_VER}
	mv ${TARGET}-cpp${BUILD_EXEEXT} ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT}
	$LN_S ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-cpp${BUILD_EXEEXT}
fi

find ${PREFIX}/${TARGET}/lib -name libiberty.a -delete -printf "rm %p\n"
find ${PREFIX}/lib -name libiberty.a -delete -printf "rm %p\n"
find ${PREFIX}/ -type f -name "*.la" -delete -printf "rm %p\n"
# seems to be duplicate to m5475
find ${PREFIX}/${TARGET} -type d -name m5200 -exec rm -rf '{}' \;
find ${gccsubdir} -type d -name m5200 -exec rm -rf '{}' \;

#
# move compiler dependant libraries to the gcc subdirectory
#
libs=`find ${PREFIX}/${TARGET}/lib -name "libstdc*" ! -path "*/gcc-lib/*" | sed -e "s@^${PREFIX}/${TARGET}/lib/@@"`
for i in $libs; do
    d=${gccsubdir}/${i%%.*}.a
    rm -f $d
	mv ${PREFIX}/${TARGET}/lib/$i $d || exit 1
done
#
# replace target library directory by symlink to sys_root
#
find ${PREFIX}/${TARGET}/lib -depth -type d -exec rmdir '{}' \;
ln -s sys-root/usr/lib ${PREFIX}/${TARGET}/lib || exit 1


for f in ${gccsubdir#/}/{cc1,cc1plus,cc1obj,cc1objplus,f77,f951,d21,collect2,lto-wrapper,lto1,gnat1,gnat1why,gnat1sciln,go1,brig1}${BUILD_EXEEXT} \
	${gccsubdir#/}/${LTO_PLUGIN} \
	${gccsubdir#/}/plugin/gengtype${BUILD_EXEEXT} \
	${gccsubdir#/}/install-tools/fixincl${BUILD_EXEEXT}; do
	test -f "${PREFIX}/$f" && ${STRIP} "$f"
done

rmdir ${PREFIX}/include

find ${PREFIX}/${TARGET} -name "*.a" -exec "${strip}" -S -x '{}' \;
find ${PREFIX}/${TARGET} -name "*.a" -exec "${ranlib}" '{}' \;
find ${gccsubdir} -name "*.a" -exec "${strip}" -S -x '{}' \;
find ${gccsubdir} -name "*.a" -exec "${ranlib}" '{}' \;


THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
rm -rf "${THISPKG_DIR}"
mkdir -p "${THISPKG_DIR}/${PREFIX}"
cp -pr ${PREFIX}/. "${THISPKG_DIR}/${PREFIX}"
for tool in ar as ld ld.bdf nm objcopy objdump ranlib size strings strip; do
	rm -f ${THISPKG_DIR}/${PREFIX}/bin/${TARGET}-${tool}
	ln -s /usr/bin/${TARGET}-${tool} ${THISPKG_DIR}/${PREFIX}/bin/${TARGET}-${tool}
	rm -f ${THISPKG_DIR}/${PREFIX}/${TARGET}/bin/${tool}
	ln -s /usr/bin/${TARGET}-${tool} ${THISPKG_DIR}/${PREFIX}/${TARGET}/bin/${tool}
done

cd "${THISPKG_DIR}" || exit 1

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}${VERSIONPATCH}
BINTARNAME=${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-doc.tar.xz ${PREFIX#/}/share/info ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man
rm -rf ${PREFIX#/}/share/gcc*/python

#
# create a separate archive for the fortran backend
#
if $with_fortran; then
fortran=${gccsubdir#/}/finclude
fortran="$fortran "${gccsubdir#/}/*/finclude
fortran="$fortran "${gccsubdir#/}/f951
fortran="$fortran "`find ${gccsubdir#/} -name libcaf_single.a`
fortran="$fortran "`find ${gccsubdir#/} -name "*gfortran*"`
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-fortran-${host}.tar.xz $fortran || exit 1
rm -rf $fortran
fi

#
# create archive for all others
#
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz ${PREFIX#/}

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/${PACKAGENAME}${VERSION}${VERSIONPATCH}-build.sh
