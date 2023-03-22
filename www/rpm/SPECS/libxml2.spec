%define pkgname libxml2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A Library to Manipulate XML Files
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.10.3
Release:        1
License:        MIT
Group:          Development/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://gitlab.gnome.org/GNOME/libxml2

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://download.gnome.org/sources/%{pkgname}/2.10/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/libxml2-fix-perl.diff
Patch2: patches/%{pkgname}/libxml2-python3-unicode-errors.patch
Patch3: patches/%{pkgname}/libxml2-python3-string-null-check.patch
Patch4: patches/%{pkgname}/libxml2-make-XPATH_MAX_NODESET_LENGTH-configurable.patch

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
BuildRequires:  cross-mint-liblzma5
BuildRequires:  cross-mint-readline
Provides:       cross-mint-libxml2-devel
%else
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  readline
BuildRequires:  libiconv
Provides:       libxml2-devel
%endif

%rpmint_build_arch

%description
The XML C library was initially developed for the GNOME project. It is
now used by many programs to load and save extensible data structures
or manipulate any kind of XML files.

This library implements a number of existing standards related to
markup languages, including the XML standard, name spaces in XML, XML
Base, RFC 2396, XPath, XPointer, HTML4, XInclude, SGML catalogs, and
XML catalogs. In most cases, libxml tries to implement the
specification in a rather strict way. To some extent, it provides
support for the following specifications, but does not claim to
implement them: DOM, FTP client, HTTP client, and SAX.

The library also supports RelaxNG. Support for W3C XML Schemas is in
progress.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

cp %{S:1} config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
STACKSIZE="-Wl,-stack,128k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --docdir=%{_rpmint_target_prefix}/share/doc/%{pkgname}
    --disable-shared
    --enable-static
    --with-html-dir=%{_rpmint_target_prefix}/share/doc/%{pkgname}/html
    --with-fexceptions
    --with-history
    --without-python
    --disable-ipv6
    --with-sax1
    --with-regexps
    --without-threads
    --with-reader
    --with-http
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
	rm -f %{buildroot}%{_rpmint_bindir}/xml2-config
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	find %{buildroot}%{_rpmint_libdir} -type f -name "xml2Conf.sh" -delete -printf "rm %p\n"
	rm -rf %{buildroot}%{_rpmint_libdir}/*/cmake
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
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_cross_pkgconfigdir}
%{_rpmint_datadir}
%else
#doc AUTHORS ChangeLog NEWS README Copyright TODO
#doc doc/*.html doc/html doc/*.gif doc/*.png
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Tue Feb 28 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Tue Apr 23 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 2.4.20

* Tue Jul 10 2001 Frank Naumann <fnaumann@freemint.de>
- first release
