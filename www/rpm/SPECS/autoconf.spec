%define pkgname autoconf

%rpmint_header

Summary:        A GNU Tool for Automatically Configuring Source Code
Name:           %{crossmint}%{pkgname}
Version:        2.69
Release:        1
License:        GPL-3.0-or-later
Group:          Development/Tools/Building

Packager:       %{packager}
URL:            http://www.gnu.org/software/autoconf

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://ftp.gnu.org/gnu/autoconf/%{pkgname}-%{version}.tar.xz
Patch0:  patches/autoconf/autoconf-2.69-0001-install-version.patch
Patch1:  patches/autoconf/autoconf-2.69-0002-atomic-replace.patch
Patch2:  patches/autoconf/autoconf-2.69-0003-ltdl.patch
Patch3:  patches/autoconf/autoconf-2.69-0004-cache.patch
Patch4:  patches/autoconf/autoconf-2.69-0006-man.patch
Patch5:  patches/autoconf/autoconf-2.69-0007-define.patch
Patch6:  patches/autoconf/autoconf-2.69-0008-crossconfig.patch
Patch7:  patches/autoconf/autoconf-2.69-0009-perl-5.17-fixes.patch
Patch8:  patches/autoconf/autoconf-texinfo.patch

BuildRequires:  m4 >= 1.4.6
Requires:       %{crossmint}info
Requires:       %{crossmint}gawk
Requires:       %{crossmint}m4
Requires:       %{crossmint}mktemp
Requires:       %{crossmint}perl

BuildArch:      noarch
%if "%{buildtype}" != "cross"
%define _arch noarch
%endif

%description
GNU Autoconf is a tool for configuring source code and makefiles. Using
autoconf, programmers can create portable and configurable packages,
because the person building the package is allowed to specify various
configuration options.

You should install autoconf if you are developing software and would
like to create shell scripts to configure your source code packages.<br />

Note that the autoconf package is not required for the end user who may
be configuring software with an autoconf-generated script; autoconf is
only required for the generation of the scripts, not their use.

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

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
"

NO_STRIP=true

for CPU in noarch; do
	CFLAGS="$COMMON_CFLAGS" \
	LDFLAGS="$COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS}

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make clean >/dev/null
done


%install

%rpmint_cflags

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


%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}


%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS BUGS INSTALL NEWS README THANKS TODO
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/autoconf
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 2.69

* Thu Oct 21 2010 Keith Scroggins <kws@radix.net>
- Updated to 2.68

* Mon May 05 2003 Marc-Anton Kehr <m.kehr@ndh.net>
- updated to 2.57

* Mon May 28 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.50

* Mon Jul 19 1999 Guido Flohr <guido@freemint.de>
- Added German translations.
- Added patch for config.guess and config.sub.
