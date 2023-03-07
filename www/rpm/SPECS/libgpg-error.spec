%define pkgname libgpg-error

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Library That Defines Common Error Values for All GnuPG Components
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.46
Release:        1
License:        GPL-2.0-or-later and LGPL-2.1-or-later
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.gnupg.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnupg.org/gcrypt/libgpg-error/%{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/libgpg-error-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make

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
This is a library that defines common error values for all GnuPG
components.  Among these are GPG, GPGSM, GPGME, GPG-Agent, libgcrypt,
pinentry, SmartCard Daemon, and possibly more in the future.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

./autogen.sh

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --disable-shared
    --disable-threads
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir
	echo '#undef HAVE_PTHREAD_H' >> config.h
	echo "#undef HAVE_PTHREAD_API" >> config.h
	echo "#undef HAVE_PTHREAD_MUTEX_RECURSIVE" >> config.h
	echo "#undef HAVE_PTHREAD_RWLOCK" >> config.h
	echo "#undef SIZEOF_PTHREAD_MUTEX_T" >> config.h
	echo "#undef USE_POSIX_THREADS" >> config.h

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove useless manpage for gpg-error-config
	rm -rf %{buildroot}%{_rpmint_target_prefix}/share/man/*/gpg-error-config*

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	rm -f %{buildroot}%{_rpmint_bindir}/gpg-error-config
	rm -f %{buildroot}%{_rpmint_bindir}/gpgrt-config
	rmdir %{buildroot}%{_rpmint_bindir} || :

# create pkg-config file
mkdir -p %{buildroot}%{_rpmint_libdir}/pkgconfig
cat > %{buildroot}%{_rpmint_libdir}/pkgconfig/%{pkgname}.pc <<-EOF
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: %{pkgname}
Description: Libgpg-error is a small library that originally defined common error values for all GnuPG components
Version: %{version}
URL: http://www.gnupg.org/

Libs: -lgpg-error
Cflags:
EOF

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
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%endif



%changelog
* Tue Mar 7 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
