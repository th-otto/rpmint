unset CDPATH
unset LANG LANGUAGE LC_ALL LC_CTYPE LC_TIME LC_NUMERIC LC_COLLATE LC_MONETARY LC_MESSAGES

topdir=`rpm --eval '%{_topdir}'`
RPMS="${topdir}/RPMS"
DEBIAN="${topdir%/*}/debian"
SPECS="${DEBIAN}/specs"
REPO="${DEBIAN}/ubuntu"
POOL="${REPO}/pool"


red="\033[27;31m"
coff="\033[m"
if test "`/bin/echo -e`" = "-e"; then
	ECHO_E=/bin/echo
else
	ECHO_E="/bin/echo -e"
fi
