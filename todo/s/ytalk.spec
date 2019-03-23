Summary: A chat program for multiple users.
Name: ytalk
Version: 3.1.1
Release: 1
Copyright: BSD
Group: Applications/Internet
Vendor: Sparemint
Source: %{name}-%{version}.tar.gz
URL: http://www.eleves.ens.fr:8080/home/espel/ytalk/
Packager: Jan Krupka <jkrupka@volny.cz>
BuildRoot: /var/tmp/ytalk-root
Summary: The talk client.

%description
YTalk is a compatible replacement for the Unix talk(1) program, which
adds a number of features. Mainly, it can talk to more than one person 
at a time.

%prep
%setup

%build
./configure
make  
strip ytalk

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/etc
install -m 755 ytalk $RPM_BUILD_ROOT/usr/bin
install -m 644 ytalk.1 $RPM_BUILD_ROOT/usr/man/man1
gzip -9 $RPM_BUILD_ROOT/usr/man/man1/ytalk.1
install -m 644 ytalkrc $RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README README.old ChangeLog BUGS term.doc poster
/usr/bin/ytalk
/usr/man/man1/ytalk.1.gz
/etc/ytalkrc

%changelog
* Sat Dec 08 2001 Jan Krupka <jkrupka@volny.cz>
First realaease for SpareMiNT (new package) 
