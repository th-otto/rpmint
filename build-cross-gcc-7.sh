#!/bin/sh

#
# This script is for using the cross-compiler to
# build the native compiler for the target(s)
#

me="$0"

PACKAGENAME=gcc
VERSION=-7.4.0
VERSIONPATCH=-20190225
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
prefix=/usr
TARGET_PREFIX=/usr
TARGET_LIBDIR=${TARGET_PREFIX}/lib
TARGET_BINDIR=${TARGET_PREFIX}/bin

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
# this patch can be recreated by
# - cloning https://github.com/th-otto/m68k-atari-mint-gcc.git
# - checking out the gcc-7-mint branch
# - running git diff gcc-7_3_0-release HEAD
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
if test ! -f "${prefix}/${TARGET}/sys-root/usr/include/compiler.h"; then
	echo "mintlib must be installed in ${prefix}/${TARGET}/sys-root/usr/include" >&2
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
gcc_dir_version=$(echo $BASE_VER | cut -d '.' -f 1)

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

rm -rf "$MINT_BUILD_DIR"
mkdir -p "$MINT_BUILD_DIR"

cd "$MINT_BUILD_DIR"

enable_lto=--disable-lto
enable_plugin=--disable-plugin
languages=c,c++,fortran
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

mpfr_config=

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}

#
# this could eventually be extracted from gcc -print-multi-lib
#
CPU_CFLAGS_000="-m68000"    ; CPU_LIBDIR_000=/m68000    ; WITH_CPU_000=m68000
CPU_CFLAGS_020="-m68020-60" ; CPU_LIBDIR_020=/m68020-60 ; WITH_CPU_020=m68020-60
CPU_CFLAGS_v4e="-mcpu=5475" ; CPU_LIBDIR_v4e=/m5475     ; WITH_CPU_v4e=5475
#
# This should list the default target cpu last,
# so that any files left behind are compiled for this
#
ALL_CPUS="020 v4e 000"

export AS_FOR_TARGET="$as"
export RANLIB_FOR_TARGET="$ranlib"
export STRIP_FOR_TARGET="$strip"
export CC_FOR_TARGET="${TARGET}-gcc"
export CXX_FOR_TARGET="${TARGET}-g++"

for CPU in ${ALL_CPUS}; do
	cd "$here" || exit 1
	rm -rf "$MINT_BUILD_DIR"
	mkdir -p "$MINT_BUILD_DIR"
	
	cd "$MINT_BUILD_DIR" || exit 1
	
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval with_cpu=\${WITH_CPU_$CPU}
	STACKSIZE="-Wl,-stack,512k"

cat <<'EOF' > "$MINT_BUILD_DIR/gcc-wrapper.sh"
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

cp "$MINT_BUILD_DIR/gcc-wrapper.sh" "$MINT_BUILD_DIR/gxx-wrapper.sh"
cat <<EOF >> "$MINT_BUILD_DIR/gcc-wrapper.sh"
eval exec "${TARGET}-gcc" \$cpu_flags \$args
EOF
cat <<EOF >> "$MINT_BUILD_DIR/gxx-wrapper.sh"
eval exec "${TARGET}-g++" \$cpu_flags \$args
EOF

chmod 755 "$MINT_BUILD_DIR/gcc-wrapper.sh"
chmod 755 "$MINT_BUILD_DIR/gxx-wrapper.sh"

	export CC="${MINT_BUILD_DIR}/gcc-wrapper.sh $CPU_CFLAGS"
	export CXX="${MINT_BUILD_DIR}/gxx-wrapper.sh $CPU_CFLAGS"

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
		--disable-libvtv \
		--disable-libmpx \
		--disable-libcc1 \
		--disable-werror \
		--with-gxx-include-dir=${TARGET_PREFIX}/include/c++/${gcc_dir_version} \
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
		$mpfr_config \
		--with-cpu=$with_cpu \
		--with-sysroot="${prefix}/${TARGET}/sys-root" \
		--enable-languages="$languages"
	
# there seems to be a problem with thin archives
	${MAKE} configure-gcc || exit 1
