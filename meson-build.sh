#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=meson
VERSION=-1.4.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/meson-test-installed-bin.patch
patches/${PACKAGENAME}/meson-distutils.patch
patches/${PACKAGENAME}/meson-mint.patch
"
EXTRA_DIST="
patches/${PACKAGENAME}/meson-m68k-atari-mint.ini
patches/${PACKAGENAME}/meson-m68k-atari-mintelf.ini
"

python_version=`${TARGET}-pkg-config --modversion python3`

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/*
${TARGET_MANDIR#/}/*
"

unpack_archive

for CPU in ${ALL_CPUS}; do

	cd "$MINT_BUILD_DIR"

	python3 setup.py build

	buildroot="${THISPKG_DIR}${sysroot}"
	_rpmconfigdir=${TARGET_PREFIX}/lib/rpm
	vim_data_dir=${TARGET_PREFIX}/share/vim
	python_sitelib=${TARGET_PREFIX}/lib/python${python_version}/site-packages

	python3 setup.py install -O1 --skip-build --force --root ${buildroot} --prefix ${TARGET_PREFIX}
	install -Dpm 0644 data/macros.meson ${buildroot}${_rpmconfigdir}/macros.d/macros.meson
	install -Dpm 0644 data/syntax-highlighting/vim/ftdetect/meson.vim -t ${buildroot}${vim_data_dir}/site/ftdetect/
	install -Dpm 0644 data/syntax-highlighting/vim/indent/meson.vim -t ${buildroot}${vim_data_dir}/site/indent/
	install -Dpm 0644 data/syntax-highlighting/vim/syntax/meson.vim -t ${buildroot}${vim_data_dir}/site/syntax/
	echo """#!${TARGET_BINDIR}/python3
from mesonbuild.mesonmain import main
import sys

sys.exit(main())
""" > ${buildroot}${TARGET_BINDIR}/meson
	chmod +x ${buildroot}${TARGET_BINDIR}/meson

	cp -r meson.egg-info ${buildroot}${python_sitelib}/meson${VERSION}-py${python_version}.egg-info

# Fix missing data files with distutils
	while read line; do
	  if [[ "$line" = %{_name}/* ]]; then
	    [[ "$line" = *.py ]] && continue
	    cp "$line" "${buildroot}${python_sitelib}/$line"
	  fi
	done < meson.egg-info/SOURCES.txt

# remove linux-specific polkit
	rm -rf ${buildroot}${TARGET_PREFIX}/share/polkit-1

	install -Dpm 0644 "$BUILD_DIR/patches/${PACKAGENAME}/meson-m68k-atari-mint.ini" "${buildroot}${TARGET_PREFIX}/share/meson/cross/m68k-atari-mint.ini"
	install -Dpm 0644 "$BUILD_DIR/patches/${PACKAGENAME}/meson-m68k-atari-mintelf.ini" "${buildroot}${TARGET_PREFIX}/share/meson/cross/m68k-atari-mintelf.ini"
	install -Dpm 0644 "$BUILD_DIR/patches/${PACKAGENAME}/meson-m68k-atari-mint.ini" "${THISPKG_DIR}${prefix}/share/meson/cross/m68k-atari-mint.ini"
	install -Dpm 0644 "$BUILD_DIR/patches/${PACKAGENAME}/meson-m68k-atari-mintelf.ini" "${THISPKG_DIR}${prefix}/share/meson/cross/m68k-atari-mintelf.ini"

	python3 setup.py clean

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

# only include the cross configurations in the *-dev archive
# make_archives

rm -rf "${THISPKG_DIR}${prefix}/${TARGET}"
cd "${THISPKG_DIR}" || exit 1
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-dev.tar.xz *
cd "${BUILD_DIR}" || exit 1
rm -rf "${THISPKG_DIR}"
rm -rf "${srcdir}"
${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${BINTARNAME}.tar.xz ${PATCHES} ${DISABLED_PATCHES} ${EXTRA_DIST} ${POST_INSTALL_SCRIPTS} ${PATCHARCHIVE}
cp -p "$me" ${DIST_DIR}/${PACKAGENAME}${VERSION}${VERSIONPATCH}-build.sh
