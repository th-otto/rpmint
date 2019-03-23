Summary       : A GTK+ IRC (chat) client.
Name          : xchat
Version       : 1.4.2
Release       : 1
Copyright     : GPL
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://xchat.org

BuildRequires : XFree86-devel, gtk+
Requires      : XFree86

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://xchat.org/files/source/1.4/xchat-%{version}.tar.gz
Patch0: xchat-1.4.2-fixed.patch
Patch1: xchat-1.4.2-perlinclude.patch
Patch2: xchat-1.4.2-plugininclude.patch
Patch3: xchat-1.4.2-time_t.patch


%description
X-Chat is yet another IRC client for the X Window System and
GTK+. X-Chat is fairly easy to use, compared to other GTK+ IRC
clients, and the interface is quite nicely designed.

Install xchat if you need an IRC client for X.


%prep
%setup -q
%patch0 -p1 -b .fixed
%patch1 -p1 -b .perl
%patch2 -p1 -b .plugin
%patch3 -p1 -b .time_t


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--disable-textfe \
	--disable-panel \
	--disable-perl \
	--disable-python
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

mkdir -p ${RPM_BUILD_ROOT}/etc/X11/applnk/Internet
install -m 644 xchat.desktop ${RPM_BUILD_ROOT}/etc/X11/applnk/Internet/xchat.desktop


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README ChangeLog doc/xchat.sgml doc/*.html
/etc/X11/applnk/Internet/xchat.desktop
%{_prefix}/bin/xchat
%{_prefix}/share/locale/*/*/*


%changelog
* Sat Dec 23 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
