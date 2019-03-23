%define PACKAGE_NAME junkbuster
#%define PACKAGE_URL http://www.waldherr.org/junkbuster/
%define PACKAGE_URL http://internet.junkbuster.com/

Summary: The Internet Junkbuster v2.0.2
Vendor:Sparemint
Name: %PACKAGE_NAME
Version: 2.0.2
Release: 1
Source0: http://internet.junkbuster.com/ijb20.tar.Z
Patch: ijb-2.0-mint.patch
Copyright: GPL
Prefix: /usr
BuildRoot: /var/tmp/%{name}-root
Group: Networking/Utilities
URL: %PACKAGE_URL
Packager: Edgar Aichinger <eaiching@t0.or.at>
Distribution: Sparemint
Summary(de): Der Internet Junkbuster v2.0.2

# Stefan Waldherr's patched rpm conflicts with this plain version.
# Hasn't yet been released for Sparemint... we need to wait for a more
# stable mintinit version (e.g. pidof run from an init script
# freezes my falcon completely. Guido?
# Conflicts: junkbuster-swa

%description
The Internet Junkbuster (TM) blocks unwanted banner ads and protects
your privacy from cookies and other threats. It's free under the GPL
(no warranty), runs under *NIX and works with almost any browser. You
need to clear you browser's cache and specify the proxy-server,
described in /usr/doc/junkbuster-2.0.2.

%description -l de
Der Internet Junkbuster (TM) blockiert unerwünschte Werbebanner und schützt
Ihre Privatsphäre vor Cookies und anderen Bedrohungen. Er ist frei unter der
GPL (ohne Garantie), läuft unter *NIX und funktioniert mit fast jedem Browser.
Sie müssen den Cache Ihres Browsers löschen und den Proxy-Server angeben,
wie in /usr/doc/junkbuster-2.0.2 beschrieben.

# -----------------------------------------------------------------------------

%prep

# only the original tarball and mint patch.
%setup -n ijb20 -q

%patch -p1 -b .mint

# -----------------------------------------------------------------------------

%build

make MORE_CFLAGS="$RPM_OPT_FLAGS"

# strip resulting program file.
strip junkbuster

# -----------------------------------------------------------------------------

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/var/log/junkbuster,%{prefix}/{sbin,share/man/man8},/etc/junkbuster}
install -s -m 744 junkbuster $RPM_BUILD_ROOT%{prefix}/sbin/junkbuster
cp -f junkbuster.1 $RPM_BUILD_ROOT%{prefix}/share/man/man8/junkbuster.8
gzip -9nf $RPM_BUILD_ROOT%{prefix}/share/man/man8/junkbuster.8
cp -f sblock.ini $RPM_BUILD_ROOT/etc/junkbuster/blockfile
cp -f scookie.ini $RPM_BUILD_ROOT/etc/junkbuster/cookiefile
cp -f saclfile.ini $RPM_BUILD_ROOT/etc/junkbuster/aclfile
cp -f junkbstr.ini $RPM_BUILD_ROOT/etc/junkbuster/config
cp -f sforward.ini $RPM_BUILD_ROOT/etc/junkbuster/forward
cp -f strust.ini $RPM_BUILD_ROOT/etc/junkbuster/trust

install -m 744 -d $RPM_BUILD_ROOT/var/log/junkbuster

# to avoid weird %doc error on my Freemint system...<ea>
mkdir -p $RPM_BUILD_ROOT/%{prefix}/doc/junkbuster-2.0.2

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%files
%doc ijbfaq.html ijbman.html README README.MiNT gpl.html
%attr (-,nobody,nobody) /var/log/junkbuster
%config /etc/junkbuster/*
%attr (-,nobody,nobody) %{prefix}/sbin/junkbuster
%{prefix}/share/man/man8/junkbuster.8.gz

# -----------------------------------------------------------------------------

%changelog
* Thu Sep 21 2000 <eaiching@t0.or.at>
- first release for SpareMiNT 
- changed Vendor, Packager, Distribution
- added german Summary/Description
- moved (compressed) manpages to /usr/share/man
- config files now in /etc/junkbuster
