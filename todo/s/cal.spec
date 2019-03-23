Summary:  Un*x like `cal' program (REPLACEMENT) with MORE features !
Name: cal
Version: 0.28 
Release: 1
Group: Applications
Prefix: /usr
Source: %{name}-%{version}.tar
Copyright: public domain
Distribution: Sparemint
Vendor: Sparemint
Packager: Jan Krupka <jkrupka@volny.cz>
BuildRoot: /var/tmp/cal

%description
Prints a calendar (gregorian dates, before [ 1582 | 1752 ] julian dates)
of one specified month or of one specified year.
It can use .calrc resource file for showing special month dates !

%prep
%setup -q

%build
cc $RPM_OPT_FLAGS cal.c -ocal
strip cal

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 cal $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
/usr/bin/cal

%changelog
* Thu Nov 11 2001 Jan Krupka <jkrupka@volny.cz>
- first release for SpareMiNT (new package)
