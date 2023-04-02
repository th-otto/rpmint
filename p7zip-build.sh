#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=p7zip
VERSION=-16.02
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/p7zip-16.02-CVE-2017-17969.patch
patches/${PACKAGENAME}/p7zip-CVE-2016-9296.patch
patches/${PACKAGENAME}/p7zip-mint.patch
"
DISABLED_PATCHES="
patches/${PACKAGENAME}/p7zip-16.02_norar.patch
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share/*
"

unpack_archive

cd "$srcdir"

sed -i s,444,644,g install.sh
sed -i s,555,755,g install.sh

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS ${CFLAGS_AMIGAOS}"
case $TARGET in
m68k-atari-mint*)
	STACKSIZE="-Wl,-stack,256k"
	;;
m68k-amigaos*)
	;;
esac

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"

for CPU in ${ALL_CPUS}; do

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \

cat <<EOF > makefile.machine
OPTFLAGS=$CPU_CFLAGS $COMMON_CFLAGS
ALLFLAGS=\${OPTFLAGS} -pipe \
        -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE \
        -DNDEBUG -DENV_UNIX \
        -D_7ZIP_LARGE_PAGES \
        -D_7ZIP_ST \
        \$(LOCAL_FLAGS)

CXX=${TARGET}-g++
CC=${TARGET}-gcc
CC_SHARED=
LINK_SHARED=

LOCAL_LIBS= ${STACKSIZE}
LOCAL_LIBS_DLL= ${STACKSIZE}

OBJ_CRC32=\$(OBJ_CRC32_C)
OBJ_AES=

EOF

	${MAKE} $JOBS || exit 1

mkdir -p "${THISPKG_DIR}${sysroot}${prefix}/bin"
mkdir -p "${THISPKG_DIR}${sysroot}${prefix}/share/man/man1"
install -m755 "$BUILD_DIR/patches/${PACKAGENAME}/p7zip-p7zip" "${THISPKG_DIR}${sysroot}${prefix}/bin/p7zip"
install -m644 "$BUILD_DIR/patches/${PACKAGENAME}/p7zip-p7zip.1" "${THISPKG_DIR}${sysroot}${prefix}/share/man/man1/p7zip.1"
./install.sh \
    ${prefix}/bin \
    ${prefix}/lib/${PACKAGENAME} \
    ${prefix}/share/man \
    ${prefix}/share/doc/packages/${PACKAGENAME} \
    "${THISPKG_DIR}${sysroot}"

	${MAKE} clean
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
