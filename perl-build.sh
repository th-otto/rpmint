#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=perl
VERSION=-5.26.1
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/perl/perl-5.26.0.patch
patches/perl/perl-regexp-refoverflow.patch
patches/perl/perl-nroff.patch
patches/perl/perl-netcmdutf8.patch
patches/perl/perl-HiRes.t-timeout.patch
patches/perl/perl-saverecontext.patch
patches/perl/perl-skip_time_hires.patch
patches/perl/perl-incfix.patch
patches/perl/perl-5.18.2-overflow.patch
patches/perl/perl-reproducible.patch
patches/perl/perl-skip_flaky_tests_powerpc.patch
patches/perl/perl-posix-sigaction.patch
patches/perl/perl-rpm-macros.patch
patches/perl/perl-mint-hints.patch
patches/perl/perl-mint-inet6.patch
patches/perl/perl-cpan-db-file.patch
patches/perl/perl-fp-classify.patch
patches/perl/perl-gdbm-compat-link-order.patch
patches/perl/perl-cross-use-correct-strip.patch
"
DISABLED_PATCHES="
patches/perl/perl-5.6.0-db1.patch
patches/perl/perl-5.6.0-buildsys.patch
patches/perl/perl-5.6.0-installman.patch
patches/perl/perl-5.6.0-nodb.patch
patches/perl/perl-5.6.0-prereq.patch
patches/perl/perl-5.6.0-mint.patch
patches/perl/perl-5.6.0-makedepend.patch
patches/perl/perl-5.6.0-cross.patch
patches/perl/perl-mint-workaround-exit.patch
"


BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/perl5
${TARGET_MANDIR#/}/*
${TARGET_SYSCONFDIR#/}/*
"

MINT_BUILD_DIR="$srcdir"

perl_cross=perl-cross-mint.tar.gz
if ! test -f "$ARCHIVES_DIR/$perl_cross"; then
	curl -L --output "$ARCHIVES_DIR/$perl_cross" https://github.com/th-otto/perl-cross/archive/mint.tar.gz
fi

unpack_archive

cd "$MINT_BUILD_DIR"

tar --strip-components=1 -xf "$ARCHIVES_DIR/$perl_cross"

COMMON_CFLAGS="\
	-Wall -Wno-unused-function \
	-fno-strict-aliasing \
	-D_GNU_SOURCE \
	-DPERL_USE_SAFE_PUTENV \
	-D_LARGEFILE_SOURCE \
	-D_FILE_OFFSET_BITS=64"
OPT_CFLAGS="-O2 -fomit-frame-pointer -fwrapv"

CONFIGURE_FLAGS="
	--target=${TARGET}
	--prefix=${TARGET_PREFIX}
	-Dvendorprefix=${TARGET_PREFIX}
	-Dosname=mint
	-Dman1dir=${TARGET_MANDIR}/man1
	-Dman3dir=${TARGET_PREFIX}/lib/perl5/man/man3
"
STACKSIZE="-Wl,-stack,512k"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

#
# installperl already takes care of that;
# also the files are made read-only so we can't use the tools
#
NO_STRIP=true
NO_RANLIB=true


CPU_ARCHNAME_000=-000
CPU_ARCHNAME_020=-020
CPU_ARCHNAME_v4e=-v4e

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	eval archname=\${CPU_ARCHNAME_$CPU}

	case $CPU in
		v4e) longdblsize=8; longdblkind=0 ;;
		*) longdblsize=12; longdblkind=4 ;;
	esac

	case $TARGET in
		*-*-mintelf*) lddlflags="-r -Wl,--oformat,elf32-m68k" ;;
		*) lddlflags="-r" ;;
	esac

	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE" \
	sh ./configure \
		${CONFIGURE_FLAGS} \
		-Dcc="$gcc $CPU_CFLAGS" \
		-Dccflags="$OPT_CFLAGS $COMMON_CFLAGS" \
		-Dcppflags="$COMMON_CFLAGS" \
		-Doptimize="$OPT_CFLAGS" \
		-Darchname=${TARGET}${archname} \
		-Dlongdblsize=${longdblsize} \
		-Dlongdblkind=${longdblkind} \
		-Dlddlflags="$lddlflags" \
		-Dcccdlflags="-Wno-unused-function" \
		-Dso='none' \
		|| exit 1

	${MAKE} || exit 1
	
	# this is sometimes not build???
	${MAKE} pod/perlmodlib.pod

	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} DESTDIR="${buildroot}" install

	install -d -m 755 ${buildroot}${TARGET_LIBDIR}/perl5/vendor_perl/${VERSION#-}/${TARGET}${archname}
	install -d -m 755 ${buildroot}${TARGET_LIBDIR}/perl5/site_perl/${VERSION#-}/${TARGET}${archname}
	gzip -9 -f ${buildroot}${TARGET_LIBDIR}/perl5/man/man3/*.3

	# change a hardlink to a symlink
	rm -f ${buildroot}${TARGET_PREFIX}/share/man/man1/perlthanks.1
	$LN_S perlbug.1 ${buildroot}${TARGET_PREFIX}/share/man/man1/perlthanks.1

	# shit, B:: files are interpreted as drive B: :-(
	# how to handle this?
	# the good thing is that rm can handle this
	# the bad thing is that only rm work correct
	rm -vf ${buildroot}${TARGET_LIBDIR}/perl5/man/man3/B::*

	# install macros.perl file
	install -D -m 644 macros.perl ${buildroot}${TARGET_SYSCONFDIR}/rpm/macros.perl
	
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	

	make_bin_archive $CPU

	rm -rf ${buildroot}${TARGET_LIBDIR}/perl5/${VERSION#-}/${TARGET}${archname}
done

move_prefix
configured_prefix="${prefix}"

make_archives
