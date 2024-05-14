
#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mpg123
VERSION=-1.25.10
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/mpg123-math.patch
patches/${PACKAGENAME}/mpg123-amigaos.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$srcdir"

rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" build/config.sub

COMMON_CFLAGS="-O2 -fomit-frame-pointer -DNO_CATCHSIGNAL ${CFLAGS_AMIGAOS} ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"
LDFLAGS="${STACKSIZE}"

WITH_FASTCALL=`if $gcc -mfastcall -E - < /dev/null >/dev/null 2>&1; then echo true; else echo false; fi`

case "$TARGET" in
*-amigaos*)
	# does not work yet because of link problems with socket library
	CONFIGURE_FLAGS+=" --disable-network"
	;;
esac

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	if $WITH_FASTCALL; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall" \
		LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -mfastcall $LDFLAGS" \
		./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir/mfastcall
		${MAKE} $JOBS || exit 1

		${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
		
		${MAKE} distclean >/dev/null
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LDFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	${MAKE} $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	${MAKE} distclean >/dev/null

	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
