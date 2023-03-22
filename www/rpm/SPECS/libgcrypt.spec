%define pkgname libgcrypt

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        The GNU Crypto Library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.10.1
Release:        1
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND GPL-3.0-or-later
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://gnupg.org/software/libgcrypt

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://gnupg.org/ftp/gcrypt/libgcrypt/%{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/libgcrypt/libgcrypt-1.10.0-allow_FSM_same_state.patch
Patch1:  patches/libgcrypt/libgcrypt-FIPS-SLI-pk.patch
Patch2:  patches/libgcrypt/libgcrypt-FIPS-SLI-hash-mac.patch
Patch3:  patches/libgcrypt/libgcrypt-FIPS-SLI-kdf-leylength.patch
Patch4:  patches/libgcrypt/libgcrypt-1.10.0-out-of-core-handler.patch
Patch5:  patches/libgcrypt/libgcrypt-jitterentropy-3.4.0.patch
Patch6:  patches/libgcrypt/libgcrypt-FIPS-rndjent_poll.patch
Patch7:  patches/libgcrypt/libgcrypt-1.10.0-use-fipscheck.patch
Patch8:  patches/libgcrypt/libgcrypt-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake >= 1.14
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-libgpg-error >= 1.27
%else
BuildRequires:  libgpg-error-devel >= 1.27
%endif

%rpmint_build_arch

%description
Libgcrypt is a general purpose library of cryptographic building
blocks.  It is originally based on code used by GnuPG.  It does not
provide any implementation of OpenPGP or other protocols.  Thorough
understanding of applied cryptography is required to use Libgcrypt.

%prep
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

./autogen.sh

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --disable-shared
    --disable-hmac-binary-check
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
	echo '#undef HAVE_PTHREAD' >> config.h

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

# create pkg-config file
mkdir -p %{buildroot}%{_rpmint_libdir}/pkgconfig
cat > %{buildroot}%{_rpmint_libdir}/pkgconfig/%{pkgname}.pc <<-EOF
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${prefix}/lib
includedir=\${prefix}/include

Name: %{pkgname}
Description: The GNU Crypto Library
Version: %{version}
URL: http://directory.fsf.org/wiki/Libgcrypt

Libs: -lgcrypt -lgpg-error
Cflags:
Requires: libgpg-error
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
