#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=arj
VERSION=-3.10.22
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="patches/arj/arj-3.10.22-mint.patch"

BINFILES="
${TARGET_BINDIR#/}/arj
${TARGET_BINDIR#/}/rearj
${TARGET_BINDIR#/}/arjdisp
${TARGET_BINDIR#/}/arj-register
${TARGET_MANDIR#/}/man1/*
"

MINT_BUILD_DIR="$srcdir/gnu"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -s -Wall $LTO_CFLAGS"

autoconf || exit 1

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix}"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"


cd "$MINT_BUILD_DIR"

case ${TARGET} in
	*-*-mintelf*) BASEDIR=mintelf ;;
	*-*-mint*) BASEDIR=mint ;;
	*) echo "unsupported target $TARGET" >&2 ;;
esac


for CPU in 020 v4e 000; do
	cd "$MINT_BUILD_DIR"

#
# a native arj is needed by the makefiles
#
	cd "$MINT_BUILD_DIR"
	./configure --enable-outdir=${BASEDIR}

	cd ..
	make prepare
	ARJ_DIR=${BASEDIR}/en/rs/arj
	export NATIVE_ARJ=${srcdir}/${ARJ_DIR}/arj
	make ${ARJ_DIR}/arj || exit 1
	export NATIVE_ARJ=${MINT_BUILD_DIR}/native_arj
	mv ${ARJ_DIR}/arj ${NATIVE_ARJ} || exit 1
	
#
# now for the real one
#
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval libdir=\${CPU_LIBDIR_$CPU}

	cd "$MINT_BUILD_DIR"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" ./configure ${CONFIGURE_FLAGS} --libdir='${exec_prefix}/lib'$libdir
	cd ..
	make prepare
	make clean

	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/msgbind
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/today
	#make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/make_key
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/postproc
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/join
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/packager
	
	make || exit 1
	make DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1
	make clean
	make_bin_archive $CPU
done

configured_prefix="${prefix}"

make_archives
