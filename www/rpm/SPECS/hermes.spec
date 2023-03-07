%define pkgname Hermes

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A library to convert pixel formats
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.3.3
Release:        1
License:        MIT
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://web.archive.org/web/20040202225109/http://www.clanlib.org/hermes/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0: patches/%{pkgname}/hermes-1.3.3-64bit.patch
Patch1: patches/%{pkgname}/hermes-1.3.3-debian.patch
Patch2: patches/%{pkgname}/hermes-ns-recipe.patch
Patch3: patches/%{pkgname}/hermes-warnings.patch
Patch5: patches/%{pkgname}/hermes-install.patch

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
%else
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  readline
BuildRequires:  libiconv
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
HERMES is a library designed to convert a source buffer with a specified pixel
format to a destination buffer with possibly a different format at the maximum
possible speed.
</br>
On x86 and MMX architectures, handwritten assembler routines are taking over
the job and doing it lightning fast.
</br>
On top of that, HERMES provides fast surface clearing, stretching and some
dithering. Supported platforms are basically all that have an ANSI C compiler
as there is no platform specific code but those are supported: DOS, Win32
(Visual C), Linux, FreeBSD (IRIX, Solaris are on hold at the moment), some BeOS
support.

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

cp %{S:1} config.sub

# mark asm files as NOT needing execstack
for i in src/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --disable-shared
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

	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

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
%else
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%endif



%changelog
* Tue Feb 28 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
