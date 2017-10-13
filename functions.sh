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
case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) host=msys ;;
	CYGWIN*) if echo "" | gcc -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	*) host=linux ;;
esac
case `uname -s` in
	MINGW*) prefix=${MINGW_PREFIX} ;;
	*) prefix=/usr ;;
esac
sysroot=${prefix}/${TARGET}/sys-root

#
# prefix of the target system. Should not need to be changed.
#
TARGET_PREFIX=/usr
TARGET_LIBDIR="${TARGET_PREFIX}/lib"
TARGET_BINDIR="${TARGET_PREFIX}/bin"

#
# Where to look for the original source archives
#
case `uname -s` in
	MINGW* | MSYS*) here=`pwd` ;;
	*) here=`pwd` ;;
esac
ARCHIVES_DIR=$HOME/packages

#
# Where to look up the source tree, after unpacking
#
test -z "${PACKAGENAME}" && { echo "PACKAGENAME not set" >&2; exit 1; }
test -z "${VERSION}" && { echo "VERSION not set" >&2; exit 1; }
srcdir="$here/${PACKAGENAME}${VERSION}"

#
# Where to look for patches, write logs etc.
#
BUILD_DIR="$here"

#
# Where to configure and build the package
#
MINT_BUILD_DIR="$srcdir"

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


BUILD_EXEEXT=
TARGET_EXEEXT=
LN_S="ln -s"
case `uname -s` in
	CYGWIN* | MINGW* | MSYS*) BUILD_EXEEXT=.exe ;;
esac
case `uname -s` in
	MINGW* | MSYS*) LN_S="cp -p" ;;
esac
case $TARGET in
 	*-*-cygwin* | *-*-mingw* | *-*-msys*) TARGET_EXEEXT=.exe ;;
