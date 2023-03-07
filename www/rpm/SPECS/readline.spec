%define pkgname readline

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        The Readline Library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        7.0
Release:        1
License:        GPL-3.0-or-later
Group:          System/Shells

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://cnswww.cns.cwru.edu/php/chet/readline/rltop.html

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  bison
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-ncurses
Provides:       cross-mint-libreadline7 = %{version}
%else
BuildRequires:  ncurses
Provides:       libreadline7 = %{version}
%endif

%if "%{buildtype}" == "cross"
BuildArch:      noarch
%else
%define _target_platform %{_rpmint_target_platform}
%if "%{buildtype}" == "v4e"
%define _arch m5475
%else
%if "%{buildtype}" == "020"
%define _arch m68020
%else
%define _arch m68k
%endif
%endif
%endif

%description
The GNU Readline library provides a set of functions for use by
applications that allow users to edit command lines as they are typed
in. Both Emacs and vi editing modes are available. The Readline library
includes additional functions to maintain a list of previously-entered
command lines, to recall and perhaps reedit those lines, and perform
csh-like history expansion on previous commands.

%prep
%setup -q -n %{pkgname}-%{version}
cp %{S:1} support/config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --disable-shared
    --config-cache
"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_func_strcoll_works=yes
bash_cv_func_strcoll_broken=no
bash_cv_must_reinstall_sighandlers=no
bash_cv_func_sigsetjmp=present
bash_cv_func_ctype_nonascii=no
EOF
}

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
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
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Thu Mar 02 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
