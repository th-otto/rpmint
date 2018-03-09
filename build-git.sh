#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=git
VERSION=-2.16.2
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/git/0001-We-trust-the-system-is-consistent-and-do-not-let-ind.patch
patches/git/0002-gitweb-Enable-prevent_xss-by-default.patch
patches/git/0003-fix-broken-bash-completion-with-colored-egrep-bnc-77.patch
patches/git/0004-cook-up-tcsh-completion-to-be-installable-bnc-853183.patch
patches/git/0005-adapt-paths-in-zsh-completion-bnc-853183.patch
patches/git/0006-Drop-the-last-updated-footer-in-documentation.patch
patches/git/0007-Support-for-the-FreeMiNT-platform.patch
patches/git/0008-Do-not-include-config.mak.uname-when-cross-compiling.patch
patches/git/0009-We-need-to-link-to-nghttp2-when-using-lcurl.patch
"
POST_INSTALL_SCRIPTS="
patches/git/apache2-gitweb.conf
patches/git/git-daemon.service
patches/git/git.xinetd
"

BINFILES="
${TARGET_BINDIR#/}/*
${TARGET_LIBDIR#/}/*
${TARGET_PREFIX#/}/libexec/git/*
${TARGET_MANDIR#/}/man1/*
${TARGET_MANDIR#/}/man5/*
${TARGET_MANDIR#/}/man7/*
${TARGET_PREFIX#/}/share/git-core/*
${TARGET_PREFIX#/}/share/git-gui/*
${TARGET_PREFIX#/}/share/gitk/*
${TARGET_PREFIX#/}/share/gitweb/*
${TARGET_PREFIX#/}/share/doc/*
etc/*
srv
"

unpack_archive

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -Wall"

CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--disable-shared \
	--localstatedir=/var/lib \
	--config-cache \
	--with-libpcre2 \
	--with-python=${prefix}/bin/python3"

export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_fread_reads_directories=yes
ac_cv_snprintf_returns_bogus=no
ac_cv_lib_curl_curl_global_init=yes
EOF
	append_gnulib_cache
}

cat <<EOF >config.mak
prefix = ${prefix}
GITWEB_CONFIG = \${sysconfdir}/gitweb.conf
GITWEB_PROJECTROOT = /srv/git
NO_CROSS_DIRECTORY_HARDLINKS = 1
NO_INSTALL_HARDLINKS = 1
PYTHON_PATH = \${prefix}/bin/python3
HOST_CPU = m68k

COMPAT_CFLAGS += -DSA_RESTART=0 -D_BSD_SOURCE=1
NO_MMAP = YesPlease
NO_ICONV = YesPlease
NO_GETTEXT = YesPlease
NO_REGEX = YesPlease
NO_IPV6 = YesPlease
NEEDS_MODE_TRANSLATION = YesPlease
NO_PTHREADS = YesPlease
NO_MEMMEM = YesPlease
NEEDS_SSL_WITH_CURL = YesPlease
NEEDS_CRYPTO_WITH_SSL = YesPlease
NEEDS_NGHTTP2_WITH_CURL = YesPlease
NO_MKDTEMP = YesPlease
NO_MKSTEMPS=YesPlease
NO_PERL_MAKEMAKER = YesPlease
NO_D_TYPE_IN_DIRENT = YesPlease
NO_LIBGEN_H = YesPlease
HAVE_PATHS_H = YesPlease
HAVE_STRINGS_H = YesPlease
HAVE_GETDELIM = YesPlease

#undef variables that slip in from config.mak.uname when cross-compiling

undefine LIBC_CONTAINS_LIBINTL
undefine HAVE_CLOCK_GETTIME
undefine HAVE_CLOCK_MONOTONIC
undefine NEEDS_LIBRT
undefine FREAD_READS_DIRECTORIES
FREAD_READS_DIRECTORIES = UnfortunatelyYes
EOF

make_args="V=1 CROSS_COMPILING=1"


for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	STACKSIZE="-Wl,-stack,128k"

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1
	
	all_make_args="${make_args} gitexecdir=${prefix}/libexec/git$multilibexecdir"
	hack_lto_cflags

	${MAKE} ${all_make_args} || exit 1
	${MAKE} ${all_make_args} doc || exit 1
	${MAKE} ${all_make_args} -C contrib/subtree || exit 1

	buildroot="${THISPKG_DIR}${sysroot}"
	${MAKE} ${all_make_args} DESTDIR="${buildroot}" install install-doc
	${MAKE} ${all_make_args} DESTDIR="${buildroot}" -C contrib/subtree install install-doc
	install -d "${buildroot}/etc/apache2/conf.d"
	install -m 644 "${BUILD_DIR}/patches/git/apache2-gitweb.conf" "${buildroot}/etc/apache2/conf.d/gitweb.conf"
	install -d -m 755 "${buildroot}/srv/git"
	install -d -m 755 "${buildroot}/etc/xinetd.d"
	install -m 644 "${BUILD_DIR}/patches/git/git.xinetd" "${buildroot}/etc/xinetd.d/git"
	install -m 644 -D contrib/completion/git-completion.bash "${buildroot}/etc/bash_completion.d/git.sh"
	install -m 644 -D contrib/completion/git-prompt.sh "${buildroot}/etc/bash_completion.d/git-prompt.sh"
	install -m 755 -D contrib/workdir/git-new-workdir "${buildroot}/${TARGET_BINDIR}"
	(cd contrib/completion
	 mkdir -p "${buildroot}/${TARGET_PREFIX}/share/tcsh"
	 tcsh ./git-completion.tcsh
	 install -m 644 -D git.csh "${buildroot}/etc/profile.d/git.csh"
	)
	install -m 644 -D contrib/completion/git-completion.zsh "${buildroot}/etc/zsh_completion.d/_git"
	
	${MAKE} ${all_make_args} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"

make_archives
