#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=python2
VERSION=-2.7.14
VERSIONPATCH=

srcarchive=Python${VERSION}

. ${scriptdir}/functions.sh

PATCHES="
patches/python2/python2-2.7-dirs.patch
patches/python2/python2-distutils-rpm-8.patch
patches/python2/python2-2.7.5-multilib.patch
patches/python2/python2-2.5.1-sqlite.patch
patches/python2/python2-2.7.4-canonicalize2.patch
patches/python2/python2-2.6-gettext-plurals.patch
patches/python2/python2-2.6b3-curses-panel.patch
patches/python2/python2-sparc_longdouble.patch
patches/python2/python2-2.7.2-fix_date_time_compiler.patch
patches/python2/python2-bundle-lang.patch
patches/python2/python2-2.7-libffi-aarch64.patch
patches/python2/python2-bsddb6.diff
patches/python2/python2-2.7.9-ssl_ca_path.patch
patches/python2/python2-ncurses-6.0-accessors.patch
patches/python2/python2-reproducible.patch
patches/python2/python2-fix-shebang.patch
patches/python2/python2-skip_random_failing_tests.patch
patches/python2/python2-sorted_tar.patch
patches/python2/python2-path.patch
patches/python2/python2-mint.patch
patches/python2/python2-mintnosharedmod.patch
patches/python2/python2-mintsetupdist.patch
patches/python2/python2-math.patch
"
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
patches/python2/python2-remove-static-libpython.diff
"
POST_INSTALL_SCRIPTS="
patches/python2/python2-python.csh
patches/python2/python2-python.sh
patches/python2/python2-pythonstart
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/python
${TARGET_LIBDIR#/}/python2.7
${TARGET_MANDIR#/}/*
${TARGET_SYSCONFDIR#/}/*
"

srcdir="$here/Python${VERSION}"
MINT_BUILD_DIR="$srcdir"

unpack_archive

python_version=$(echo ${VERSION#-} | head -c 3)

cd "$MINT_BUILD_DIR"

# drop Autoconf version requirement
sed -i 's/^version_required/dnl version_required/' configure.ac

autoreconf -fiv
# autoreconf may have overwritten config.sub
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub

# prevent make from trying to rebuild asdl stuff, which requires existing
# python installation
touch Parser/asdl* Python/Python-ast.c Include/Python-ast.h

COMMON_CFLAGS="\
	-O2 -fomit-frame-pointer -fwrapv \
	-DOPENSSL_LOAD_CONF"
STACKSIZE="-Wl,-stack,512k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${TARGET_PREFIX}
	--build=`./config.guess`
	--docdir=${TARGET_PREFIX}/share/doc/packages/python
	--disable-ipv6
	--with-fpectl
	--disable-shared --enable-static
	--enable-unicode=ucs4
	--with-system-expat
	--without-thread
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
	${MAKE} DESTDIR="${buildroot}" SYSROOT=${sysroot} install

	${MAKE} clean >/dev/null


	rm -f ${buildroot}${TARGET_LIBDIR}$multilibdir/charset.alias	
	rm -f ${buildroot}${TARGET_BINDIR}/*-config

	chmod u+w ${buildroot}${TARGET_LIBDIR}/*.a
	if test "$multilibdir" != ""; then
		mkdir -p ${buildroot}${TARGET_LIBDIR}$multilibdir
		mv ${buildroot}${TARGET_LIBDIR}/*.a ${buildroot}${TARGET_LIBDIR}$multilibdir
	fi
	
	# remove hard links and replace them with symlinks
	for dir in bin include lib ; do
	    rm -f ${buildroot}${prefix}/$dir/python
	    ln -s python${python_version} ${buildroot}${prefix}/$dir/python
	done

	########################################
	# startup script
	########################################
	install -d -D -m 755 ${buildroot}${TARGET_SYSCONFDIR}/profile.d
	install -m 644 ${BUILD_DIR}/patches/${PACKAGENAME}/python2-pythonstart ${buildroot}${TARGET_SYSCONFDIR}/pythonstart
	install -m 644 ${BUILD_DIR}/patches/${PACKAGENAME}/python2-python.sh ${buildroot}${TARGET_SYSCONFDIR}/profile.d/python.sh
	install -m 644 ${BUILD_DIR}/patches/${PACKAGENAME}/python2-python.csh ${buildroot}${TARGET_SYSCONFDIR}/profile.d/python.csh

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
