%define name       gaim
%define version    0.59.9
%define release    2
%define serial     1
%define prefix     /usr
%define sysconfdir /etc

Summary:	A Gtk+ based multiprotocol instant messaging client
Name:		%{name}
Version:	%{version}
Release:	%{release}
Serial:		%{serial}
Copyright:	GPL
Group:		Applications/Internet
Vendor:		Sparemint
Url:		http://gaim.sf.net/
Source:		%{name}-%{version}.tar.gz
Packager:	Mark Duckworth <mduckworth@atari-source.com>
BuildRoot:	/var/tmp/%{name}-%{version}-root
Requires:	gtk+ >= 1.2.5

%description
Gaim allows you to talk to anyone using a variety of messaging 
protocols, including AIM (Oscar and TOC), ICQ, IRC, Yahoo!, 
MSN Messenger, Jabber, Gadu-Gadu, Napster, and Zephyr.  These 
protocols are implemented using a modular, easy to use design.  
To use a protocol, just load the plugin for it.

Gaim supports many common features of other clients, as well as many 
unique features, such as perl scripting and C plugins.

Gaim is NOT affiliated with or endorsed by AOL.

%prep
%setup

%build
cd ..
patch -p0 < /usr/src/redhat/SOURCES/gaim-0.59.9-mint.patch
cd gaim-0.59.9
CFLAGS="$RPM_OPT_FLAGS" LIBS="-liconv -lsocket" ./configure --prefix=%{prefix} --disable-gnome --disable-artsc --with-static-prpls=all
make

%install
make DESTDIR=$RPM_BUILD_ROOT prefix=%{prefix} sysconfdir=%{sysconfdir} install
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

%files
%defattr(-,root,root)
%{prefix}/bin/gaim
%doc doc/the_penguin.txt doc/CREDITS NEWS COPYING AUTHORS doc/FAQ README ChangeLog plugins/PERL-HOWTO HACKING
%{prefix}/man/man1/*
%attr(755,root,root) 
%{prefix}/lib/gaim/*
%{prefix}/share/locale/*/*/*
%{prefix}/share/pixmaps/gaim.png
%{prefix}/share/gnome/apps/Internet/gaim.desktop

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Sun Jan 18 2004 Mark Duckworth <mduckworth@atari-source.com>
- Release #2
- Added stack fixing and stripping
- Changed vendor to sparemint
- Changed requires

* Sat Sep 10 2003 Mark Duckworth <mduckworth@atari-source.com>
- Initial sparemint import
- Date is definitely incorrect..  Cannot remember initial build date.
