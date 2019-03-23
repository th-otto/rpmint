Summary: Translates rpm database into HTML and RDF info
Name: rpm2html 
%define version 1.2
Version: %{version}
Release: 1
Group: Utilities/System
Source: ftp://rufus.w3.org/pub/rpm2html/%{name}-%{version}.tar.gz
URL: http://rufus.w3.org/linux/rpm2html/
Copyright: W3C Copyright (BSD like).
BuildRoot: /var/tmp/%{name}-root
Patch0: rpm2html-1.2.mintcfg.patch
Packager: Edgar Aichinger <eaiching@t0.or.at>
Distribution: Sparemint
Vendor: Sparemint
Summary(de): Übersetzt die rpm-Datenbank in HTML- und RDF-Informationen

%description
Rpm2html tries to solve 2 big problems one face when
grabbing a RPM package from a mirror on the net and trying to
install it:
   - it gives more information than just the filename before
     installing the package.
   - it tries to solve the dependancy problem by analyzing all
     the Provides and Requires of the set of RPMs. It shows the
     cross references by the way of hypertext links. 
Rpm2html can now dump the metadata associated to RPM packages into
standard RDF files.

%description -l de
Rpm2html versucht, zwei große Probleme zu lösen, denen man begegnet,
wenn man ein RPM-Paket aus dem Netz holt und versucht, es zu
installieren:
   - es stellt mehr Information als nur den Dateinamen zu Verfügung,
     bevor man das Paket installiert.
   - es versucht das Problem der Abhängigkeiten zu lösen, indem es
     die Provides and Requires der vorhandenen RPMs analysiert. Es zeigt
     die Querverweise durch Hypertext-Links an. 
Rpm2html kann jetzt die Metadaten aus RPM-Paketen in Standard RDF Dateien
ausgeben.

%prep
%setup -q
%patch0 -p1 -b .mintcfg
CFLAGS="$RPM_OPT_FLAGS" LIBS="-lport -lsocket" ./configure --host=m68k-atari-mint --prefix=/usr --sysconfdir=/etc

%build
make

%install
install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/etc
install -d $RPM_BUILD_ROOT/usr/share/rpm2html
install -d $RPM_BUILD_ROOT/usr/man/man1
install -d $RPM_BUILD_ROOT/usr/doc
install rpm2html $RPM_BUILD_ROOT/usr/bin
install -m 644 msg.fr $RPM_BUILD_ROOT/usr/share/rpm2html
install -m 644 msg.es $RPM_BUILD_ROOT/usr/share/rpm2html
install -m 644 msg.de $RPM_BUILD_ROOT/usr/share/rpm2html
install -m 644 msg.pl $RPM_BUILD_ROOT/usr/share/rpm2html
install -m 644 msg.cz $RPM_BUILD_ROOT/usr/share/rpm2html
install -m 644 rpm2html.config  $RPM_BUILD_ROOT/etc
install -m 644 rpm2html.1  $RPM_BUILD_ROOT/usr/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1
strip $RPM_BUILD_ROOT/usr/bin/%{name}

%files
%defattr(-,root,root)
%doc CHANGES BUGS Copyright PRINCIPLES README TODO 
%doc rpm2html-cdrom.config rpm2html-en.config
%doc rpm2html.config.mirrors rpm2html-fr.config
%doc rpm2html.config.resources rpm2html-rdf.config
%dir /usr/bin
/usr/bin/rpm2html
/usr/share/rpm2html/msg.fr
/usr/share/rpm2html/msg.es
/usr/share/rpm2html/msg.de
/usr/share/rpm2html/msg.pl
/usr/share/rpm2html/msg.cz
%config /etc/rpm2html.config
%doc /usr/man/man1/rpm2html.1.gz

%changelog
* Wed Sep 15 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
