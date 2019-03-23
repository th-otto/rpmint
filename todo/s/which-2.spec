Summary: Displays where a particular program in your path is located.
Name: which
Version: 2.14
Release: 1
License: GPL
Group: Applications/System
Source0: ftp://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
Source1: which-2.sh
Source2: which-2.csh
Prefix: %{_prefix}
Buildroot: %{_tmppath}/%{name}-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Zeigt an, wo in Ihrem PATH ein bestimmtes Programm liegt.

%description
The which command shows the full pathname of a specified program, if
the specified program is in your PATH.

%description -l de
Der Befehl which zeigt den kompletten Pfadnamen eines angegebenen Programmes,
falls dieses in Ihrem PATH liegt.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
strip $RPM_BUILD_ROOT/usr/bin/which
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/which.1
gzip -9nf $RPM_BUILD_ROOT/usr/info/which.info
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 $RPM_SOURCE_DIR/which-2.sh $RPM_SOURCE_DIR/which-2.csh \
	$RPM_BUILD_ROOT/etc/profile.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc EXAMPLES README
%{_bindir}/*
%config /etc/profile.d/which-2.*
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Tue Jul 30 2002 Edgar Aichinger <eaiching@t0.or.at>
- updated to 2.14

* Sun Feb 10 2002 Edgar Aichinger <eaiching@t0.or.at>
- updated to 2.13

* Fri May 05 2000 Edgar Aichinger <eaiching@t0.or.at>
- new version 2.11
- fixed manpage location

* Tue Oct 19 1999 Edgar Aichinger <eaiching@t0.or.at>
- updated to version 2.9

* Wed Sep 01 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpage

* Fri Aug 27 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- German Description
- added requirements, Vendor, Packager.
