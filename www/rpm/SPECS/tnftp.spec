%define pkgname tnftp

%rpmint_header

Summary:        Enhanced FTP Client
Name:           %{crossmint}%{pkgname}
Version:        20230507
Release:        1.5
License:        BSD-3-Clause
Group:          Productivity/Networking/Ftp/Clients

Packager:       %{packager}
URL:            https://ftp.netbsd.org/pub/NetBSD/misc/tnftp/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.netbsd.org/pub/NetBSD/misc/tnftp/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/tnftp/tnftp-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  make
Provides:       %{crossmint}libedit-devel

%rpmint_build_arch

%description
%{pkgname} is the FTP (File Transfer Protocol) client from NetBSD.  FTP is a widely
used protocol for transferring files over the Internet and for archiving files.
%{pkgname} provides some advanced features beyond the Linux netkit ftp client, but
maintains a similar user interface to the traditional ftp client.  It was
formerly called lukemftp.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoreconf -fiv
cp %{S:1} buildaux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-editcomplete
	--disable-ipv6
"

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

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	ln -sf tnftp %{buildroot}%{_rpmint_bindir}/ftp

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

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
%license COPYING
%doc ChangeLog NEWS README THANKS
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/share/man



%changelog
* Mon Jul 08 2024 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
