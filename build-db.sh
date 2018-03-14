#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=db
VERSION=-4.8.30
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/db/db${VERSION}.patch
patches/db/mintelf-config.patch
patches/db/rpm-no-fsync.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/doc/*
"

MINT_BUILD_DIR="$srcdir/build_unix"

unpack_archive

cd "$MINT_BUILD_DIR/../dist"
./s_config
cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -fno-strict-aliasing $LTO_CFLAGS"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	 --enable-compat185 --disable-dump185 --disable-mutexsupport"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/dist/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	hack_lto_cflags

	${MAKE} $JOBS || exit 1
	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install || exit 1

	# Fix header file installation
	if ! test -d ${buildroot}${TARGET_PREFIX}/include/db4; then
		mkdir -p ${buildroot}${TARGET_PREFIX}/include/db4
		mv ${buildroot}${TARGET_PREFIX}/include/*.h ${buildroot}${TARGET_PREFIX}/include/db4
	fi
	rm -f ${buildroot}${TARGET_PREFIX}/include/{db,db_185,db_cxx}.h
	echo "#include <db4/db.h>" > ${buildroot}${TARGET_PREFIX}/include/db.h
	echo "#include <db4/db_185.h>" > ${buildroot}${TARGET_PREFIX}/include/db_185.h
	echo "#include <db4/db_cxx.h>" > ${buildroot}${TARGET_PREFIX}/include/db_cxx.h
	
	# remove dangling tags symlink from examples.
	cd ..
	rm -f examples_cxx/tags
	rm -f examples_c/tags
	# Move documentation to the right directory
	mkdir -p ${buildroot}${TARGET_PREFIX}/share/doc/${PACKAGENAME}
	mv -f ${buildroot}${TARGET_PREFIX}/docs/* ${buildroot}/${TARGET_PREFIX}/share/doc/${PACKAGENAME}
	cp -a examples_cxx examples_c ${buildroot}/${TARGET_PREFIX}/share/doc/${PACKAGENAME}
	cp -a LICENSE README ${buildroot}/${TARGET_PREFIX}/share/doc/${PACKAGENAME}

	cd "$MINT_BUILD_DIR"
	${MAKE} distclean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
