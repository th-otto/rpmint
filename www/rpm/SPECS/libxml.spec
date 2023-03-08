%define pkgname libxml

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        An XML library
Summary(de):    Eine XML-Bibliothek
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.8.9
Release:        1
License:        LGPL
Group:          Development/Libraries

Packager:       Edgar Aichinger <eaiching@t0.or.at>
URL:            http://xmlsoft.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://download.gnome.org/sources/libxml/1.8/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/libxml-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-zlib
BuildRequires:  cross-mint-libiconv
Provides:       cross-mint-libxml-devel
%else
BuildRequires:  pkgconfig(zlib)
BuildRequires:  readline
BuildRequires:  libiconv
Provides:       libxml-devel
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
The libxml package contains an XML library, which allows you to
manipulate XML files. XML (eXtensible Markup Language) is a data
format for structured document interchange via the Web.

%description -l de
Das Paket libxml enthält eine XML-Bibliothek, die Ihnen ermöglicht,
XML-Dateien zu manipulieren. XML (eXtensible Markup Language) ist
ein Datenformat für den Austausch strukturierter Dokumente über das Web.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

cp %{S:1} config.sub

%build

autoreconf -fiv

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
STACKSIZE="-Wl,-stack,128k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --sysconfdir="/etc" \
    --disable-shared
    --enable-static
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete config script
	rm -f %{buildroot}%{_rpmint_bindir}/xml-config
	rmdir %{buildroot}%{_rpmint_bindir} || :
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	find %{buildroot}%{_rpmint_libdir} -type f -name "xmlConf.sh" -delete -printf "rm %p\n"
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

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
#doc AUTHORS ChangeLog NEWS README COPYING COPYING.LIB TODO
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Wed Mar 08 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Apr 26 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.8.9

* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Sun Nov 07 1999 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
