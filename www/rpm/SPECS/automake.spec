%define pkgname automake

%rpmint_header

Summary:        A Program for Automatically Generating GNU-Style Makefile.in Files
Name:           %{crossmint}%{pkgname}
Version:        1.16
Release:        1
License:        GPL-2.0-or-later
Group:          Development/Tools/Building

Packager:       %{packager}
URL:            https://www.gnu.org/software/automake

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/automake/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/automake/automake-1.16-0001-source.patch
Patch1: patches/automake/automake-1.16-0002-crossconfig.patch
Patch2: patches/automake/automake-1.16-0003-subdir-objects.patch
Patch3: patches/automake/automake-1.16-0004-fix-primary-prefix-invalid-couples-test.patch
Patch4: patches/automake/automake-1.16-0006-correct-parameter-parsing-in-test-driver-script.patch

BuildRequires:  m4 >= 1.4.6
Requires:       %{crossmint}autoconf >= 2.69
Requires:       %{crossmint}info
Requires:       %{crossmint}perl

BuildArch:      noarch
%if "%{buildtype}" != "cross"
%define _arch noarch
%endif

%description
Automake is a tool for automatically generating "Makefile.in" files
from "Makefile.am" files.  "Makefile.am" is a series of "make" macro
definitions (with rules occasionally thrown in).  The generated
"Makefile.in" files are compatible with the GNU Makefile standards.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

sed -e 's@-unknown-@-${VENDOR}-@g' lib/config.guess > lib/config.guess.new && mv lib/config.guess.new lib/config.guess
touch -r configure Makefile.am Makefile.in t/testsuite-part.am

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
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
%rpmint_install_info %{pkgname}-history

%preun
%rpmint_uninstall_info %{pkgname}
%rpmint_uninstall_info %{pkgname}-history


%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS doc/amhello-1.0.tar.gz
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal-%{version}/*
%{_isysroot}%{_rpmint_target_prefix}/share/automake-%{version}/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.16

* Fri Nov 05 2010 Keith Scroggins <kws@radix.net>
- Updated to 1.11.1

* Mon May 05 2003 Marc-Anton Kehr <m.kehr@ndh.net>
- updated to 1.7.4

* Mon Jul 19 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Added German translations.
- Added requirement for Autoconf.
