Summary:   exchange data with Siemens mobile phones
Name:      scmxx
Version:   0.6.1.5
Release:   1
Group:     Communications
Copyright: GPL
Vendor:    Sparemint
Url:       http://www.hendrik-sattler.de/scmxx
Packager:  Jan Krupka <jkrupka@volny.cz>
Source0:   http://www.hendrik-sattler.de/scmxx/download/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
 SCMxx is a console program that allows you to exchange certain types of
 data with mobile phones made by Siemens. Some of the data types that can
 be exchanged are logos, ring tones, vCalendars, phonebook entries, and
 SMS messages. It works with the following models:
 S25,
 S35i, M35i and C35i,
 SL45, S45, ME45 and C45
 and probably others.
 It basically uses the AT command set published by Siemens
 (with some other, additional resources).
 See the website http://www.hendrik-sattler.de/scmxx for details.

%prep
%setup -q

%build
./configure --with-device=/dev/ttyS1 --bindir=%{_bindir} --mandir=%{_mandir}
%{__make}

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
make install DESTDIR="$RPM_BUILD_ROOT"
cp contrib/sms2mail $RPM_BUILD_ROOT/usr/bin/
cp contrib/smssend $RPM_BUILD_ROOT/usr/bin/

mkdir -p $RPM_BUILD_ROOT/usr/man/man1
gzip docs/scmxx.1
mv docs/scmxx.1.gz $RPM_BUILD_ROOT/usr/man/man1/

%clean
%{__make} dist-clean

%files
%defattr(-,root,root)
%doc BUGS INSTALL README TODO AUTHORS CHANGELOG examples docs/*
%attr(0755,-,-) %{_bindir}/scmxx
%attr(0755,-,-) %{_bindir}/sms2mail
%attr(0755,-,-) %{_bindir}/smssend
/usr/man/man1/scmxx.1.gz

%changelog
* Sun Oct 13 2002 Jan Krupka <jkrupka@volny.cz>
- first release for SpareMiNT (new package)

* Tue Feb 12 2002 Jan Krupka <jkrupka@volny.cz>
- updated to version 0.6.1.5

