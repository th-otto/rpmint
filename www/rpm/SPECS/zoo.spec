%define pkgname zoo

%rpmint_header

Summary:        Pack Program
Name:           %{crossmint}%{pkgname}
Version:        2.10.1
Release:        1
License:        Public Domain
Group:          Productivity/Archiving/Compression

URL:            http://ftp.math.utah.edu/pub/zoo/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        http://ftp.math.utah.edu/pub/%{pkgname}/%{pkgname}-2.10.1.tar.bz2

Patch0: patches/zoo/zoo-config.patch
Patch1: patches/zoo/zoo-2.10-tempfile.patch
Patch2: patches/zoo/zoo-gcc.patch
Patch3: patches/zoo/zoo-2.10-CAN-2005-2349.patch
Patch4: patches/zoo/zoo-return.patch
Patch5: patches/zoo/zoo-security_pathsize.patch
Patch6: patches/zoo/zoo-security_parse.patch
Patch7: patches/zoo/zoo-2.10-security-infinite_loop.patch
Patch8: patches/zoo/zoo-fclose.patch


%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
Zoo is a packer based on the Lempel-Ziv algorithm. Lots of files on
DOS/AmigaDOS and TOS systems used this packer for their archives. The
compression rate of gzip is not reached, and thus zoo should only be used
for decompressing old archives.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-2-10-1
cd v2-10.1

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

cd v2-10.1

COMMON_CFLAGS="-O3 -fomit-frame-pointer $LTO_CFLAGS -DANSI_HDRS=1 -DANSI_PROTO=1 $LTO_CFLAGS"
STACKSIZE=-Wl,-stack,256k

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

	make \
		CC="${TARGET}-gcc" \
		MODEL="$CPU_CFLAGS $COMMON_CFLAGS -D__linux" \
		CFLAGS=-c \
		zoo fiz || exit 1
	install -Dpm 0755 zoo "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/zoo"
	install -Dpm 0755 fiz "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/fiz"
	install -Dpm 0644 zoo.1 "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/zoo.1"
	install -Dpm 0644 fiz.1 "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/fiz.1"

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make clean
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license v2-10.1/Copyright
%doc v2-10.1/AUTHOR
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
