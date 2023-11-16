#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=libexif
VERSION=-0.6.22
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/libexif/libexif-build-date.patch
patches/libexif/libexif-shared.patch
"
DISABLED_PATCHES="
patches/libexif/libexif-CVE-2017-7544.patch
patches/libexif/libexif-CVE-2016-6328.patch
"
EXTRA_DIST="
patches/automake/mintelf-config.sub
"

BINFILES="
"

unpack_archive

cd "$srcdir"

export LANG=POSIX
export LC_ALL=POSIX

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" config.sub || exit 1

cd libexif
	
mv exif-byte-order.h exifbyte.h ; ln -s exifbyte.h exif-byte-order.h
mv exif-content.h    exifcont.h ; ln -s exifcont.h exif-content.h
mv exif-data.h       exifdata.h ; ln -s exifdata.h exif-data.h
mv exif-data-type.h  exiftype.h ; ln -s exiftype.h exif-data-type.h
mv exif-entry.h      exifent.h  ; ln -s exifent.h  exif-entry.h
mv exif-format.h     exifform.h ; ln -s exifform.h exif-format.h
mv exif-ifd.h        exififd.h  ; ln -s exififd.h  exif-ifd.h
mv exif-loader.h     exifload.h ; ln -s exifload.h exif-loader.h
mv exif-log.h        exiflog.h  ; ln -s exiflog.h  exif-log.h
mv exif-mem.h        exifmem.h  ; ln -s exifmem.h  exif-mem.h
mv exif-mnote-data.h exifnote.h ; ln -s exifnote.h exif-mnote-data.h
mv exif-tag.h        exiftag.h  ; ln -s exiftag.h  exif-tag.h
mv exif-utils.h      exifutil.h ; ln -s exifutil.h exif-utils.h

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${ELF_CFLAGS}"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--datadir=${prefix}/share \
	--with-doc-dir=${prefix}/share/doc/${PACKAGENAME} \
	--disable-nls \
	--disable-shared"

STACKSIZE="-Wl,-stack,128k"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$multilibdir
	: hack_lto_cflags
	${MAKE} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install

	cd "${THISPKG_DIR}${sysroot}/usr/include/libexif"

mv exif-byte-order.h exifbyte.h ; ln -s exifbyte.h exif-byte-order.h
mv exif-content.h    exifcont.h ; ln -s exifcont.h exif-content.h
mv exif-data.h       exifdata.h ; ln -s exifdata.h exif-data.h
mv exif-data-type.h  exiftype.h ; ln -s exiftype.h exif-data-type.h
mv exif-entry.h      exifent.h  ; ln -s exifent.h  exif-entry.h
mv exif-format.h     exifform.h ; ln -s exifform.h exif-format.h
mv exif-ifd.h        exififd.h  ; ln -s exififd.h  exif-ifd.h
mv exif-loader.h     exifload.h ; ln -s exifload.h exif-loader.h
mv exif-log.h        exiflog.h  ; ln -s exiflog.h  exif-log.h
mv exif-mem.h        exifmem.h  ; ln -s exifmem.h  exif-mem.h
mv exif-mnote-data.h exifnote.h ; ln -s exifnote.h exif-mnote-data.h
mv exif-tag.h        exiftag.h  ; ln -s exiftag.h  exif-tag.h
mv exif-utils.h      exifutil.h ; ln -s exifutil.h exif-utils.h

	cd "$MINT_BUILD_DIR"

	${MAKE} clean >/dev/null
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_LIBDIR}/charset.alias
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
