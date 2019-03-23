Summary: The HTML welcome page you'll see after installing Sparemint.
Name: indexhtml
Version: 1.0
Release: 1
Source: indexhtml-%{version}.tar.gz
Copyright: distributable
Group: Documentation
BuildArchitectures: noarch
BuildRoot: /var/tmp/indexhtml-root
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Die HTML-Seite, die zu Sparemint Willkommen heißt.

%description
The indexhtml package contains the HTML page and graphics for
a welcome page shown by your Web browser, which you'll see
after you've successfully installed Red Hat Linux.

%description -l de
Das Indexhtml-Paket enthält die HTML-Seite und Grafiken für eine
Willkommens-Seite, die von Web-Browsern angezeigt werden sollte,
nachdem Sparemint erfolgreich installiert wude.

%prep
%setup -q -n indexhtml-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/doc/HTML

cd $RPM_BUILD_ROOT/usr/doc/HTML
cp -p $RPM_BUILD_DIR/indexhtml-%{version}/* .

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/doc/HTML/*
