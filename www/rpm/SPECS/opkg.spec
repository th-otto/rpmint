%define pkgname opkg

%rpmint_header

Summary:        Opkg lightweight package management system
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.6.1
Release:        1
License:        GPL-2.0-or-later
Group:          System/Packages

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://git.yoctoproject.org/cgit/cgit.cgi/opkg/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://git.yoctoproject.org/cgit/cgit.cgi/%{pkgname}/snapshot/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Source2: patches/%{pkgname}/opkg-20_migrate-feeds
Source3: patches/%{pkgname}/opkg-customfeeds.conf
Source4: patches/%{pkgname}/opkg-smime.conf
Source5: patches/%{pkgname}/opkg.conf
Source6: patches/%{pkgname}/opkg-key

Patch0:  patches/%{pkgname}/%{pkgname}-%{version}.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-opkg-devel
%else
Provides:       opkg-devel
%endif

%rpmint_build_arch

%description
Opkg is a lightweight distribution package manager, optimized for embedded applications and static image generation.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} conf/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--mandir=%{_rpmint_target_prefix}/share/man
	--infodir=%{_rpmint_target_prefix}/share/info
	--libdir=%{_rpmint_target_prefix}/lib
	--sysconfdir=/etc
	--localstatedir=/var
	--sharedstatedir=/var/lib
	--with-rundir=/var/run
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--enable-libopkg-api
	--enable-sha256
	--disable-shared
	--disable-python
	--disable-plugins
	--disable-gpg
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	rm -rf autom4te.cache config.h.in.orig

	make V=1 %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/%{pkgname}
	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/%{pkgname}
	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/%{pkgname}/keys
	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/uci-defaults
	mkdir -p %{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}/sbin
	install -m 644 %{S:2} %{buildroot}%{_rpmint_sysroot}/etc/uci-defaults/20_migrate-feeds
	install -m 644 %{S:3} %{buildroot}%{_rpmint_sysroot}/etc/%{pkgname}/customfeeds.conf
	install -m 644 %{S:4} %{buildroot}%{_rpmint_sysroot}/etc/%{pkgname}/opkg-smime.conf
	install -m 644 %{S:5} %{buildroot}%{_rpmint_sysroot}/etc/%{pkgname}/opkg.conf
	install -m 755 %{S:6} %{buildroot}%{_rpmint_sysroot}/%{_rpmint_target_prefix}/sbin/opkg-key

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
%license COPYING
%doc AUTHORS ChangeLog ChangeLog.ipkg NEWS README TODO CONTRIBUTING developer-doc
%dir %{_isysroot}%{_rpmint_target_prefix}/lib/%{pkgname}
%config %{_isysroot}/etc/uci-defaults/*
%dir %{_isysroot}/etc/%{pkgname}/keys
%config(noreplace) %{_isysroot}/etc/%{pkgname}/customfeeds.conf
%config(noreplace) %{_isysroot}/etc/%{pkgname}/opkg-smime.conf
%config(noreplace) %{_isysroot}/etc/%{pkgname}/opkg.conf
%{_isysroot}%{_rpmint_target_prefix}/sbin/*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/share
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Sun Apr 02 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
