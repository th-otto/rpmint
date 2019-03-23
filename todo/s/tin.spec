Name: tin
Summary: tin - an easy-to-use USENET news reader
Version: 1.6.2
Release: 1
Copyright: BSD
Group: Applications/News
Source: ftp://ftp.tin.org/pub/news/clients/tin/v1.6/%{name}-%{version}.tar.gz
Buildroot: /var/tmp/%{name}-%{version}-%{release}
Packager: Keith Scroggins <kws@radix.net>

%description
tin is an easy-to-use USENET news reader for the console using NNTP.
It supports threading, scoring, different charsets, and many other
useful things. It has also support for different languages.

%define prefix /usr
%define confdir /etc/tin

%prep
%setup -q
CFLAGS="$RPM_OPT_FLAGS" ./configure --with-install-prefix=$RPM_BUILD_ROOT \
 --prefix=%{prefix} \
 --mandir=%{_mandir} \
 --sysconfdir=%{confdir} \
 --verbose \
 --disable-echo \
 --enable-prototypes \
 --enable-nntp-only

%build
make build

%install
ln -s /usr/bin/strip src/strip
make install
make install_sysdefs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %attr(755,root,root) %{confdir}
%config(noreplace) %attr(644,root,root) %{confdir}/*
%attr(755,root,root) %{prefix}/bin/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%doc doc/CHANGES doc/INSTALL doc/TODO doc/WHATSNEW
%doc doc/auth.txt doc/filtering doc/good-netkeeping-seal doc/iso2asc.txt
%doc doc/keymap.sample doc/mailcap.sample doc/pgp.txt doc/reading-mail.txt
%doc doc/tools.txt doc/umlaute.txt doc/umlauts.txt doc/wildmat.3
%doc README

%changelog
* Wed Oct 15 2003 Keith Scroggins <kws@radix.net>
- Specfile created for tin 1.6.2.

