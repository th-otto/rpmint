#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=arj
VERSION=-3.10.22
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/arj/arj-3.10.22-mint.patch
patches/arj/arj-3.10.22-missing-protos.patch
patches/arj/arj-3.10.22-custom-printf.patch
patches/arj/arj-3.10.22-quotes.patch
patches/arj/arj-3.10.22-reproducible.patch
patches/arj/arj-3.10.22-fixstrcpy.patch
patches/arj/arj-001_arches_align.patch
patches/arj/arj-002_no_remove_static_const.patch
patches/arj/arj-003_64_bit_clean.patch
patches/arj/arj-004_parallel_build.patch
patches/arj/arj-doc_refer_robert_k_jung.patch
patches/arj/arj-strip.patch
"
DISABLED_PATCHES="patches/automake/mintelf-config.sub"

BINFILES="
${TARGET_BINDIR#/}/arj
${TARGET_BINDIR#/}/rearj
${TARGET_BINDIR#/}/arjdisp
${TARGET_MANDIR#/}/man1/*
"

MINT_BUILD_DIR="$srcdir/gnu"

unpack_archive

cd "$MINT_BUILD_DIR"
autoreconf -fiv
rm -rf autom4te.cache
cp "$BUILD_DIR/patches/automake/mintelf-config.sub" config.sub || exit 1

COMMON_CFLAGS="-O2 -fomit-frame-pointer -s -Wall ${ELF_CFLAGS} $LTO_CFLAGS"

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


for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

#
# a native arj is needed by the makefiles
#
	cd "$MINT_BUILD_DIR"
	./configure --enable-outdir=${BASEDIR}
	cd ..

	${MAKE} prepare
	ARJ_DIR=${BASEDIR}/en/rs/arj
	export NATIVE_ARJ=${srcdir}/${ARJ_DIR}/arj
	${MAKE} ${ARJ_DIR}/arj || exit 1
	export NATIVE_ARJ=${MINT_BUILD_DIR}/native_arj
	mv ${ARJ_DIR}/arj ${NATIVE_ARJ} || exit 1
	
#
# now for the real one
#
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	cd "$MINT_BUILD_DIR"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir
	cd ..
	${MAKE} prepare
	${MAKE} clean

	${MAKE} CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/msgbind
	${MAKE} CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/today
	#${MAKE} CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/make_key
	${MAKE} CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/postproc
	${MAKE} CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/join
	${MAKE} CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/packager
	
	${MAKE} || exit 1
	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install || exit 1

	# remove the register remainders of arj's sharewares time
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/arj-register
	rm -f ${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1/arj-register.1*

	${MAKE} clean
	make_bin_archive $CPU
done

configured_prefix="${prefix}"

make_archives
