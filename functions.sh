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
	Darwin*) host=macos; TAR_OPTS= ;;
	*) host=linux ;;
esac
case `uname -s` in
	MINGW*) prefix=${MINGW_PREFIX} ;;
	Darwin*) prefix=/opt/cross-mint ;;
	*) prefix=/usr ;;
esac
sysroot=${prefix}/${TARGET}/sys-root

#
# prefix of the target system. Should not need to be changed.
#
TARGET_PREFIX=/usr
TARGET_LIBDIR="${TARGET_PREFIX}/lib"
TARGET_BINDIR="${TARGET_PREFIX}/bin"
TARGET_MANDIR="${TARGET_PREFIX}/share/man"
TARGET_INFODIR="${TARGET_PREFIX}/share/info"

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
BINTARNAME=${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}
THISPKG_DIR="${DIST_DIR}/${PACKAGENAME}${VERSION}"

#
# this could eventually be extracted from gcc -print-multi-lib
#
CPU_CFLAGS_000=-m68000    ; CPU_LIBDIR_000=
CPU_CFLAGS_020=-m68020-60 ; CPU_LIBDIR_020=/m68020-60
CPU_CFLAGS_v4e=-mcpu=5475 ; CPU_LIBDIR_v4e=/m5475

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

LTO_CFLAGS=
ranlib=ranlib
case "${TARGET}" in
    *-*-*elf* | *-*-linux*)
    	ranlib=gcc-ranlib
		# we cannot add this to CFLAGS, because then autoconf tests
		# for missing c library functions will always succeed
		LTO_CFLAGS="-flto -ffat-lto-objects"
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
		test -z "$srcarchive" && srcarchive=${PACKAGENAME}${VERSION}
		for f in "$ARCHIVES_DIR/${srcarchive}.tar.xz" \
		         "$ARCHIVES_DIR/${srcarchive}.tar.bz2" \
		         "$ARCHIVES_DIR/${srcarchive}.tar.gz" \
		         "$ARCHIVES_DIR/${srcarchive}.tgz" \
		         "${here}${srcarchive}.tar.xz" \
		         "${here}${srcarchive}.tar.bz2" \
		         "${here}${srcarchive}.tar.gz" \
		         "${here}${srcarchive}.tgz"; do
			if test -f "$f"; then missing=false; tar xvf "$f" || exit 1; fi
		done
		if $missing; then
			echo "${srcarchive}.*: no such file" >&2
			exit 1
		fi
		if test ! -d "$srcdir"; then
			echo "$srcdir: no such directory" >&2
			exit 1
		fi
		if test -n "${PATCHARCHIVE}"; then
			mkdir -p "$BUILD_DIR/${PACKAGENAME}-patches"
			${TAR} -C "$BUILD_DIR/${PACKAGENAME}-patches" --strip-components=1 -xjf "${PATCHARCHIVE}"
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
		    cd "$srcdir" || exit 1
		    flags=
		    if patch -N -s --dry-run -p1 -i "$BUILD_DIR/$f" > /dev/null 2>&1; then
		    	flags="-N -p1"
			    patch $flags -i "$BUILD_DIR/$f" || exit 1
		    else
		    	echo "patch $f does not apply" >&2
		    	exit 1
			fi
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


hack_lto_cflags()
{
	if test "$LTO_CFLAGS" != ""; then
        sed -i 's/^S\["CFLAGS"\]="\([^"]*\)"$/S\["CFLAGS"\]="'"$LTO_CFLAGS"' \1"/
s/^S\["CXXFLAGS"\]="\([^"]*\)"$/S\["CXXFLAGS"\]="'"$LTO_CFLAGS"' \1"/
s/^S\["BUILD_CFLAGS"\]="\([^"]*\)"$/S\["BUILD_CFLAGS"\]="'"$LTO_CFLAGS"' \1"/
s/^s,@CFLAGS@,\(.*\)$/s,@CFLAGS@,'"$LTO_CFLAGS"' \1/
s/^s,@CXXFLAGS@,\(.*\)$/s,@CXXFLAGS@,'"$LTO_CFLAGS"' \1/' config.status
		./config.status
	fi
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


gzip_docs()
{
	cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" || exit 1
	rm -f share/info/dir
	if test -d share/man; then
		for f in share/man/*/*; do
			case $f in
			*.gz) ;;
			*)
				if test -h $f; then
					t=$(readlink $f)
					case $t in
					*.gz) ;;
					*)
						rm -f $f $f.gz
						$LN_S $t.gz $f.gz
						;;
					esac
				else
					rm -f ${f}.gz; gzip -9 $f
				fi
				;;
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
}


make_bin_archive()
{
	archsuffix=${1-000}

	gzip_docs

	cd "${THISPKG_DIR}${sysroot}" || exit 1
	files=""
	for i in ${BINFILES}; do
		i=${i#/}
		if test -d "$i" -o -f "$i" -o -h "$i"; then
			files="$files $i"
			case $i in 
			*/bin/* | */sbin/* | bin/* | sbin/*)
				if test ! -d "$i" -a ! -h "$i"; then
					"${strip}" "$i"
				fi
				;;
			esac
		else
			echo "$i does not exist for packaging" >&2
			exit 1
		fi
	done

	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}-${archsuffix}.tar.xz $files

	cd "$MINT_BUILD_DIR" || exit 1
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
	gzip_docs

	cd "${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" || exit 1
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

	${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-dev.tar.xz *

	if test -n "${BINFILES}"; then
		cd "${THISPKG_DIR}${sysroot}" || exit 1
		files=""
		for i in ${BINFILES}; do
			i=${i#/}
			if test -d "$i" -o -f "$i" -o -h "$i"; then
				files="$files $i"
			else
				echo "$i does not exist for packaging" >&2
				exit 1
			fi
		done
		
		rm -rf $files
		cd "${THISPKG_DIR}" || exit 1
		files=`find . -type f`
		if test "$files" = ""; then
			echo "no dev files, removing ${TARNAME}-dev.tar.xz"
			rm -f ${DIST_DIR}/${TARNAME}-dev.tar.xz
		fi
	fi
	
	cd "${BUILD_DIR}" || exit 1
	if test "$KEEP_PKGDIR" != yes; then
		rm -rf "${THISPKG_DIR}"
	fi
	if test "$KEEP_SRCDIR" != yes; then
		rm -rf "${srcdir}"
	fi

	test -z "${PATCHES}" || ${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}.tar.xz ${PATCHES} ${PATCHARCHIVE}
	cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
	cp -p "${scriptdir}/functions.sh" "${DIST_DIR}"
}
