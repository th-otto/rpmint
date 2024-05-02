#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=python3
VERSION=-3.11.8
VERSIONPATCH=

srcarchive=Python${VERSION}

. ${scriptdir}/functions.sh

python_version=3.11

PATCHES="
patches/python3/python3-F00251-change-user-install-location.patch
patches/python3/python3-distutils-reproducible-compile.patch
patches/python3/python3-3.3.0b1-localpath.patch
patches/python3/python3-3.3.0b1-fix_date_time_compiler.patch
patches/python3/python3-3.3.0b1-test-posix_fadvise.patch
patches/python3/python3-subprocess-raise-timeout.patch
patches/python3/python3-bpo-31046_ensurepip_honours_prefix.patch
patches/python3/python3-no-skipif-doctests.patch
patches/python3/python3-skip-test_pyobject_freed_is_freed.patch
patches/python3/python3-fix_configure_rst.patch
patches/python3/python3-support-expat-CVE-2022-25236-patched.patch
patches/python3/python3-skip_if_buildbot-extend.patch
patches/python3/python3-CVE-2023-27043-email-parsing-errors.patch
patches/python3/python3-libexpat260.patch
patches/python3/python3-CVE-2023-6597-TempDir-cleaning-symlink.patch
patches/python3/python3-bsc1221260-test_asyncio-ResourceWarning.patch
patches/python3/python3-bluez-devel.patch
patches/python3/python3-Fix-shebangs.patch
patches/python3/python3-cross-config.patch
patches/python3/python3-mintnosharedmod.patch
patches/python3/python3-mintsetupdist.patch
patches/python3/python3-mint.patch
"
DISABLED_PATCHES="
patches/python3/python3-3.0b1-record-rpm.patch
patches/python3/python3-3.7.17-multilib-new.patch
patches/python3/python3-3.3.0b1-curses-panel.patch
patches/python3/python3-3.3.3-skip-distutils-test_sysconfig_module.patch
patches/python3/python3-distutils-reproducible-compile.patch
patches/python3/python3-skip_random_failing_tests.patch
patches/python3/python3-0001-allow-for-reproducible-builds-of-python-packages.patch
patches/python3/python3-fix-localeconv-encoding-for-LC_NUMERIC.patch
patches/python3/python3-sorted_tar.patch
patches/python3/python3-ctypes-pass-by-value.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"
POST_INSTALL_SCRIPTS="
patches/python3/python3-macros.python3
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

autoreconf -fiv
# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

# prevent make from trying to rebuild asdl stuff, which requires existing
# python installation
touch Parser/asdl* Python/Python-ast.c Include/Python-ast.h

# drop in-tree libffi and expat
rm -rf Modules/_ctypes/libffi* Modules/_ctypes/darwin
# Cannot remove it because of gh#python/cpython#92875
# rm -rf Modules/expat

# drop duplicate README from site-packages
rm -f Lib/site-packages/README.txt

# Don't fail on warnings when building documentation
sed -i -e '/^SPHINXERRORHANDLING/s/-W//' Doc/Makefile

COMMON_CFLAGS="\
	-O2 -fomit-frame-pointer -fwrapv \
	-DOPENSSL_LOAD_CONF \
	 -IVendor/ \
	${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${TARGET_PREFIX}
	--build=`./config.guess`
	--with-platlibdir=lib
	--docdir=${TARGET_PREFIX}/share/doc/packages/python
	--disable-ipv6
	--disable-shared --enable-static
	--enable-unicode=ucs4
	--with-system-expat
	--without-thread
	--without-ensurepip
	--with-build-python=python3
	--config-cache
"

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
ac_cv_lib_intl_textdomain=yes
ac_cv_func_pthread_condattr_setclock=no
ac_cv_have_pthread_t=no
ac_cv_func_pthread_kill=no
ac_cv_func_pthread_sigmask=no
ac_cv_header_pthread_h=no
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
	PYTHON_FOR_BUILD=python3 \
	LIBS=-liconv \
	sh ./configure \
		${CONFIGURE_FLAGS} \
		|| exit 1
	: hack_lto_cflags

	${MAKE} ${JOBS} || exit 1
	
	buildroot="${THISPKG_DIR}${sysroot}"

	${MAKE} DESTDIR="${buildroot}" TARGET=${TARGET} SYSROOT=${sysroot} install || exit 1

	# RPM macros
	mkdir -p ${buildroot}${TARGET_SYSCONFDIR}/rpm
	install -m 644 ${BUILD_DIR}/patches/${PACKAGENAME}/python3-macros.python3 ${buildroot}${TARGET_SYSCONFDIR}/rpm/macros.python3

	# scripts
	rm -f ${buildroot}${prefix}/bin/pydoc3*
	install -m 755 Tools/scripts/pydoc3 ${buildroot}${prefix}/bin/pydoc${python_version}
	ln -s pydoc${python_version} ${buildroot}${prefix}/bin/pydoc3
	install -m 755 Tools/scripts/2to3 ${buildroot}${prefix}/bin/2to3-${python_version}
	# install -m 755 Tools/scripts/pyvenv ${buildroot}${prefix}/bin/pyvenv-${python_version} || :

	${MAKE} clean >/dev/null

	rm -f ${buildroot}${TARGET_LIBDIR}$multilibdir/charset.alias	
	rm -f ${buildroot}${TARGET_BINDIR}/*-config

	chmod u+w ${buildroot}${TARGET_LIBDIR}/*.a
	if test "$multilibdir" != ""; then
		mkdir -p ${buildroot}${TARGET_LIBDIR}$multilibdir
		mv ${buildroot}${TARGET_LIBDIR}/*.a ${buildroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	# remove the hard links and/or symlinks,
	# keeping python2.7 the default
	for dir in bin include lib ; do
	    rm -f ${buildroot}${prefix}/$dir/python
	done
	rm -f ${buildroot}${prefix}/lib/pkgconfig/python.pc
	
	# remove wrapper scripts for packages not built
	rm -f ${buildroot}${prefix}/bin/idle*

	# the directory for modules must exist; getpath.c depends on it
	mkdir -p ${buildroot}${TARGET_LIBDIR}/python${python_version}/lib-dynload
	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
