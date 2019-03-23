Summary: GNU recode
Name: recode
Version: 3.4
Release: 1
Source: prep.ai.mit.edu:/pub/gnu/recode-3.4.tar.gz
Copyright: GPL
Group: Applications/Text
BuildRoot: /var/tmp/recode-root
Summary(de): GNU-Recode
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint

%description
The GNU recode utility convert files between various character sets.

%description -l de 
GNU-Recode konvertiert Dateien zwischen verschiedenen Zeichensätzen
(bzw. Zeichentabellen).

%prep
%setup

%build
./configure --prefix=/usr
make "CFLAGS=$RPM_OPT_FLAGS" "LDFLAGS=-s"

%install
rm -rf $RPM_BUILD_ROOT
make "prefix=$RPM_BUILD_ROOT/usr" install
gzip -n -9f $RPM_BUILD_ROOT/usr/info/recode.info*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644, root, root, 0755)
%doc BACKLOG COPYING INSTALL NEWS README THANKS File-Latin1
%attr(0755, root, root) /usr/bin/recode
/usr/info/recode.info*

%changelog
* Sat Sep 11 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial revision.
