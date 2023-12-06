#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=lua51
VERSION=-5.1.5
VERSIONPATCH=
major_version=5.1

srcarchive=lua${VERSION}

. ${scriptdir}/functions.sh

PATCHES="
patches/lua53/lua51-build-system.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/lua
${TARGET_MANDIR#/}/man1/*
"

srcdir="$here/$srcarchive"
MINT_BUILD_DIR="$srcdir"
unpack_archive

cd "$MINT_BUILD_DIR"

cat doc/lua.1  | sed 's/TH LUA 1/TH LUA${major_version} 1/' > doc/lua${major_version}.1
cat doc/luac.1 | sed 's/TH LUAC 1/TH LUAC${major_version} 1/' > doc/luac${major_version}.1

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} --disable-shared"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	${MAKE} $JOBS -C src \
		CC="${TARGET}-gcc" \
		AR="${ar} rcu " \
		RANLIB=${ranlib} \
		MYCFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -std=gnu99 -D_GNU_SOURCE" \
		MYLIBS="$CPU_CFLAGS ${STACKSIZE}" \
		V=${major_version} \
		all || exit 1

	${MAKE} \
		V=${major_version} \
		INSTALL_TOP="${THISPKG_DIR}${sysroot}${TARGET_PREFIX}" \
		INSTALL_LIB="${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}"$multilibdir \
		install || exit 1
	# we have already lua 5.3 so don't make this the default
	mv "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}"$multilibdir/liblua.a "${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}"$multilibdir/liblua${major_version}.a
	mv ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/lua ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/lua${major_version}
	mv ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/luac ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/luac${major_version}

	install -D -d -m 755 ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/lua/${major_version}
	
	${MAKE} clean
	make_bin_archive $CPU
done

# create pkg-config file
mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig
cat > ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig/lua${major_version}.pc <<-EOF
prefix=${TARGET_PREFIX}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include/lua${major_version}
INSTALL_LMOD=\${prefix}/share/data/lua/${major_version}
INSTALL_CMOD=\${libdir}/lua/${major_version}

Name: Lua ${major_version}
Description: An Extensible Extension Language
Version: ${VERSION#-}
Libs: -llua${major_version} -lm
Cflags: -I\${includedir}
EOF
# ln -s lua${major_version}.pc ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/pkgconfig/lua.pc

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
