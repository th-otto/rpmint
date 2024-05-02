#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=ninja
VERSION=-1.11.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/ninja-disable-maxprocs-test.patch
patches/${PACKAGENAME}/ninja-re2c-g.patch
patches/${PACKAGENAME}/ninja-mint.patch
"
EXTRA_DIST="
patches/${PACKAGENAME}/ninja-macros.ninja
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_PREFIX#/}/share
${TARGET_PREFIX#/}/lib
"

unpack_archive

cd "$MINT_BUILD_DIR"

python3 ./configure.py --verbose --bootstrap
mv ninja build-ninja
rm -rf build build.ninja

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS ${ELF_CFLAGS}"

STACKSIZE="-Wl,-stack,512k"

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	CXX=${TARGET}-g++ \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	AR=${TARGET}-ar \
	LDFLAGS="$STACKSIZE -s" \
	python3 ./configure.py --verbose --host=mint
	./build-ninja -v $JOBS || exit 1

	buildroot="${THISPKG_DIR}${sysroot}"
	_rpmconfigdir=${TARGET_PREFIX}/lib/rpm
	
	install -D -p -m 0755 ninja ${buildroot}${TARGET_BINDIR}/ninja
	install -D -p -m 0644 misc/zsh-completion ${buildroot}${TARGET_PREFIX}/share/zsh/site-functions/_ninja
	install -D -p -m 0644 misc/ninja.vim ${buildroot}${TARGET_PREFIX}/share/vim/site/syntax/ninja.vim
	install -D -p -m 0644 misc/bash-completion ${buildroot}${TARGET_PREFIX}/share/bash-completion/completions/ninja
	install -D -p -m 0644 "$BUILD_DIR/patches/${PACKAGENAME}/ninja-macros.ninja" ${buildroot}${_rpmconfigdir}/macros.d/macros.ninja

	make_bin_archive $CPU
	
	rm -rf build build.ninja
done

make_archives
