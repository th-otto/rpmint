%define pkgname git

%rpmint_header

Summary:        Fast, scalable, distributed revision control system
Name:           %{crossmint}%{pkgname}
Version:        2.21.0
Release:        1
License:        GPL-2.0-only
Group:          Development/Tools/Version Control

Packager:       %{packager}
URL:            https://git-scm.com/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://www.kernel.org/pub/software/scm/git/%{pkgname}-%{version}.tar.xz
Source1: patches/git/git-apache2-gitweb.conf
Source2: patches/git/git-daemon.service
Source3: patches/git/git-git.xinetd

Patch0: patches/git/git-0001-We-trust-the-system-is-consistent-and-do-not-let-ind.patch
Patch1: patches/git/git-0002-gitweb-Enable-prevent_xss-by-default.patch
Patch2: patches/git/git-0004-cook-up-tcsh-completion-to-be-installable-bnc-853183.patch
Patch3: patches/git/git-0005-adapt-paths-in-zsh-completion-bnc-853183.patch
Patch4: patches/git/git-0006-Drop-the-last-updated-footer-in-documentation.patch
Patch5: patches/git/git-0007-Support-for-the-FreeMiNT-platform.patch
Patch6: patches/git/git-0008-Do-not-include-config.mak.uname-when-cross-compiling.patch
Patch7: patches/git/git-worktree-fix-worktree-add-race.patch
Patch8: patches/git/git-setup-don-t-fail-if-commondir-reference-is-deleted.patch
Patch9: patches/git/git-use-pkg-config.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  tcsh
BuildRequires:  asciidoc
BuildRequires:  xmlto
Requires:       python3
Requires:       perl

%rpmint_build_arch

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations and
full access to internals.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

autoconf
rm -rf autom4te.cache

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--sysconfdir=/etc
	--disable-nls
	--disable-shared
	--localstatedir=/var/lib
	--config-cache
	--with-libpcre2
	--with-python=%{_rpmint_target_prefix}/bin/python3
"
STACKSIZE=-Wl,-stack,128k

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_fread_reads_directories=yes
ac_cv_snprintf_returns_bogus=no
ac_cv_lib_curl_curl_global_init=yes
EOF
	%rpmint_append_gnulib_cache
}

#
# do not build any perl module at all for cross-compiling,
# since that will add perl() provides to the binary rpm,
# which will conflict with the host
#
cat <<EOF >config.mak
prefix = %{_rpmint_target_prefix}
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
%{expr:"%{buildtype}" == "cross" ? "NO_PERL = YesPlease" : ""}
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

make_args="V=1"
if test "%{_build_os}" != "mint"; then
	make_args+=" CROSS_COMPILING=1"
fi


#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	all_make_args="%{?_smp_mflags} ${make_args} gitexecdir=%{_rpmint_target_prefix}/libexec/git$multilibexecdir"

	make ${all_make_args}
	make ${all_make_args} doc
	make ${all_make_args} -C contrib/subtree

	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make ${all_make_args} DESTDIR="${buildroot}" install install-doc
	make ${all_make_args} DESTDIR="${buildroot}" -C contrib/subtree install install-doc

	install -d "${buildroot}/etc/apache2/conf.d"
	install -m 644 "%{S:1}" "${buildroot}/etc/apache2/conf.d/gitweb.conf"
	install -d -m 755 "${buildroot}/srv/git"
	install -d -m 755 "${buildroot}/etc/xinetd.d"
	install -m 644 "%{S:3}" "${buildroot}/etc/xinetd.d/git"
	install -m 644 -D contrib/completion/git-completion.bash "${buildroot}/etc/bash_completion.d/git.sh"
	install -m 644 -D contrib/completion/git-prompt.sh "${buildroot}/etc/bash_completion.d/git-prompt.sh"
	install -m 755 -D contrib/workdir/git-new-workdir "${buildroot}/%{_rpmint_target_prefix}/bin"
	(cd contrib/completion
	 mkdir -p "${buildroot}/%{_rpmint_target_prefix}/share/tcsh"
	 tcsh ./git-completion.tcsh
	 install -m 644 -D git.csh "${buildroot}/etc/profile.d/git.csh"
	)
	install -m 644 -D contrib/completion/git-completion.zsh "${buildroot}/etc/zsh_completion.d/_git"

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	# install via macro later
	rm -fv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}/COPYING*

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/libexec/git$multilibexecdir/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make ${all_make_args} clean >/dev/null
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%license COPYING* LGPL*
%doc README.md RelNotes
%{_isysroot}/etc/*
%dir %{_isysroot}/srv/git
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/libexec/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}/*
%{_isysroot}%{_rpmint_target_prefix}/share/git-core/*
%{_isysroot}%{_rpmint_target_prefix}/share/git-gui/*
%{_isysroot}%{_rpmint_target_prefix}/share/gitk/*
%if "%{buildtype}" != "cross"
%{_isysroot}%{_rpmint_target_prefix}/share/gitweb/*
%{_isysroot}%{_rpmint_target_prefix}/share/perl5/*
%endif


%changelog
* Fri Apr 07 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
