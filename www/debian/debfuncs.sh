unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

topdir=`rpm --eval '%{_topdir}'`
RPMS="${topdir}/RPMS"
DEBIAN="${topdir%/*}/debian"
SPECS="${DEBIAN}/specs"
REPO="${DEBIAN}/ubuntu"
POOL="${REPO}/pool"