esac

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

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}${VERSIONPATCH}
THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
BUILD=`/usr/share/automake/config.guess 2>/dev/null`
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`

LTO_CFLAGS=
ranlib=ranlib
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
    	ranlib=gcc-ranlib
		# we cannot add this to CFLAGS, because then autoconf tests
		# for missing c library functions will always succeed
		LTO_CFLAGS="-flto"
		;;
esac

ranlib=`which ${TARGET}-${ranlib} 2>/dev/null`
strip=`which "${TARGET}-strip"`
gcc=`which "${TARGET}-gcc"`
cxx=`which "${TARGET}-g++"`
MAKE=make

if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$gcc" -o ! -x "$strip"; then
	echo "cross tools for ${TARGET} not found" >&2
	exit 1
fi

unpack_archive()
{
	rm -rf "$srcdir"
	if :; then
		missing=true
		for f in "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.xz" \
		         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.bz2" \
		         "$ARCHIVES_DIR/${PACKAGENAME}${VERSION}.tar.gz" \
		         "${here}${PACKAGENAME}${VERSION}.tar.xz" \
		         "${here}${PACKAGENAME}${VERSION}.tar.bz2" \
		         "${here}${PACKAGENAME}${VERSION}.tar.gz"; do
			if test -f "$f"; then missing=false; tar xvf "$f" || exit 1; fi
		done
		if $missing; then
			echo "${PACKAGENAME}${VERSION}.*: no such file" >&2
			exit 1
		fi
		if test ! -d "$srcdir"; then
			echo "$srcdir: no such directory" >&2
			exit 1
		fi
		if test -n "${PATCHARCHIVE}"; then
			mkdir -p "$BUILD_DIR/${PACKAGENAME}-patches"
			tar -C "$BUILD_DIR/${PACKAGENAME}-patches" --strip-components=1 -xjf "${PATCHARCHIVE}"
			cd "$srcdir"
			for patch in $BUILD_DIR/${PACKAGENAME}-patches/${PACKAGENAME}*.patch
			do
			    patch -f -T -p1 -s < $patch
			done
			cd "$BUILD_DIR"
			rm -rf "$BUILD_DIR/${PACKAGENAME}-patches"
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
	fi

	if test ! -d "$srcdir"; then
		echo "$srcdir: no such directory" >&2
		exit 1
	fi

	rm -rf "${THISPKG_DIR}"
}


# FIXME: libtool kills it
hack_lto_cflags()
{
        sed -i 's/^S\["CFLAGS"\]="\([^"]*\)"$/S\["CFLAGS"\]="'"$LTO_CFLAGS"' \1"/
s/^S\["CXXFLAGS"\]="\([^"]*\)"$/S\["CXXFLAGS"\]="'"$LTO_CFLAGS"' \1"/' config.status
			./config.status
}


move_prefix()
{
	cd "${THISPKG_DIR}"
	if test "${prefix}" != "${TARGET_PREFIX}"; then
		cd "${THISPKG_DIR}${sysroot}" || exit 1
		test ! -d "${TARGET_PREFIX}" || exit 1
		mv "${prefix}" "${TARGET_PREFIX}" || exit 1
	fi
}


move_arch_bins()
{
	archdir=$1
	if test -d "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/bin"; then
		cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/bin"
		mkdir -p ${archdir}
		for i in *; do
			test -h "$i" && continue
			test -d "$i" && continue
			"${strip}" "$i"
			mv "$i" "${archdir}/$i" || exit 1
		done
	fi
	cd "$MINT_BUILD_DIR"
}

move_v4e_bins()
{
	move_arch_bins m5475
}

move_020_bins()
{
	move_arch_bins m68020-60
}


copy_pkg_configs()
{
	local pattern="${1:-*.pc}"
	local build_prefix="$prefix/$TARGET"
	local i base dst
	
	cd "${THISPKG_DIR}"
	mkdir -p ./$build_prefix/lib/pkgconfig
	
	#
	# replace absolute pathnames by their symbolic equivalents
	# and remove unneeded -I and -L switches,
	# since those directories are always on the
	# default search path.
	# remove -L${sharedlibdir}, because
	# sharedlibdir is the bin directory, but the import libraries
	# are in the lib directory
	#
	for i in .${sysroot}$TARGET_LIBDIR/pkgconfig/$pattern; do
		test -e "$i" || continue
		true && {
			# from the *.pc files generated for the target,
			# generate *.pc files that are suitable for the cross-compiler
			base=${i##*/}
			dst=./$build_prefix/lib/pkgconfig/$base
			if test ! -f $dst -o $i -nt $dst; then
				cp -a $i $dst
				test -h "$i" && continue
				sed -i 's,",,g
						 s,prefix[ ]*=[ ]*'${configured_prefix}',prefix='${sysroot}${TARGET_PREFIX}',
			             /^prefix[ ]*=/{p;d}
			             s,=[ ]*'$prefix',=${prefix},
			             s,-L'$TARGET_LIBDIR',-L${libdir},g
			             s,-L${sharedlibdir} ,,g
			             s,-L${libdir} ,,g
			             s,-L${libdir}$,,
			             s,-L'${TARGET_BINDIR}'[ ]*,,g
			             s,-I/usr/include,-I${includedir},g
			             s,-I'${sysroot}${TARGET_PREFIX}/include',-I${includedir},g
			             s,-I${includedir} ,,g
			             s,-I${includedir}$,,' $dst
			fi
		}
		true && {
			sed -e 's,",,g
					 s,prefix[ ]*=[ ]*'${configured_prefix}',prefix='${TARGET_PREFIX}',
			         /^prefix[ ]*=/{p;d}
			         s,[ ]*=[ ]*'$prefix',=${prefix},
			         s,-L'$TARGET_LIBDIR',-L${libdir},g
		             s,-L${sharedlibdir} ,,g
			         s,-L${libdir} ,,g
			         s,-L${libdir}$,,
		             s,-L'${TARGET_BINDIR}'[ ]*,,g
 		             s,-I/usr/include,-I${includedir},g
		             s,-I'${sysroot}${TARGET_PREFIX}/include',-I${includedir},g
				     s,-I${includedir} ,,g
				     s,-I${includedir}$,,' $i > $i.tmp
			diff -q $i $i.tmp >/dev/null && rm -f $i.tmp || {
				echo "fixed $i"
				mv $i.tmp $i
			}
		}
	done
}


make_archives()
{
	cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" || exit 1
	rm -f share/info/dir
	if test -d share/man; then
		for f in share/man/*/*; do
			case $f in
			*.gz) ;;
			*) rm -f ${f}.gz; gzip -9 $f ;;
			esac
		done
	fi
	if test -d share/info; then
		for f in share/info/*; do
			case $f in
			*.gz) ;;
			*) rm -f ${f}.gz; gzip -9 $f ;;
			esac
		done
	fi

	find . -name "*.la" -exec rm '{}' \;
	test "$LTO_CFLAGS" != "" || find . -name "*.a" ! -type l -exec "${strip}" -S -x '{}' \;
	find . -name "*.a" ! -type l -exec "${ranlib}" '{}' \;
	
	if test -d "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/bin"; then
		cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/bin"
		for i in *; do
			test -h "$i" && continue
			test -d "$i" && continue
			"${strip}" "$i"
		done
	fi
	
	#
	# remove pkgconfig dirs in architecture dependent subdirs
	# we only need the one in the toplevel directory
	#
	rm -rf ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/lib/*/pkgconfig
	
	cd "${THISPKG_DIR}" || exit 1
	
	tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin.tar.xz *
	
	cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
	rm -rf "${srcdir}"

	test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.tar.xz ${PATCHES} ${PATCHARCHIVE}
	cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
	cp -p "${scriptdir}/functions.sh" "${DIST_DIR}"
}
