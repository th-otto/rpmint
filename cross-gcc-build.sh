#!/bin/bash

#
# This script is for using the cross-compiler to
# build the native compiler for the target(s)
#

me="$0"

unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

scriptdir=${0%/*}
scriptdir=`cd "${scriptdir}"; pwd`

PACKAGENAME=gcc
VERSION=-14.1.0
VERSIONPATCH=-20240531
REVISION="MiNT ${VERSIONPATCH#-}"

#
# For which target we build-
# should be either m68k-atari-mint or m68k-atari-mintelf
#
TARGET=${1:-m68k-atari-mint}
if test "$TARGET" = m68k-atari-mintelf; then
REVISION="MiNT ELF ${VERSIONPATCH#-}"
fi

#
# The prefix where the executables should
# be installed later. If installed properly,
# this actually does not matter much, since
# all relevant directories are looked up
# relative to the executable
#
prefix=/usr
TARGET_PREFIX=/usr
TARGET_LIBDIR=${TARGET_PREFIX}/lib
TARGET_BINDIR=${TARGET_PREFIX}/bin

#
# Where to look for the original source archives
#
here=`pwd`
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
MINT_BUILD_DIR="$BUILD_DIR/gcc-cross-${TARGET##*-}-build"

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
with_fortran=true

#
# whether to include the D backend
# (currently does not work natively because of missing libphobos)
#
with_D=false

#
# whether to include the ada backend
#
with_ada=false

#
# whether to include the modula-2 backend
#
# FIXME: building the native compiler with a cross-compiler currently does not work,
# because m2/boot-bin/mklink is compiled using the cross-compiler, then executed
#
with_m2=false

#
# whether to use dwarf2 exceptions instead of sjlj.
# Only works for elf toolchains.
#
case $TARGET in
*-*-*elf)
	with_dw2_exceptions=--disable-sjlj-exceptions
	;;
esac


#
# this patch can be recreated by
# - cloning https://github.com/th-otto/m68k-atari-mint-gcc.git
# - checking out the mint/gcc-12 branch
# - running git diff releases/gcc-12.2.0 HEAD
#
PATCHES="patches/gcc/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.patch"
OTHER_PATCHES="
patches/gmp/gmp-universal.patch
patches/gmp/gmp-6.2.1-CVE-2021-43618.patch
patches/gmp/gmp-6.2.1-arm64-invert_limb.patch
gmp-for-gcc.sh
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
fi

if test ! -d "$srcdir"; then
	echo "$srcdir: no such directory" >&2
	exit 1
fi

#
# install mintlib if needed, so libstdc++ can be configured
#
if ! test -f ${prefix}/${TARGET}/sys-root/usr/include/compiler.h; then
	if test "${GITHUB_REPOSITORY}" != ""; then
		sudo mkdir -p ${prefix}/${TARGET}/sys-root/usr
		echo "fetching mintlib"
		wget -q -O - "https://tho-otto.de/snapshots/mintlib/mintlib-latest.tar.bz2" | sudo $TAR -C "${prefix}/${TARGET}/sys-root/usr" -xjf -
		echo "fetching fdlibm"
		wget -q -O - "https://tho-otto.de/snapshots/fdlibm/fdlibm-latest.tar.bz2" | sudo $TAR -C "${prefix}/${TARGET}/sys-root/usr" -xjf -
	fi
fi

if test ! -f "${prefix}/${TARGET}/sys-root/usr/include/compiler.h"; then
	echo "mintlib headers must be installed in ${prefix}/${TARGET}/sys-root/usr/include" >&2
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

BASE_VER=$(cat $srcdir/gcc/BASE-VER)
if test "$BASE_VER" != "${VERSION#-}"; then
	echo "version mismatch: this script is for gcc ${VERSION#-}, but gcc source is version $BASE_VER" >&2
	exit 1
fi
gcc_major_version=$(echo $BASE_VER | cut -d '.' -f 1)
gcc_dir_version=$gcc_major_version
gccsubdir=${TARGET_LIBDIR}/gcc/${TARGET}/${gcc_dir_version}
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

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

enable_lto=--disable-lto
enable_plugin=--disable-plugin
enable_libphobos=
languages=c,c++
$with_fortran && languages="$languages,fortran"
$with_ada && languages="$languages,ada"
$with_D && { languages="$languages,d"; enable_libphobos=; } # --enable-libphobos does not work because of missing swapcontext() in mintlib
$with_m2 && languages="$languages,m2"
ranlib=ranlib

case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
    	enable_lto=--enable-lto
    	languages="$languages,lto"
		# not here; we are just building it
		# ranlib=gcc-ranlib
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

ranlib=`which ${TARGET}-${ranlib}`
strip=`which "${TARGET}-strip"`
as=`which "${TARGET}-as"`
if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$as" -o ! -x "$strip"; then
	echo "cross-binutil tools for ${TARGET} not found" >&2
	exit 1
fi

gcc4_compat=
if test $gcc_major_version -lt 13; then
	# with gcc 13 and above, do not longer use the compatible interface
	gcc4_compat=--with-default-libstdcxx-abi=gcc4-compatible
fi

#
# gcc 13 and above need support for a zoneinfo database
# in std::chrono
#
zoneinfo=
if test $gcc_major_version -ge 13; then
	zoneinfo=--with-libstdcxx-zoneinfo=${TARGET_PREFIX}/share/zoneinfo
fi

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}

#
# this could eventually be extracted from gcc -print-multi-lib
#
CPU_CFLAGS_000="-m68000"    ; WITH_CPU_000=m68000
CPU_CFLAGS_020="-m68020-60" ; WITH_CPU_020=m68020-60
CPU_CFLAGS_v4e="-mcpu=5475" ; WITH_CPU_v4e=5475

#
# This should list the default target cpu last,
# so that any files left behind are compiled for this
#
ALL_CPUS="020 v4e 000"



fail()
{
	component="$1"
	echo "configuring $component failed"
	exit 1
}


export AS_FOR_TARGET="$as"
export RANLIB_FOR_TARGET="$ranlib"
export STRIP_FOR_TARGET="$strip"
export CC_FOR_TARGET="${TARGET}-gcc${VERSION}"
export GCC_FOR_TARGET="${TARGET}-gcc${VERSION}"
export CXX_FOR_TARGET="${TARGET}-g++${VERSION}"
export GFORTRAN_FOR_TARGET="${TARGET}-gfortran${VERSION}"
export GOC_FOR_TARGET="${TARGET}-goc${VERSION}"

for CPU in ${ALL_CPUS}; do
	cd "$here" || exit 1
	rm -rf "$MINT_BUILD_DIR"
	mkdir -p "$MINT_BUILD_DIR"
	
	cd "$MINT_BUILD_DIR" || exit 1
	
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval with_cpu=\${WITH_CPU_$CPU}
	STACKSIZE="-Wl,-stack,512k"

GCC_WRAPPER="$MINT_BUILD_DIR/gcc-wrapper.sh"
GXX_WRAPPER="$MINT_BUILD_DIR/gxx-wrapper.sh"

cat <<'EOF' > "${GCC_WRAPPER}"
#!/bin/sh

#
# Wrapper to invoke the cross-compiler to generate code for the
# intended architecture. We cannot use CFLAGS_FOR_TARGET, because
# that would only be used for the just-built xgcc, which is already
# a binary for the target in our case. We also cannot just add the
# flags to $CC, because that clashes when compiling multilibs.
# So what we do is to add the flags to $CC, use this
# script as the compiler, and keep only the last cpu-specific flags
#
cpu_flags=
args=
for i in "$@"; do
    case "$i" in
		-m68*) cpu_flags=$1 ;;
		-mcpu=*) cpu_flags=$1 ;;
        *)
        	i="${i//\\/\\\\}"
		    args="$args \"${i//\"/\\\"}\""
        	;;
    esac
done
EOF

cp "${GCC_WRAPPER}" "${GXX_WRAPPER}"
cat <<EOF >> "${GCC_WRAPPER}"
eval exec "${TARGET}-gcc${VERSION}" \$cpu_flags \$args
EOF
cat <<EOF >> "${GXX_WRAPPER}"
eval exec "${TARGET}-g++${VERSION}" \$cpu_flags \$args
EOF

chmod 755 "${GCC_WRAPPER}"
chmod 755 "${GXX_WRAPPER}"

	export CC="${GCC_WRAPPER} $CPU_CFLAGS"
	export CXX="${GXX_WRAPPER} $CPU_CFLAGS"
	export GNATMAKE=${TARGET}-gnatmake
	export GNATLINK=${TARGET}-gnatlink
	export GNATBIND=${TARGET}-gnatbind

	export LDFLAGS="$STACKSIZE"
	export CFLAGS="-O2 -fomit-frame-pointer"
	export CXXFLAGS="-O2 -fomit-frame-pointer"
	$srcdir/configure \
		--target="${TARGET}" --host="${TARGET}" --build="$BUILD" \
		--prefix="${TARGET_PREFIX}" \
		--libdir="${TARGET_LIBDIR}" \
		--bindir="${TARGET_BINDIR}" \
		--libexecdir='${libdir}' \
		--with-pkgversion="$REVISION" \
		--disable-libcc1 \
		--disable-werror \
		--with-gxx-include-dir=${TARGET_PREFIX}/include/c++/${gcc_dir_version} \
		$gcc4_compat \
		$zoneinfo \
		--with-gcc-major-version-only \
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
		$with_dw2_exceptions \
		--with-cpu=$with_cpu \
		--with-build-sysroot="${prefix}/${TARGET}/sys-root" \
		--enable-languages="$languages" || fail "gcc"
	
# there seems to be a problem with thin archives
	${MAKE} configure-gcc || exit 1
#	cd gcc || exit 1
#	sed -i 's/^S\["thin_archive_support"\]="\([^"]*\)"$/S\["thin_archive_support"\]="no"/' config.status
# c++ complains about an unknown option?
test -f gcc/config.status || exit 1
sed -i -e 's/-Wno-error=format-diag//' gcc/config.status
	./config.status
	
	cd "$MINT_BUILD_DIR" || exit 1

	${MAKE} $JOBS all-gcc || exit 1
	${MAKE} $JOBS all-target-libgcc || exit 1
	${MAKE} $JOBS || exit 1
	
	THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
	rm -rf "${THISPKG_DIR}"
	
	cd "$MINT_BUILD_DIR"

	rm -rf "${THISPKG_DIR}${TARGET_BINDIR}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin" "${THISPKG_DIR}${TARGET_LIBDIR}"
	rm -rf "${THISPKG_DIR}${gccsubdir}"

	${MAKE} DESTDIR="${THISPKG_DIR}" install >/dev/null || exit 1
	
	mkdir -p "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
	
	cd "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
	
	for i in c++ cpp g++ gcc gcov gfortran gdc gcc-ar gcc-nm gcc-ranlib; do
		cd "${THISPKG_DIR}${TARGET_BINDIR}"
		test -f "$i" || continue
		rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
		mv $i ${TARGET}-$i
		$LN_S ${TARGET}-$i $i
		cd "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
		rm -f ${i} ${i}${TARGET_EXEEXT}
		$LN_S ../../bin/$i${TARGET_EXEEXT} $i
	done
	
	for i in gnat gnatbind gnatchop gnatclean gnatkr gnatlink gnatls gnatmake gnatname gnatprep gnatxref; do
		cd "${THISPKG_DIR}${TARGET_BINDIR}"
		test -f "$i" || continue
		rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
		mv $i ${TARGET}-$i
		$LN_S ${TARGET}-$i $i
	done
	
	cd "${THISPKG_DIR}${TARGET_BINDIR}"
	${strip} *
	
	if test -x ${TARGET}-g++; then
		rm -f ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-g++-${BASE_VER}
		rm -f ${TARGET}-g++-${gcc_dir_version}${TARGET_EXEEXT} ${TARGET}-g++-${gcc_dir_version}
		mv ${TARGET}-g++${TARGET_EXEEXT} ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-g++${TARGET_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-g++-${gcc_dir_version}${TARGET_EXEEXT}
		rm -f g++-${BASE_VER}${TARGET_EXEEXT} g++-${BASE_VER}
		rm -f g++-${gcc_dir_version}${TARGET_EXEEXT} g++-${gcc_dir_version}${TARGET_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} g++-${BASE_VER}${TARGET_EXEEXT}
		$LN_S ${TARGET}-g++-${gcc_dir_version}${TARGET_EXEEXT} g++-${gcc_dir_version}${TARGET_EXEEXT}
	fi
	
	if test -x ${TARGET}-c++; then
		rm -f ${TARGET}-c++${TARGET_EXEEXT} ${TARGET}-c++
		$LN_S ${TARGET}-g++${TARGET_EXEEXT} ${TARGET}-c++${TARGET_EXEEXT}
	fi
	for tool in gcc gfortran gdc gccgo go gofmt gm2; do
		if test -x ${TARGET}-${tool}; then
			rm -f ${TARGET}-${tool}-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-${tool}-${BASE_VER}
			rm -f ${TARGET}-${tool}-${gcc_dir_version}${TARGET_EXEEXT} ${TARGET}-${tool}-${gcc_dir_version}
			mv ${TARGET}-${tool}${TARGET_EXEEXT} ${TARGET}-${tool}-${BASE_VER}${TARGET_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-${tool}${TARGET_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-${tool}-${gcc_dir_version}${TARGET_EXEEXT}
			rm -f ${tool}-${BASE_VER}${TARGET_EXEEXT} ${tool}-${BASE_VER}
			rm -f ${tool}-${gcc_dir_version}${TARGET_EXEEXT} ${tool}-${gcc_dir_version}${TARGET_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${TARGET_EXEEXT} ${tool}-${BASE_VER}${TARGET_EXEEXT}
			$LN_S ${TARGET}-${tool}-${gcc_dir_version}${TARGET_EXEEXT} ${tool}-${gcc_dir_version}${TARGET_EXEEXT}
		fi
	done
	if test -x ${TARGET}-cpp; then
		rm -f ${TARGET}-cpp-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-cpp-${BASE_VER}
		mv ${TARGET}-cpp${TARGET_EXEEXT} ${TARGET}-cpp-${BASE_VER}${TARGET_EXEEXT}
		$LN_S ${TARGET}-cpp-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-cpp
	fi
	
	cd "${THISPKG_DIR}"
	
# that directory only contains the gdb pretty printers;
# on the host we don't want them because they would conflict
# with the system ones
# the new mintelf target eventually supports gdb again
	if test ${TARGET} != m68k-atari-mintelf; then
		rm -rf ${TARGET_PREFIX#/}/share/gcc-${gcc_dir_version}
		if test -d ${TARGET_PREFIX#/}/${TARGET}/lib; then find ${TARGET_PREFIX#/}/${TARGET}/lib -name "libstdc++*.py" -delete; fi
		if test -d ${TARGET_PREFIX#/}/lib; then find ${TARGET_PREFIX#/}/lib -name "libstdc++*.py" -delete; fi
	fi

	rm -f ${TARGET_PREFIX#/}/share/info/dir
	for f in ${TARGET_PREFIX#/}/share/man/*/* ${TARGET_PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
	
	rm -f */*/libiberty.a
	find . -type f -name "*.la" -delete -printf "rm %p\n"

#
# move compiler dependant libraries to the gcc subdirectory
#
	cd ${THISPKG_DIR}${TARGET_PREFIX}/lib || exit 1
	libs=`find . -name "lib*.a" ! -path "*/gcc/*"`
	tar -c $libs | tar -x -C ${THISPKG_DIR}${gccsubdir}
	rm -f $libs
	for i in libgfortran.spec libgomp.spec libitm.spec libsanitizer.spec libmpx.spec libgphobos.spec; do
		test -f $i && mv $i ${THISPKG_DIR}${gccsubdir}
		find . -name "$i" -delete
	done
	find . -depth -type d -empty | xargs rmdir -v
	cd "${THISPKG_DIR}" || exit 1

	for f in ${gccsubdir#/}/{cc1,cc1plus,cc1obj,cc1objplus,f951,d21,collect2,lto-wrapper,lto1,gnat1,gnat1why,gnat1sciln,go1,brig1,cc1gm2,g++-mapper-server}${TARGET_EXEEXT} \
		${gccsubdir#/}/${LTO_PLUGIN} \
		${gccsubdir#/}/plugin/gengtype${TARGET_EXEEXT} \
		${gccsubdir#/}/install-tools/fixincl${TARGET_EXEEXT}; do
		test -f "$f" && ${strip} "$f"
	done

	find ${TARGET_PREFIX#/} -name "*.a" -exec "${strip}" -S -x '{}' \;
	find ${TARGET_PREFIX#/} -name "*.a" -exec "${ranlib}" '{}' \;

	cd ${TARGET_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/include-fixed && {
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
	
	cd "${THISPKG_DIR}" || exit 1
	
	#
	# create a separate archive for the fortran backend
	#
	if $with_fortran; then
		fortran=`find ${gccsubdir#/} -name finclude`
		fortran="$fortran "${gccsubdir#/}/f951
		fortran="$fortran "`find ${gccsubdir#/} -name libcaf_single.a`
		fortran="$fortran "`find ${gccsubdir#/} -name "*gfortran*"`
		fortran="$fortran "`find ${TARGET_PREFIX#/}/bin -name "*gfortran*"`
		${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-fortran-${CPU}.tar.xz $fortran || exit 1
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
		D="$D "${TARGET_PREFIX#/}/bin/*-gdc*
		${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-d-${CPU}.tar.xz $D || exit 1
		rm -rf $D
	fi

	#
	# create a separate archive for the ada backend
	#
	if $with_ada; then
		ada=`find ${gccsubdir#/} -name adainclude`
		ada="$ada "`find ${gccsubdir#/} -name adalib`
		ada="$ada "`find ${gccsubdir#/} -name "gnat1*"`
		ada="$ada "`find ${TARGET_PREFIX#/}/bin -name "*gnat*"`
		${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-ada-${CPU}.tar.xz $ada || exit 1
		rm -rf $ada
	fi

	#
	# create a separate archive for the modula-2 backend
	#
	if $with_m2; then
		m2=`find ${gccsubdir#/} -type d -name m2`
		m2="$m2 "`find ${gccsubdir#/} -name "libm2*"`
		m2="$m2 "`find ${gccsubdir#/} -name "cc1gm2*"`
		m2="$m2 "${TARGET_PREFIX#/}/bin/${TARGET}-gm2*
		${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-m2-${CPU}.tar.xz $m2 || exit 1
		rm -rf $m2
	fi

	#
	# create archive for all others
	#
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-${CPU}.tar.xz *
done # for CPU

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint.tar.xz ${PATCHES}

cp -p "$me" ${DIST_DIR}/cross-${PACKAGENAME}${VERSION}${VERSIONPATCH}-build.sh