#	cd gcc || exit 1
#	sed -i 's/^S\["thin_archive_support"\]="\([^"]*\)"$/S\["thin_archive_support"\]="no"/' config.status
#	./config.status
	
	cd "$MINT_BUILD_DIR" || exit 1

	${MAKE} $JOBS all-gcc || exit 1
	${MAKE} $JOBS all-target-libgcc || exit 1
	${MAKE} $JOBS || exit 1
	
	THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"
	rm -rf "${THISPKG_DIR}"
	
	cd "$MINT_BUILD_DIR"

	rm -rf "${THISPKG_DIR}${TARGET_BINDIR}" "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin" "${THISPKG_DIR}${TARGET_LIBDIR}"

	${MAKE} DESTDIR="${THISPKG_DIR}" install >/dev/null || exit 1
	
	mkdir -p "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
	
	cd "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
	
	for i in c++ cpp g++ gcc gcov gfortran gcc-ar gcc-nm gcc-ranlib; do
		cd "${THISPKG_DIR}${TARGET_BINDIR}"
		test -f "$i" || continue
		rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
		mv $i ${TARGET}-$i
		$LN_S ${TARGET}-$i $i
		cd "${THISPKG_DIR}${TARGET_PREFIX}/${TARGET}/bin"
		rm -f ${i} ${i}${TARGET_EXEEXT}
		$LN_S ../../bin/$i${TARGET_EXEEXT} $i
	done
	
	cd "${THISPKG_DIR}${TARGET_BINDIR}"
	${strip} *
	
	if test -x ${TARGET}-g++; then
		rm -f ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-g++-${BASE_VER}
		$LN_S ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-g++
		rm -f g++-${BASE_VER}${TARGET_EXEEXT} g++-${BASE_VER}
		$LN_S ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-g++
	fi
	
	if test -x ${TARGET}-c++; then
		rm -f ${TARGET}-c++${TARGET_EXEEXT} ${TARGET}-c++
		$LN_S ${TARGET}-g++ ${TARGET}-c++
	fi
	if test ${BASE_VER} != ${gcc_dir_version} && test -x ${TARGET}-gcc-${gcc_dir_version}; then
		rm -f ${TARGET}-gcc-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-gcc-${BASE_VER}
		mv ${TARGET}-gcc-${gcc_dir_version} ${TARGET}-gcc-${BASE_VER}${TARGET_EXEEXT}
		$LN_S ${TARGET}-gcc-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-gcc-${gcc_dir_version}
		rm -f gcc-${BASE_VER}${TARGET_EXEEXT} gcc-${BASE_VER}
		$LN_S gcc-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-gcc-${gcc_dir_version}
	fi
	if test -x ${TARGET}-cpp; then
		rm -f ${TARGET}-cpp-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-cpp-${BASE_VER}
		mv ${TARGET}-cpp${TARGET_EXEEXT} ${TARGET}-cpp-${BASE_VER}${TARGET_EXEEXT}
		$LN_S ${TARGET}-cpp-${BASE_VER}${TARGET_EXEEXT} ${TARGET}-cpp
	fi
	
	cd "${THISPKG_DIR}"
	
	rm -f ${TARGET_PREFIX#/}/share/info/dir
	for f in ${TARGET_PREFIX#/}/share/man/*/* ${TARGET_PREFIX#/}/share/info/*; do
		case $f in
		*.gz) ;;
		*) rm -f ${f}.gz; gzip -9 $f ;;
		esac
	done
	
	rm -f */*/libiberty.a
	find . -type f -name "*.la" -delete -printf "rm %p\n"
	${strip} ${TARGET_LIBDIR#/}/gcc/${TARGET}/*/{cc1,cc1plus,cc1obj,cc1objplus,f951,collect2,lto-wrapper,lto1}${TARGET_EXEEXT}
	${strip} ${TARGET_LIBDIR#/}/gcc/${TARGET}/*/${LTO_PLUGIN}
	${strip} ${TARGET_LIBDIR#/}/gcc/${TARGET}/*/plugin/gengtype${TARGET_EXEEXT}
	${strip} ${TARGET_LIBDIR#/}/gcc/${TARGET}/*/install-tools/fixincl${TARGET_EXEEXT}
	
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
	
	# these are currently identically compiled 2 times; FIXME
	if test "$CPU_LIBDIR_000" != ""; then
		for dir in . mshort mfastcall mfastcall/mshort; do
			for f in libgcov.a libgcc.a libcaf_single.a; do
				rm -f ${TARGET_LIBDIR#/}/gcc/${TARGET}/$dir/$f
			done
		done
		for dir in mfastcall/mshort mfastcall mshort; do
			rmdir ${TARGET_LIBDIR#/}/gcc/${TARGET}/$dir 2>/dev/null
		done
	fi
	
	cd "${THISPKG_DIR}" || exit 1
	
	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-${CPU}.tar.xz *
done # for CPU

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint.tar.xz ${PATCHES}

cp -p "$me" ${DIST_DIR}/build-cross-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
