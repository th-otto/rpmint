%define pkgname p7zip

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        A file compression utility
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        16.02
Release:        1
License:        LGPL-2.1-or-later
Group:          Productivity/Archiving/Compression

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://p7zip.sourceforge.net/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.bz2
Source1: patches/%{pkgname}/p7zip-p7zip
Source2: patches/%{pkgname}/p7zip-p7zip.1

Patch0: patches/%{pkgname}/p7zip-16.02-CVE-2017-17969.patch
Patch1: patches/%{pkgname}/p7zip-CVE-2016-9296.patch
Patch2: patches/%{pkgname}/p7zip-mint.patch

%rpmint_essential
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gcc-c++
%else
BuildRequires:  gcc-c++
%endif
BuildRequires:  make
%ifarch x86_64
BuildRequires:  yasm
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
p7zip is a quick port of 7z.exe and 7za.exe (command line version of
7zip, see www.7-zip.org) for Unix. 7-Zip is a file archiver with
highest compression ratio. Since 4.10, p7zip (like 7-zip) supports
little-endian and big-endian machines.

This package provides:
 * 7za - a stand-alone executable (handles less archive formats than 7z)
 * p7zip - a gzip-like wrapper around 7zr/7za

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i s,444,644,g install.sh
sed -i s,555,755,g install.sh


%build

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS} --disable-shared"
STACKSIZE="-Wl,-stack,256k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}"

cat <<EOF > makefile.machine
OPTFLAGS=$CPU_CFLAGS $COMMON_CFLAGS
ALLFLAGS=\${OPTFLAGS} -pipe \
        -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE \
        -DNDEBUG -DENV_UNIX \
        -D_7ZIP_LARGE_PAGES \
        -D_7ZIP_ST \
        \$(LOCAL_FLAGS)

CXX=%{_rpmint_target}-g++
CC=%{_rpmint_target}-gcc
CC_SHARED=
LINK_SHARED=

LOCAL_LIBS= ${STACKSIZE}
LOCAL_LIBS_DLL= ${STACKSIZE}

OBJ_CRC32=\$(OBJ_CRC32_C)
OBJ_AES=

EOF

	make %{?_smp_mflags}

mkdir -p "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin"
mkdir -p "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1"
install -m755 "%{S:1}" "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/p7zip"
install -m644 "%{S:2}" "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/p7zip.1"
./install.sh \
    %{_rpmint_target_prefix}/bin \
    %{_rpmint_target_prefix}/lib/%{pkgname} \
    %{_rpmint_target_prefix}/share/man \
    %{_rpmint_target_prefix}/share/packages/%{pkgname} \
    "%{buildroot}%{_rpmint_sysroot}"

	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
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


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}/*
%{_rpmint_datadir}
%else
%{_rpmint_target_prefix}/bin/*
%{_rpmint_target_prefix}/share
%endif



%changelog
* Sat Mar 04 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
