#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=mksh
VERSION=-57
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/${PACKAGENAME}/mksh-vendor-mkshrc.patch
patches/${PACKAGENAME}/mksh-Allow-files-without-the-executable-bit.patch
"
DISABLED_PATCHES="
"

BINFILES="
bin/*
${TARGET_BINDIR#/}/*
${TARGET_MANDIR#/}/man1/
${TARGET_PREFIX#/}/share/doc
"

unpack_archive

cd "$srcdir"

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer $LTO_CFLAGS ${ELF_CFLAGS} ${CFLAGS_AMIGAOS}"
case $TARGET in
m68k-atari-mint*)
	STACKSIZE="-Wl,-stack,256k"
	;;
m68k-amigaos*)
	;;
esac

CONFIGURE_FLAGS="--host=${TARGET} --prefix=${prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"

HAVE_SYS_SIGLIST=0
HAVE_SYS_ERRLIST=0
HAVE__SYS_SIGLIST=0
HAVE__SYS_ERRLIST=0
export HAVE_SYS_SIGLIST HAVE_SYS_ERRLIST HAVE__SYS_SIGLIST HAVE__SYS_ERRLIST

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	export TARGET_OS=FreeMiNT
	export CC=${gcc}
	export CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}"
	export CPPFLAGS='-DMKSH_VENDOR_MKSHRC_PATH=\"/etc/mkshrc\" -DMKSH_SMALL'
	CPPFLAGS="$CPPFLAGS -DKSH_VERSIONNAME_VENDOR_EXT=\\\"\ +${VENDOR}\\\""

	sh ./Build.sh -r
    # build lksh to automatically enable -o posix if called as sh
    CPPFLAGS="$CPPFLAGS -DMKSH_BINSHPOSIX"
    sh ./Build.sh -L -r

	for shell in mksh lksh; do
	    install -D -p -m 755 ${shell} ${THISPKG_DIR}${sysroot}/bin/${shell}
	    install -D -p -m 644 ${shell}.1 ${THISPKG_DIR}${sysroot}${TARGET_MANDIR}/man1/${shell}.1
	    mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}
	    ln -sf ../../bin/${shell} ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/${shell}
	done
	mkdir -p ${THISPKG_DIR}${sysroot}${TARGET_SYSCONFDIR}
	ln -sf bash.bashrc ${THISPKG_DIR}${sysroot}${TARGET_SYSCONFDIR}/mkshrc
    install -D -p -m 644 dot.mkshrc ${THISPKG_DIR}${sysroot}${TARGET_PREFIX}/share/doc/mksh/dot.mkshrc

	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

make_archives
