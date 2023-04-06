#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=file
VERSION=-5.32
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/file/file-5.19-misc.dif
patches/file/file-4.24-autoconf.dif
patches/file/file-5.14-tex.dif
patches/file/file-4.20-ssd.dif
patches/file/file-4.20-xen.dif
patches/file/file-5.22-elf.dif
patches/file/file-5.19-printf.dif
patches/file/file-5.12-zip.dif
patches/file/file-5.17-option.dif
patches/file/file-4.21-scribus.dif
patches/file/file-4.21-xcursor.dif
patches/file/file-5.19-cromfs.dif
patches/file/file-5.18-javacheck.dif
patches/file/file-5.19-solv.dif
patches/file/file-5.19-zip2.0.dif
patches/file/file-5.19-biorad.dif
patches/file/file-5.19-clicfs.dif
patches/file/file-5.23-endian.patch
patches/file/file-5.24-nitpick.dif
patches/file/file-5.15-clear-invalid.patch
patches/file/file-secure_getenv.patch
patches/file/file-5.28-btrfs-image.dif
patches/file/file-5.32-mint.patch
patches/file/file-5.32.dif
"
# patches/file/file-5.16-ocloexec.patch
DISABLED_PATCHES="
patches/automake/mintelf-config.sub
"
POST_INSTALL_SCRIPTS="patches/file/file-zisofs.magic"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
${TARGET_PREFIX#/}/share/misc
etc
"

unpack_archive

cd "$srcdir"

export LANG=POSIX
export LC_ALL=POSIX
rm -f Magdir/*,v Magdir/*~
rm -f ltcf-c.sh ltconfig ltmain.sh
autoreconf -fiv
test -s src/magic.h.in || cp -p src/magic.h src/magic.h.in
rm -fv src/magic.h
# patch it again in case it was replaced by autoreconf
cp ${BUILD_DIR}/patches/automake/mintelf-config.sub config.sub

cat "${BUILD_DIR}/patches/file/file-zisofs.magic" >> magic/Localstuff

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -DHOWMANY=69632"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}
	--sysconfdir=/etc
	--disable-nls
	--disable-shared
	--enable-fsect-man5
	--config-cache
"
STACKSIZE="-Wl,-stack,128k"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

mkdir -p ${THISPKG_DIR}${sysroot}/etc
cat << EOF > ${THISPKG_DIR}${sysroot}/etc/magic
# Localstuff: file(1) magic(5) for locally observed files
#     global magic file is ${prefix}/share/misc/magic(.mgc)
EOF

#
# compile a version for the host first, which is needed to compile the magic file
#
./configure --disable-shared --disable-nls
${MAKE} $JOBS
mv src/file src/file.host
mv magic/Localstuff magic/Localstuff.orig
${MAKE} distclean
mv magic/Localstuff.orig magic/Localstuff

create_config_cache()
{
cat <<EOF >config.cache
EOF
	append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir

	hack_lto_cflags
	${MAKE} V=1 FILE_COMPILE='$(top_builddir)/src/file.host' $JOBS || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	mv magic/Localstuff magic/Localstuff.orig
	${MAKE} clean >/dev/null
	mv magic/Localstuff.orig magic/Localstuff
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
