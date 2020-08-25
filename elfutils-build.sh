#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=elfutils
VERSION=-0.170
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/elfutils/elfutils-disable-tests-with-ptrace.patch
patches/elfutils/elfutils-0001-backends-Add-support-for-EM_PPC64-GNU_ATTRIBUTES.patch
patches/elfutils/elfutils-ppc-machine-flags.patch
patches/elfutils/elfutils-no-threads.patch
patches/elfutils/elfutils-mint.patch
patches/elfutils/elfutils-mintelf-config.patch
patches/elfutils/elfutils-lto-warnings.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
"

unpack_archive

cd "$MINT_BUILD_DIR"

# Change DATE/TIME macros to use last change time of ChangeLog
modified=$(head -1 ChangeLog | cut -d" " -f1)
DATE=$(date -d "${modified}" "+%Y-%m-%d")
TIME=$(date -d "${modified}" "+%R")
find . -type f -regex ".*\.c\|.*\.cpp\|.*\.h" -exec sed -i "s/__DATE__/\"${DATE}\"/g;s/__TIME__/\"${TIME}\"/g" {} +
# Set modversion used to verify dynamically loaded ebl backend matches to
# similarly predictable value [upstream default is hostname + date]
MODVERSION="${VENDOR} ${DATE} ${TIME}"
sed --in-place "s/^MODVERSION=.*\$/MODVERSION=\"${MODVERSION}\"/" configure.ac

autoreconf -fi
# autoreconf may have overwritten config.sub
patch -p1 < "$BUILD_DIR/patches/${PACKAGENAME}/elfutils-mintelf-config.patch"

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} \
	--docdir=${TARGET_PREFIX}/share/doc/${PACKAGENAME} \
	--disable-nls \
	--disable-shared \
	--program-prefix=eu- \
	--config-cache \
"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	rm -f config.cache
	if test "$LTO_CFLAGS" != ""; then
		echo 'ac_cv_stack_usage=no' >> config.cache
		echo 'ac_cv_null_dereference=no' >> config.cache
	fi

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	hack_lto_cflags
	
	${MAKE} $JOBS || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	cp -a "${BUILD_DIR}/patches/${PACKAGENAME}/elf.h" "${THISPKG_DIR}${sysroot}/${prefix}/include"
	
	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
