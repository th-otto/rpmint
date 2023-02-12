unset CDPATH

topdir=`rpm --eval '%{_topdir}'`
RPMS="${topdir}/RPMS"
DEBIAN="${topdir%/*}/debian"
SPECS="${DEBIAN}/specs"
REPO="${DEBIAN}/ubuntu"
POOL="${REPO}/pool"
