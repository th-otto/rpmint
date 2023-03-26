%define pkgname libiconv

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Libiconv is a conversion library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.17
Release:        1
License:        LGPL-2.1-or-later AND GPL-3.0-or-later
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.gnu.org/software/libiconv

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch1: libiconv-1.16-aliases.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  m4

%rpmint_build_arch

%description
The libiconv library provides an iconv() implementation, for use on
systems which don't have one, or whose implementation cannot convert
from/to Unicode.

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

export CHOST=$TARGET

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=%{_rpmint_target} --prefix=%{_rpmint_target_prefix}
	--docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname} \
	--enable-extra-encodings
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done


%install

%rpmint_cflags

# already done in loop above
# make install DESTDIR=%{buildroot}%{_rpmint_sysroot}

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
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man
%{_isysroot}%{_rpmint_target_prefix}/share/doc
%{_isysroot}%{_rpmint_target_prefix}/share/locale



%changelog
* Wed Mar 1 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
