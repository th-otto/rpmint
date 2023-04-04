#!/bin/sh

me="$0"
scriptdir=${0%/*}

PACKAGENAME=bash
VERSION=-4.4
PATCHLEVEL=.23
VERSIONPATCH=

. ${scriptdir}/functions.sh

PATCHES="
patches/bash/bash-4.4-patches/bash44-001
patches/bash/bash-4.4-patches/bash44-002
patches/bash/bash-4.4-patches/bash44-003
patches/bash/bash-4.4-patches/bash44-004
patches/bash/bash-4.4-patches/bash44-005
patches/bash/bash-4.4-patches/bash44-006
patches/bash/bash-4.4-patches/bash44-007
patches/bash/bash-4.4-patches/bash44-008
patches/bash/bash-4.4-patches/bash44-009
patches/bash/bash-4.4-patches/bash44-010
patches/bash/bash-4.4-patches/bash44-011
patches/bash/bash-4.4-patches/bash44-012
patches/bash/bash-4.4-patches/bash44-013
patches/bash/bash-4.4-patches/bash44-014
patches/bash/bash-4.4-patches/bash44-015
patches/bash/bash-4.4-patches/bash44-016
patches/bash/bash-4.4-patches/bash44-017
patches/bash/bash-4.4-patches/bash44-018
patches/bash/bash-4.4-patches/bash44-019
patches/bash/bash-4.4-patches/bash44-020
patches/bash/bash-4.4-patches/bash44-021
patches/bash/bash-4.4-patches/bash44-022
patches/bash/bash${VERSION}.dif
patches/bash/bash-2.03-manual.patch
patches/bash/bash-4.0-security.patch
patches/bash/bash-4.3-2.4.4.patch
patches/bash/bash-3.0-evalexp.patch
patches/bash/bash-3.0-warn-locale.patch
patches/bash/bash-4.3-decl.patch
patches/bash/bash-4.3-include-unistd.dif
patches/bash/bash-3.2-printf.patch
patches/bash/bash-4.3-loadables.dif
patches/bash/bash-4.1-completion.dif
patches/bash/bash-4.0-setlocale.dif
patches/bash/bash-4.3-winch.dif
patches/bash/bash-4.1-bash.bashrc.dif
patches/bash/bash-man2html-no-timestamp.patch
patches/bash/bash-4.3-perl522.patch
patches/bash/bash-4.3-extra-import-func.patch
patches/bash/bash-4.4-paths.patch
patches/bash/bash-4.4-profile.patch
patches/bash/bash-4.4-mint.patch
patches/bash/bash-cross-comp.patch
"

DISABLED_PATCHES="
patches/bash/bash-4.3-pathtemp.patch
patches/bash/bash-4.2-nscdunmap.dif
patches/bash/bash-4.2-endpw.dif
patches/bash/bash-readline-7.0.dif
patches/bash/bash-readline-6.3-input.dif
patches/bash/bash-readline-5.2-conf.patch
patches/bash/bash-readline-6.2-metamode.patch
patches/bash/bash-readline-6.2-endpw.dif
patches/bash/bash-readline-6.2-xmalloc.dif
patches/bash/bash-readline-6.3-destdir.patch
patches/bash/bash-readline-6.3-rltrace.patch
patches/automake/mintelf-config.sub
"

BINFILES="
${TARGET_BINDIR#/}/*
bin/*
${TARGET_MANDIR#/}/man1/*
${TARGET_PREFIX#/}/share/info/*
${TARGET_PREFIX#/}/share/doc/bash/*
${TARGET_PREFIX#/}/share/bash/helpfiles/*
etc/skel
"

unpack_archive

cd "$srcdir"

autoconf || exit 1
rm -rf autom4te.cache config.h.in.orig

cp "${BUILD_DIR}/patches/automake/mintelf-config.sub" support/config.sub

cd "$MINT_BUILD_DIR"

COMMON_CFLAGS="-O2 -fomit-frame-pointer -DIMPORT_FUNCTIONS_DEF=0"
STACKSIZE="-Wl,-stack,256k"

SYSMALLOC="--without-gnu-malloc --without-bash-malloc"
READLINE="--with-installed-readline"

COMMON_CONFIGURE_FLAGS="--host=${TARGET} \
	--prefix=${prefix} \
	--sysconfdir=/etc \
	--disable-nls \
	--with-curses \
	--with-afs \
	$SYSMALLOC \
	$READLINE \
	--enable-separate-helpfiles=${TARGET_PREFIX}/share/bash/helpfiles \
	--disable-strict-posix-default \
	--config-cache"

CONFIGURE_FLAGS="$COMMON_CONFIGURE_FLAGS \
	--enable-job-control \
	--enable-alias \
	--enable-readline \
	--enable-history \
	--enable-bang-history \
	--enable-directory-stack \
	--enable-process-substitution \
	--enable-prompt-string-decoding \
	--enable-select \
	--enable-help-builtin \
	--enable-array-variables \
	--enable-brace-expansion \
	--enable-command-timing \
	--enable-disabled-builtins \
"

MINSH_CONFIGURE_FLAGS="$COMMON_CONFIGURE_FLAGS \
	--enable-minimal-config \
	--enable-arith-for-command \
	--disable-readline \
	--without-installed-readline \
	--disable-history \
	--enable-array-variables \
	--enable-brace-expansion \
	--enable-casemod-attributes \
	--enable-casemod-expansion \
	--enable-cond-command \
	--enable-cond-regexp \
	--enable-directory-stack \
	--enable-dparen-arithmetic \
	--enable-extended-glob \
"

# set to true if /bin/sh should be a minimal shell
minsh=true


export PKG_CONFIG_LIBDIR="$prefix/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_func_chown_works=yes
ac_cv_func_strcoll_works=yes
ac_cv_func_working_mktime=yes
bash_cv_func_sigsetjmp=present
bash_cv_getcwd_malloc=yes
bash_cv_job_control_missing=present
bash_cv_sys_named_pipes=present
bash_cv_sys_siglist=yes
bash_cv_under_sys_siglist=yes
bash_cv_unusable_rtsigs=no
bash_cv_wcontinued_broken=yes
bash_cv_wexitstatus_offset=8
gt_cv_int_divbyzero_sigfpe=yes
EOF
	append_gnulib_cache
}

disable_iconv()
{
	# even if we have iconv, we don't want to use it,
	# because mintlib does not support locales, and it
	# just bloats the binary
	sed -i 's/^D\["HAVE_ICONV"\]="[ ]*[01]"$/D\["HAVE_ICONV="\]=" 0"/
s/^S\["LIBICONV"\]="\([^"]*\)"$/S\["LIBICONV"\]=""/
s/^S\["LTLIBICONV"\]="\([^"]*\)"$/S\["LTLIBICONV"\]=""/' config.status
	./config.status
}

for CPU in ${ALL_CPUS}; do
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache

	if $minsh; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
		"$srcdir/configure" ${MINSH_CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir \
		--libexecdir='${exec_prefix}/libexec/bash'$multilibexecdir
		hack_lto_cflags
		disable_iconv

		${MAKE} ${JOBS} Program=sh sh || exit 1
		${MAKE} distclean
	fi
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"$srcdir/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/bash'$multilibexecdir

	sed -i 's/^install:.*/install:/' examples/loadables/Makefile

	hack_lto_cflags
	disable_iconv

	${MAKE} ${JOBS} || exit 1

	${MAKE} DESTDIR="${THISPKG_DIR}${sysroot}" install
	
	mkdir -p ${THISPKG_DIR}${sysroot}/bin
	mv ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/bash ${THISPKG_DIR}${sysroot}/bin
	
	if $minsh; then
		cd ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}
		install ${MINT_BUILD_DIR}/sh ${THISPKG_DIR}${sysroot}/bin/sh
		rm -fv sh
		$LN_S ../../bin/sh sh
	else
		cd ${THISPKG_DIR}${sysroot}/bin
		rm -fv sh
		$LN_S bash sh
		cd ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}
		rm -fv sh
		$LN_S ../../bin/bash sh
	fi
	cd ${THISPKG_DIR}${sysroot}/bin
	rm -fv rbash
	$LN_S bash rbash
	cd ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}
	rm -fv rbash
	$LN_S ../../bin/bash rbash
	
	cd ${MINT_BUILD_DIR}
	${MAKE} clean >/dev/null

	cd ${THISPKG_DIR}${sysroot}
	rm -f ${TARGET_LIBDIR#/}$multilibdir/charset.alias	

	mkdir -p ${THISPKG_DIR}${sysroot}/etc/skel
	install -m 644 ${BUILD_DIR}/patches/bash/bash-dot.bashrc    ${THISPKG_DIR}${sysroot}/etc/skel/.bashrc
	install -m 644 ${BUILD_DIR}/patches/bash/bash-dot.profile   ${THISPKG_DIR}${sysroot}/etc/skel/.profile
    touch -t 199605181720.50 ${THISPKG_DIR}${sysroot}/etc/skel/.bash_history
    chmod 600 ${THISPKG_DIR}${sysroot}/etc/skel/.bash_history
	chmod 755 ${THISPKG_DIR}${sysroot}${TARGET_BINDIR}/bashbug
    
	make_bin_archive $CPU
done

move_prefix
configured_prefix="${prefix}"
copy_pkg_configs

# not really patches, just to get them in the archive
PATCHES="$PATCHES patches/bash/bash-dot.bashrc patches/bash/bash-dot.profile"

make_archives
