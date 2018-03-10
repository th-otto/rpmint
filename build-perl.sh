#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=perl
VERSION=-5.6.0
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/perl/perl-5.6.0-buildsys.patch
patches/perl/perl-5.6.0-installman.patch
patches/perl/perl-5.6.0-nodb.patch
patches/perl/perl-5.6.0-prereq.patch
patches/perl/perl-5.6.0-mint.patch
patches/perl/perl-5.6.0-makedepend.patch
patches/perl/perl-5.6.0-cross.patch
"
# Perl does not have a single entry point to define what db library to use
# so the patch below is mostly broken...
DISABLED_PATCHES="
patches/perl/perl5.005_03-db1.patch
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/*
${TARGET_MANDIR#/}/*
"

MINT_BUILD_DIR="$srcdir"


unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -Wall"

CONFIGURE_FLAGS=" \
	-d -e -s -K \
	-Dprefix=${TARGET_PREFIX} \
	-Dinstallprefix=${THISPKG_DIR}${sysroot}${TARGET_PREFIX} \
	-Dosname=mint \
	-Dcf_email=\"fnaumann@freemint.de\" \
	-Di_db \
	-Di_gdbm \
	-Dman1dir=${TARGET_MANDIR}/man1 \
	-Dman3dir=${TARGET_PREFIX}/lib/perl5/man/man3"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"


CPU_ARCHNAME_000=-000
CPU_ACRHNAME_020=-020
CPU_ARCHNAME_v4e=-v4e

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	eval archname=\${CPU_ARCHNAME_$CPU}
	STACKSIZE="-Wl,-stack,128k"

cat > config.over <<EOF
osname=mint
osvers=
ar=`which ${TARGET}-ar 2>/dev/null`
full_ar=`which ${TARGET}-ar 2>/dev/null`
ranlib='${ranlib}'
cc="${TARGET}-gcc"
cpp="${TARGET}-cpp"
cppflags="-fno-strict-aliasing"
cpprun="${TARGET}-cpp -E"
cppstdin="${TARGET}-cpp -E"
cpplast='-'
cppminus='-'
ld="${TARGET}-gcc"
ldflags="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE"
archname=${TARGET}${archname}
byteorder='4321'
lseeksize='4'
libc=''
libs='-lm'
EOF

cat > Policy.sh <<EOF
osname=mint
osvers=
archname=${TARGET}${archname}
crosscompile='define'
byteorder='4321'
locincpth=""
loclibpth=""
glibpth=""
xlibpth=""
charsize=1
alignbytes=2
libswanted='gdbm socket m'
so='none'
usemymalloc='n'
usrinc=''
d_suidsafe='undef'
usevfork='true'
timeincl='sys/time.h time.h '
libswanted='gdbm socket m'
strings='string.h'
usrinc='/none'
i_time='define'
i_systime='define'
i_systimek='undef'
doublesize='8'
longlongsize='8'
lseeksize='4'
ptrsize='4'
d_Gconvert='gcvt((x),(n),(b))'
d_PRIEldbl='define'
d_PRIFldbl='define'
d_PRIGldbl='define'
d_PRIX64='define'
d_PRId64='define'
d_PRIeldbl='define'
d_PRIfldbl='define'
d_PRIgldbl='define'
d_PRIi64='define'
d_PRIo64='define'
d_PRIu64='define'
d_PRIx64='define'
sPRIfldbl='"llf"'
sPRIfldbl='"llf"'
sPRIgldbl='"llg"'
sPRIeldbl='"lle"'
sPRIFldbl='"llF"'
sPRIGldbl='"llG"'
sPRIEldbl='"llE"'
d_Gconvert='gcvt((x),(n),(b))'
sPRIX64='"llX"'
sPRId64='"lld"'
sPRIi64='"lli"'
sPRIo64='"llo"'
sPRIu64='"llu"'
sPRIx64='"llx"'
d_castneg='define'
d_memchr='define'
d_memcmp='define'
d_memset='define'
d_sigsetjmp='define'
d_strchr='define'
d_setresgid='undef'
d_setresuid='undef'
EOF

case $CPU in
	v4e) echo "longdblsize='8'" >> Policy.sh ;;
	*) echo "longdblsize='12'" >> Policy.sh ;;
esac

	sh ./Configure \
		${CONFIGURE_FLAGS} \
		-Dcc="${TARGET}-gcc" \
		-Dccflags="$CPU_CFLAGS" \
		-Dcpp="${TARGET}-cpp" \
		-Dcpprun="${TARGET}-cpp -E" \
		-Dcppstdin="${TARGET}-cpp -E" \
		-Doptimize="$CPU_CFLAGS $COMMON_CFLAGS" \
		-Darchname=${TARGET}${archname} \
		-Dhintfile=Policy.sh \
		|| exit 1

	${MAKE} $JOBS || exit 1
	
	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install
	install -m 755 utils/pl2pm ${buildroot}${TARGET_PREFIX}/bin/pl2pm
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	
	exit 0
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
