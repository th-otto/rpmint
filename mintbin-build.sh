#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mintbin
VERSION=-0.3
VERSIONPATCH=-20200828

. ${scriptdir}/functions.sh

PATCHES=""

unpack_archive

cd "$MINT_BUILD_DIR"

CC="${GCC}" ./configure --prefix=${prefix} --disable-nls --target=$TARGET
${MAKE} $JOBS || exit 1

${MAKE} DESTDIR="${THISPKG_DIR}" install || exit 1

cd "${THISPKG_DIR}/${prefix}/bin" || exit 1
${STRIP} *

cd "${THISPKG_DIR}/${prefix}/${TARGET}/bin" || exit 1
${STRIP} *

for i in arconv cnm csize cstrip flags mintbin stack symex; do
	if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
		rm -f ${i} ${i}${BUILD_EXEEXT}
		$LN_S ../../bin/${TARGET}-$i${BUILD_EXEEXT} $i
	fi
done
	
cd "${THISPKG_DIR}"
rm -f ${prefix#/}/share/info/dir
for f in ${prefix#/}/share/info/*; do
	case $f in
	*.gz) ;;
	*) rm -f ${f}.gz; gzip -9 $f ;;
	esac
done

TARNAME=${PACKAGENAME}${VERSION}-${TARGET##*-}${VERSIONPATCH}

${TAR} ${TAR_OPTS} -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz *

cd "${BUILD_DIR}"
if test "$KEEP_PKGDIR" != yes; then
	rm -rf "${THISPKG_DIR}"
fi
if test "$KEEP_SRCDIR" != yes; then
	rm -rf "${srcdir}"
fi

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/${PACKAGENAME}${VERSION}${VERSIONPATCH}-build.sh
