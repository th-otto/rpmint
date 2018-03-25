#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=python3
VERSION=-3.6.4
VERSIONPATCH=

srcarchive=Python${VERSION}

. ${scriptdir}/functions.sh

python_version=$(echo ${VERSION#-} | head -c 3)


PATCHES="
patches/python3/Python-3.0b1-record-rpm.patch
patches/python3/python-3.6.0-multilib-new.patch
patches/python3/python-3.3.0b1-localpath.patch
patches/python3/python-3.3.0b1-fix_date_time_compiler.patch
patches/python3/python-3.3.0b1-curses-panel.patch
patches/python3/python-3.3.0b1-test-posix_fadvise.patch
patches/python3/python-3.3.3-skip-distutils-test_sysconfig_module.patch
patches/python3/subprocess-raise-timeout.patch
patches/python3/0001-allow-for-reproducible-builds-of-python-packages.patch
patches/python3/distutils-reproducible-compile.patch
patches/python3/skip_random_failing_tests.patch
patches/python3/fix-localeconv-encoding-for-LC_NUMERIC.patch
patches/python3/python3-sorted_tar.patch
patches/python3/ctypes-pass-by-value.patch
patches/python3/mintelf-config.patch
patches/python3/mint.patch
patches/python3/python-mintnosharedmod.patch
patches/python3/python-mintsetupdist.patch
patches/python3/cross-config.patch
"
DISABLED_PATCHES="
"
POST_INSTALL_SCRIPTS="
patches/python3/macros.python3
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/python${python_version}
${TARGET_MANDIR#/}/*
${TARGET_SYSCONFDIR#/}/*
"

srcdir="$here/Python${VERSION}"
MINT_BUILD_DIR="$srcdir"

unpack_archive

cd "$MINT_BUILD_DIR"

# drop Autoconf version requirement
sed -i 's/^AC_PREREQ/dnl AC_PREREQ/' configure.ac

autoreconf -f -i
# autoreconf may have overwritten config.sub
# patch -p1 < "$BUILD_DIR/patches/python3/mintelf-config.patch"
# prevent make from trying to rebuild asdl stuff, which requires existing
# python installation
touch Parser/asdl* Python/Python-ast.c Include/Python-ast.h

COMMON_CFLAGS="\
	-O2 -fomit-frame-pointer -fwrapv \
	-DOPENSSL_LOAD_CONF"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS=" \
	--host=${TARGET} \
	--build=`./config.guess` \
	--prefix=${TARGET_PREFIX} \
	--docdir=${TARGET_PREFIX}/share/doc/packages/python \
    --disable-ipv6 \
    --with-fpectl \
    --disable-shared --enable-static \
    --enable-unicode=ucs4 \
    --with-system-expat \
    --without-ensurepip \
	--config-cache"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

CPU_ARCHNAME_000=-000
CPU_ARCHNAME_020=-020
CPU_ARCHNAME_v4e=-v4e


for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

cat << EOF > config.cache
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
EOF

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	eval archname=\${CPU_ARCHNAME_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE" \
	AR="$ar" \
	RANLIB="$ranlib" \
	STRIP="$strip" \
	sh ./configure \
		${CONFIGURE_FLAGS} \
		|| exit 1
	hack_lto_cflags

	${MAKE} ${JOBS} || exit 1
	
	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" TARGET=${TARGET} SYSROOT=${sysroot} install

	# RPM macros
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/rpm
	install -m 644 ${BUILD_DIR}/patches/${PACKAGENAME}/macros.python3 ${buildroot}${TARGET_SYSCONFDIR}/rpm

	# scripts
	install -m 755 Tools/scripts/pydoc3 ${buildroot}${prefix}/bin/pydoc3-${python_version}
	install -m 755 Tools/scripts/2to3 ${buildroot}${prefix}/bin/2to3-${python_version}
	install -m 755 Tools/scripts/pyvenv ${buildroot}${prefix}/bin/pyvenv-${python_version}
	
	${MAKE} clean >/dev/null

	cd ${buildroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	

	if test "$multilibdir" != ""; then
		mkdir -p ${buildroot}${TARGET_LIBDIR}$multilibdir
		mv ${buildroot}${TARGET_LIBDIR}/*.a ${buildroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	# remove the hard links and/or symlinks,
	# keeping python2.7 the default
	for dir in bin include lib ; do
	    rm -f ${buildroot}/${prefix}/$dir/python
	done
	rm -f ${buildroot}/${prefix}/lib/pkgconfig/python.pc
	
	# remove wrapper scripts for packages not built
	rm -f ${buildroot}/${prefix}/bin/idle*

	# the directory for modules must exist; getpath.c depends on it
	mkdir -p ${buildroot}${TARGET_LIBDIR}/python${python_version}/lib-dynload
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
