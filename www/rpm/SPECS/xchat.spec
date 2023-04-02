%define pkgname xchat

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary       : A GTK+ IRC (chat) client.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 1.4.2
Release       : 2
License       : GPL-2.0-or-later
Group         : Applications/Internet

Packager:       %{packager}
URL           : http://xchat.org

%rpmint_essential
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
BuildRequires : cross-mint-gtk+-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
BuildRequires : gtk+-devel
Requires      : XFree86
%endif

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://xchat.org/files/source/1.4/%{pkgname}-%{version}.tar.gz
Patch0: xchat-1.4.2-fixed.patch
Patch1: xchat-1.4.2-perlinclude.patch
Patch2: xchat-1.4.2-plugininclude.patch
Patch3: xchat-1.4.2-time_t.patch
Patch4: xchat-1.4.2-configure.patch

%rpmint_build_arch

%description
X-Chat is yet another IRC client for the X Window System and
GTK+. X-Chat is fairly easy to use, compared to other GTK+ IRC
clients, and the interface is quite nicely designed.

Install xchat if you need an IRC client for X.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

touch NEWS
touch ABOUT-NLS
touch config.rpath
chmod 755 config.rpath

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--bindir=%{_rpmint_target_prefix}/X11R6/bin
	--disable-nls
	--disable-textfe
	--disable-panel
	--disable-perl
	--disable-python
"
STACKSIZE="-Wl,-stack,128k"

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 020
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC=${TARGET}-gcc \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	./configure ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}

	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/X11/applnk/Internet
	install -m 644 xchat.desktop %{buildroot}%{_rpmint_sysroot}/etc/X11/applnk/Internet/xchat.desktop

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
%doc README ChangeLog AUTHORS doc/*
%{_isysroot}/etc/X11/applnk/Internet/xchat.desktop
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/xchat
#%%{_isysroot}%%{_rpmint_target_prefix}/share/locale/*/*/*


%changelog
* Sun Apr 02 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
