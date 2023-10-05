%define pkgname dash

%rpmint_header

Summary:        POSIX-compliant Implementation of /bin/sh
Name:           %{crossmint}%{pkgname}
Version:        0.5.12
Release:        1
License:        BSD-3-Clause
Group:          System/Shells

Packager:       %{packager}
URL:            http://gondor.apana.org.au/~herbert/dash/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://gondor.apana.org.au/~herbert/dash/files/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

Patch0:  patches/dash/dash-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  %{crossmint}libedit

%rpmint_build_arch

%description
DASH is a POSIX-compliant implementation of /bin/sh that aims to be as small as
possible without sacrificing speed where possible.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-fnmatch \
	--enable-glob \
	--with-libedit \
"
STACKSIZE="-Wl,-stack,128k"

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

	build_dir=`pwd`

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	mkdir -p %{buildroot}%{_rpmint_sysroot}/bin
	mv %{buildroot}%{_rpmint_bindir}/dash %{buildroot}%{_rpmint_sysroot}/bin
	cd %{buildroot}%{_rpmint_bindir}
	$LN_S ../../bin/dash dash

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_rpmint_sysroot}/bin/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	cd "$build_dir"
	make clean >/dev/null
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
%doc ChangeLog
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*


%changelog
* Wed Oct 04 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file for version 0.5.12
