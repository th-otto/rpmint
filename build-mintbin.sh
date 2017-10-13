#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mintbin
VERSION=-0.3
VERSIONPATCH=-20171006

. ${scriptdir}/functions.sh

PATCHES=""

unpack_archive

cd "$MINT_BUILD_DIR"

./configure --prefix=${prefix} --disable-nls --target=$TARGET
make $JOBS || exit 1

make DESTDIR="${THISPKG_DIR}" install || exit 1

cd "${THISPKG_DIR}/${prefix}/bin" || exit 1
strip -p *

cd "${THISPKG_DIR}/${prefix}/${TARGET}/bin" || exit 1
strip -p *

for i in arconv cnm csize cstrip flags mintbin stack symex; do
	if test -x ../../bin/${TARGET}-$i && test -x $i && test ! -h $i && cmp -s $i ../../bin/${TARGET}-$i; then
		rm -f ${i} ${i}${EXEEXT}
		$LN_S ../../bin/${TARGET}-$i${EXEEXT} $i
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

tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${TARNAME}-bin-${host}.tar.xz .

cd "${BUILD_DIR}"
#rm -rf "${THISPKG_DIR}"
rm -rf "${srcdir}"

test -z "${PATCHES}" || tar --owner=0 --group=0 -Jcf ${DIST_DIR}/${PACKAGENAME}${VERSION}-mint${VERSIONPATCH}.tar.xz ${PATCHES}
cp -p "$me" ${DIST_DIR}/build-${PACKAGENAME}${VERSION}${VERSIONPATCH}.sh
