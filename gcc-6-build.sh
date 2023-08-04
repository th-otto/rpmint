#!/bin/sh

# This is an almost automatic script for building the binary packages.
# It is designed to be run on linux, cygwin or mingw,
# but it should run fine on other GNU environments.

me="$0"

unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

scriptdir=${0%/*}
scriptdir=`cd "${scriptdir}"; pwd`

PACKAGENAME=gcc
VERSION=-6.2.1
VERSIONPATCH=-20220824
REVISION="MiNT ${VERSIONPATCH#-}"

#
# For which target we build-
# should be either m68k-atari-mint or m68k-atari-mintelf
#
TARGET=${1:-m68k-atari-mint}

#
# The hosts compiler.
# To build the 32bit version for linux,
# invoke this script with
# GCC="gcc -m32" GXX="g++ -m32"
# You will also need to have various 32bit flavours
# of system libraries installed.
# For other 32bit hosts (mingw32 and cygwin32)
# use the appropriate shell for that system.
#
GCC=${GCC-gcc}
GXX=${GXX-g++}

# Where to put the executables for later use.
# This should be the same as the one configured
# in the binutils script
#
here=`pwd`
PKG_DIR="$here/binary7-package"

#
# The prefix where the executables should
# be installed later. If installed properly,
# this actually does not matter much, since
# all relevant directories are looked up
# relative to the executable
#
TAR=${TAR-tar}
TAR_OPTS=${TAR_OPTS---owner=0 --group=0}
SED_INPLACE=-i
case `uname -s` in
	MINGW64*) host=mingw64; PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; PREFIX=/mingw32; ;;
	MINGW*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; PREFIX=/$host ;;
	MSYS*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; PREFIX=/$host ;;
	CYGWIN*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi; PREFIX=/usr ;;
	Darwin*) host=macos; STRIP=strip; TAR_OPTS=; SED_INPLACE="-i .orig"; PREFIX=/opt/cross-mint ;;
	*) PREFIX=/usr
	   host=linux64
	   if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then
	      host=linux32
	      PKG_DIR+="-32bit"
	      export PATH=${PKG_DIR}/usr/bin:$PATH
          #
          # This is needed because otherwise configure scripts
          # will pick /usr/${TARGET}/bin/$tool which will be a 64bit version
          #
	      build_time_tools=--with-build-time-tools=${PKG_DIR}/usr/${TARGET}/bin
	   fi
	   ;;
esac
case $TARGET in
	m68k-amigaos*)
		PATH="/opt/amiga/bin:$PATH"
		PREFIX=/opt/amiga
		sysroot=
		headers=--with-headers=$PREFIX/$TARGET/sys-include
		if test ! -f "${PREFIX}/${TARGET}/sys-include/_newlib_version.h"; then
			echo "amigaos headers must be installed in ${PREFIX}/${TARGET}/sys-include" >&2
			exit 1
		fi
		;;
	*)
		sysroot=--with-sysroot="${PREFIX}/${TARGET}/sys-root"
		headers=
		if test ! -f "${PREFIX}/${TARGET}/sys-root/usr/include/compiler.h"; then
			echo "mintlib headers must be installed in ${PREFIX}/${TARGET}/sys-root/usr/include" >&2
			exit 1
		fi
		;;
esac

#
# Where to look for the original source archives
#
ARCHIVES_DIR="$here"

#
# where to look for mpfr/gmp/mpc/isl etc.
# currently only needed on Darwin, which lacks
# libmpc.
# Should be a static compiled version, so the
# compiler does not depend on non-standard shared libs
# We will compile now the required libraries before
# trying to compile gcc, in order to produce universal
# libraries
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
PKG_DIR="$here/amiga-package"

#
# Where to put the binary packages
#
DIST_DIR="$here/pkgs"

#
# Where to look up the source tree.
#
srcdir="$HOME/m68k-atari-mint-gcc"
if test -d "$srcdir"; then
	if test -f "$srcdir/gcc/config/m68k/mint.h"; then
		# MiNT patches already applied
		touch ".patched-${PACKAGENAME}${VERSION}"
	fi
else
	echo "$srcdir not found" >&2
	echo "please clone https://github.com/th-otto/m68k-atari-mint-gcc" >&2
	echo "and checkout the mint/gcc-6 branch" >&2
	exit 1 
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
# whether to include the modula-2 backend
#
with_m2=false

#
# whether to include the ada backend
#
with_ada=false
case $host in
	linux64 | linux32)
		;;
	*)
		# ADA is currently only available for linux
		with_ada=false
		# D backend takes too long on github runners
		with_D=false
		# m2 backend needs pthread.h
		with_m2=false
		;;
esac


#
# this patch can be recreated by
# - cloning https://github.com/th-otto/m68k-atari-mint-gcc.git
# - checking out the mint/gcc-6 branch
# - running git diff releases/gcc-6.5.0 HEAD
#
PATCHES="patches/gcc/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch"
OTHER_PATCHES="
patches/gmp/gmp-universal.patch
patches/gmp/gmp-6.2.1-CVE-2021-43618.patch
patches/gmp/gmp-6.2.1-arm64-invert_limb.patch
gmp-for-gcc.sh
zstd-for-gcc.sh
"

if test ! -f ".patched-${PACKAGENAME}${VERSION}"; then
	found=false
	for f in "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.xz" \
	         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.bz2" \
	         "${PACKAGENAME}${VERSION}.tar.xz" \
	         "${PACKAGENAME}${VERSION}.tar.bz2"; do
		if test -f "$f"; then
			found=true
			$TAR xf "$f" || exit 1
			break
		fi
	done
	if ! $found; then
		echo "no archive found for ${PACKAGENAME}${VERSION}" >&2
		echo "download it from https://ftp.gnu.org/gnu/gcc/ and" >&2
		echo "put it in this directory, or in $ARCHIVES_DIR" >&2
		exit 1
	fi
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
else
	for f in $PATCHES; do
	  if ! test -f "$f"; then
	    echo "missing patch $f" >&2
	    exit 1
	  fi
	done
fi

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi

if test -d /usr/lib64 -a $host = linux64; then
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

BASE_VER=$(cat $srcdir/gcc/BASE-VER)
if test "$BASE_VER" != "${VERSION#-}"; then
	echo "version mismatch: this script is for gcc ${VERSION#-}, but gcc source is version $BASE_VER" >&2
	exit 1
fi
gcc_major_version=$(echo $BASE_VER | cut -d '.' -f 1)
gcc_dir_version=${BASE_VER}
gccsubdir=${BUILD_LIBDIR}/gcc/${TARGET}/${gcc_dir_version}
gxxinclude=/usr/include/c++/${gcc_dir_version}

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
# FIXME: maybe use $GCC -dumpmachine intead?
#
for a in "" -1.16 -1.15 -1.14 -1.13 -1.12 -1.11 -1.10; do
	BUILD=`/usr/share/automake${a}/config.guess 2>/dev/null`
	test "$BUILD" != "" && break
	test "$host" = "macos" && BUILD=`/opt/local/share/automake${a}/config.guess 2>/dev/null`
	test "$BUILD" != "" && break
done
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`
case $BUILD in
	x86_64-pc-mingw32) BUILD=x86_64-pc-msys ;;
	i686-pc-mingw32) BUILD=i686-pc-msys ;;
esac

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer -Wno-implicit-fallthrough"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD=""
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
LDFLAGS_FOR_TARGET=

enable_lto=--disable-lto
enable_plugin=--disable-plugin
enable_libphobos=
languages=c
$with_fortran && languages="$languages,fortran"
$with_ada && languages="$languages,ada"
$with_D && { languages="$languages,d"; enable_libphobos=; } # --enable-libphobos does not work because of missing swapcontext() in mintlib
$with_m2 && languages="$languages,m2"
ranlib=ranlib
STRIP=${STRIP-strip -p}

case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
        enable_lto=--enable-lto
        case "${BUILD}" in
        *-*-linux*)
            enable_plugin=--enable-plugin
            ;;
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
	strip=`which "${TARGET}-strip" 2>/dev/null`
	as=`which "${TARGET}-as" 2>/dev/null`
fi
if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$as" -o ! -x "$strip"; then
	echo "cross-binutil tools for ${TARGET} not found" >&2
	exit 1
fi

mpfr_config=

unset GLIBC_SO
with_zstd=

case $host in
	macos*)
		GCC=/usr/bin/clang
		GXX=/usr/bin/clang++
		MACOSX_DEPLOYMENT_TARGET=10.9
		ARCHS="-arch x86_64"
		case `$GCC --print-target-triple 2>/dev/null` in
		arm64* | aarch64*)
			BUILD_ARM64=yes
			;;
		esac
		if test `uname -r | cut -d . -f 1` -ge 20; then
			BUILD_ARM64=yes
		fi
		if test "$BUILD_ARM64" = yes; then
			ARCHS="${ARCHS} -arch arm64"
			MACOSX_DEPLOYMENT_TARGET=11
		fi
		export MACOSX_DEPLOYMENT_TARGET
		CFLAGS_FOR_BUILD="-pipe -O2 ${ARCHS}"
		CXXFLAGS_FOR_BUILD="-pipe -O2 -stdlib=libc++ ${ARCHS}"
		LDFLAGS_FOR_BUILD="-Wl,-headerpad_max_install_names ${ARCHS}"
		mpfr_config="--with-mpc=${CROSSTOOL_DIR}"
		if test $gcc_major_version -ge 10; then
			export PKG_CONFIG_LIBDIR="$PKG_CONFIG_LIBDIR:${CROSSTOOL_DIR}/lib/pkgconfig"
			with_zstd="--with-zstd=${CROSSTOOL_DIR}"
		fi
		;;
esac

export CC="${GCC}"
export CXX="${GXX}"


fail()
{
	component="$1"
	echo "configuring $component failed"
	exit 1
}


#
# Now, for darwin, build gmp etc.
#
. ${scriptdir}/gmp-for-gcc.sh
if test $gcc_major_version -ge 10; then
	. ${scriptdir}/zstd-for-gcc.sh
fi

cd "$MINT_BUILD_DIR"

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
	--with-gxx-include-dir=${PREFIX}/${TARGET}/sys-root${gxxinclude} \
	--with-default-libstdcxx-abi=gcc4-compatible \
	--with-gcc --with-gnu-as --with-gnu-ld \
	--with-system-zlib \
	--disable-libgomp \
	--without-newlib \
	--disable-libstdcxx-pch \
	--disable-threads \
	--disable-win32-registry \
	$enable_lto \
	$enable_libphobos \
	--enable-ssp \
	--enable-libssp \
	$enable_plugin \
	--disable-decimal-float \
	--disable-nls \
	$with_zstd \
	--with-libiconv-prefix="${PREFIX}" \
	--with-libintl-prefix="${PREFIX}" \
	$mpfr_config \
	$build_time_tools \
	$headers \
	$sysroot \
	--enable-languages="$languages" || fail "gcc"


case $host in
	linux32)
		# make sure to pick up the just-compiled 32bit version of ld, not
		# some previous 64bit version
		# symptom of using a wrong linker is an error message "error loading plugin: wrong ELF class: ELFCLASS32" in the config.log
		sed $SED_INPLACE "s|S\[\"build_tooldir\"\]=.*|S[\"build_tooldir\"]=\"${PKG_DIR}${PREFIX}/${TARGET}\"|" config.status
		./config.status
		;;
esac

${MAKE} $JOBS all-gcc || exit 1
${MAKE} $JOBS all-target-libgcc || exit 1
${MAKE} $JOBS || exit 1

THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
rm -rf "${THISPKG_DIR}"
for INSTALL_DIR in "${PKG_DIR}" "${THISPKG_DIR}"; do
	
	cd "$MINT_BUILD_DIR"
	${MAKE} DESTDIR="${INSTALL_DIR}" install >/dev/null || exit 1
	
	mkdir -p "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	cd "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin"
	
	for tool in c++ cpp g++ gcc gcov gfortran gdc; do
		if test -x ../../bin/${TARGET}-${tool}; then
			rm -f ${tool} ${tool}${BUILD_EXEEXT}
			$LN_S ../../bin/${TARGET}-${tool}${BUILD_EXEEXT} ${tool}
		fi
	done
	
	cd "${INSTALL_DIR}/${PREFIX}/bin"
	${STRIP} *
	
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
	for tool in gcc gfortran gdc gccgo go gofmt gm2 \
	            gnat gnatbind gnatchop gnatclean gnatkr gnatlink gnatls gnatmake gnatname gnatprep gnatxref; do
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

	cd "${INSTALL_DIR}"
	
# that directory only contains the gdb pretty printers;
# on the host we don't want them because they would conflict
# with the system ones; on the target we don't need them
# because gdb does not work
	rm -rf ${PREFIX#/}/share/gcc-${gcc_dir_version}
	if test -d ${PREFIX#/}/${TARGET}/lib; then find ${PREFIX#/}/${TARGET}/lib -name "libstdc++*.py" -delete; fi
	if test -d ${PREFIX#/}/lib; then find ${PREFIX#/}/lib -name "libstdc++*.py" -delete; fi

	rm -f ${PREFIX#/}/share/info/dir
	for f in ${PREFIX#/}/share/man/*/* ${PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
	
	# This is a experimental fork of gcc-6,
	# and we don't want it to replace the default compilers
	for f in c++ cpp g++ gcc gcc-ar gcc-nm gcc-ranlib gcov gcov gcov-dump gcov-tool; do
		rm -f "${INSTALL_DIR}/${PREFIX}/bin/${TARGET}-$f"
		rm -f "${INSTALL_DIR}/${PREFIX}/${TARGET}/bin/$f"
	done

	rm -f */*/libiberty.a
	find . -type f -name "*.la" -delete -printf "rm %p\n"

#
# move compiler dependant libraries to the gcc subdirectory
#
	cd ${INSTALL_DIR}${PREFIX}/${TARGET}/lib || exit 1
	libs=`find . -name "lib*.a" ! -path "*/gcc/*"`
	$TAR -c $libs | $TAR -x -C ${INSTALL_DIR}${gccsubdir}
	rm -f $libs
	for i in libgfortran.spec libgomp.spec libitm.spec libsanitizer.spec libmpx.spec libgphobos.spec; do
		test -f $i && mv $i ${INSTALL_DIR}${gccsubdir}
		find . -name "$i" -delete
	done
	rmdir m*/*/*/* || :
	rmdir m*/*/* || :
	rmdir m*/* || :
	rmdir m* || :
	cd "${INSTALL_DIR}"

	case $host in
		cygwin*) soext=.dll; LTO_PLUGIN=cyglto_plugin-0${soext}; MY_LTO_PLUGIN=cyglto_plugin_mintelf-${gcc_dir_version}${soext} ;;
		mingw* | msys*) soext=.dll; LTO_PLUGIN=liblto_plugin-0${soext}; MY_LTO_PLUGIN=liblto_plugin_mintelf-${gcc_dir_version}${soext} ;;
		macos*) soext=.dylib; LTO_PLUGIN=liblto_plugin${soext}; MY_LTO_PLUGIN=liblto_plugin_mintelf-${gcc_dir_version}${soext} ;;
		*) soext=.so; LTO_PLUGIN=liblto_plugin${soext}.0.0.0; MY_LTO_PLUGIN=liblto_plugin_mintelf${soext}.${gcc_dir_version} ;;
	esac
	
	for f in ${gccsubdir#/}/{cc1,cc1plus,cc1obj,cc1objplus,f951,d21,collect2,lto-wrapper,lto1,gnat1,gnat1why,gnat1sciln,go1,brig1,cc1gm2,g++-mapper-server}${BUILD_EXEEXT} \
		${gccsubdir#/}/${LTO_PLUGIN} \
		${gccsubdir#/}/plugin/gengtype${BUILD_EXEEXT} \
		${gccsubdir#/}/plugin/m2rte${soext} \
		${gccsubdir#/}/install-tools/fixincl${BUILD_EXEEXT}; do
		test -f "$f" && ${STRIP} "$f"
	done

	rmdir ${PREFIX#/}/include
	
	if test -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN}; then
		mkdir -p ${PREFIX#/}/lib/bfd-plugins
		cd ${PREFIX#/}/lib/bfd-plugins
		rm -f ${MY_LTO_PLUGIN}
		$LN_S ../../${BUILD_LIBDIR##*/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN} ${MY_LTO_PLUGIN}
		cd "${INSTALL_DIR}"
	fi
	
	find ${PREFIX#/}/${TARGET} -name "*.a" -exec "${strip}" -S -x '{}' \;
	find ${PREFIX#/}/${TARGET} -name "*.a" -exec "${ranlib}" '{}' \;
	find ${gccsubdir#/} -name "*.a" -exec "${strip}" -S -x '{}' \;
	find ${gccsubdir#/} -name "*.a" -exec "${ranlib}" '{}' \;
	
	cd ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/include-fixed && {
		for i in `find . -type f`; do
			case $i in
			./README | ./limits.h | ./syslimits.h) ;;
			*) echo "removing fixed include file $i"; rm -f $i ;;
			esac
		done
		for i in `find . -type l`; do
			rm -fv $i
		done
		for i in `find . -depth -type d`; do
			test "$i" = "." || rmdir "$i"
		done
	}

	# these are currently identically compiled 2 times; FIXME
	# this only happens if gcc was patched to put the m68000 libraries also
	# in a sub-directory of /usr/lib
	m68000=`"${INSTALL_DIR}/${PREFIX}/bin/${TARGET}-gcc" -m68000 -print-multi-directory`
	if test "$m68000" = "m68000"; then
		for dir in . mshort mfastcall mfastcall/mshort; do
			for f in libgcov.a libgcc.a libcaf_single.a; do
				rm -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/$dir/$f
			done
		done
		for dir in mfastcall/mshort mfastcall mshort; do
			rmdir ${BUILD_LIBDIR#/}/gcc/${TARGET}/$dir 2>/dev/null
		done
	fi

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
	fortran=`find ${gccsubdir#/} -name finclude`
	fortran="$fortran "${PREFIX#/}/bin/*gfortran*
	fortran="$fortran "${PREFIX#/}/${TARGET}/bin/*gfortran*
	fortran="$fortran "${gccsubdir#/}/f951
	fortran="$fortran "`find ${gccsubdir#/} -name libcaf_single.a`
	fortran="$fortran "`find ${gccsubdir#/} -name "*gfortran*"`
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-fortran-${host}.tar.xz $fortran || exit 1
	rm -rf $fortran
fi

#
# create a separate archive for the D backend
#
if $with_D; then
	D=
	test -d ${gccsubdir#/}include/d && D="$D "${gccsubdir#/}include/d
	D="$D "`find ${gccsubdir#/} -name "libgdruntim*"`
	D="$D "`find ${gccsubdir#/} -name "libgphobos*"`
	D="$D "`find ${gccsubdir#/} -name "d21*"`
	D="$D "${PREFIX#/}/bin/*-gdc*
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-d-${host}.tar.xz $D || exit 1
	rm -rf $D
fi

#
# create a separate archive for the ada backend
#
if $with_ada; then
	ada=`find ${gccsubdir#/} -name adainclude`
	ada="$ada "`find ${gccsubdir#/} -name adalib`
	ada="$ada "`find ${gccsubdir#/} -name "gnat1*"`
	ada="$ada "${PREFIX#/}/bin/${TARGET}-gnat*
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-ada-${host}.tar.xz $ada || exit 1
	rm -rf $ada
fi

#
# create a separate archive for the modula-2 backend
#
if $with_m2; then
	m2=
	test -d ${gccsubdir#/}/m2 && m2="$m2 "${gccsubdir#/}/m2
	m2="$m2 "`find ${gccsubdir#/} -name "libm2*"`
	m2="$m2 "`find ${gccsubdir#/} -name "cc1gm2*"`
	test -f ${gccsubdir#/}/plugin/m2rte${soext} && m2="$m2 ${gccsubdir#/}/plugin/m2rte${soext}"
	m2="$m2 "${PREFIX#/}/bin/${TARGET}-gm2*
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-m2-${host}.tar.xz $m2 || exit 1
	rm -rf $m2
fi

#
# create archive for all others
#
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz ${PREFIX#/}

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}.tar.xz ${PATCHES} ${OTHER_PATCHES}
cp -p "$me" ${DIST_DIR}/${PACKAGENAME}${VERSION}${VERSIONPATCH}-build.sh
