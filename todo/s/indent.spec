Summary: A GNU program for formatting C code.
Name: indent
Version: 2.2.5
Release: 3
Copyright: GPL
Group: Applications/Text
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp://prep.ai.mit.edu/pub/gnu/indent-2.2.5.tar.gz
Prereq: /sbin/install-info
BuildRoot: /var/tmp/indent-root
Summary(de): Ein GNU-Programm, um C-Quellcode zu formatieren.

%description
Indent is a GNU program for beautifying C code, so that it is easier to
read.  Indent can also convert from one C writing style to a different
one.  Indent understands correct C syntax and tries to handle incorrect
C syntax.

Install the indent package if you are developing applications in C and
you'd like to format your code automatically.

%description -l de
Indent ist ein GNU-Programm zum Verschönern von C-Quelltexten, so daß 
diese leichter zu lesen sind.  Indent kann auch zwischen verschiedenen
C-Schreibstilen konvertieren.  Indent kennt die Syntax von C und versucht
syntaktische Fehler in C-Quellen zu korrigieren.

Installieren Sie das Paket indent, falls Sie in C Anwendungen entwickeln
und Ihre Quelltexte automatisch formatieren lassen möchten.

%prep
%setup -q

%build
./configure --prefix=/usr
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,info,share/man/man1}

make prefix=$RPM_BUILD_ROOT/usr exec_prefix=$RPM_BUILD_ROOT/usr mandir=$RPM_BUILD_ROOT/usr/share/man install
gzip -9nf $RPM_BUILD_ROOT/usr/info/indent.info*
install -m644 indent.1 $RPM_BUILD_ROOT/usr/share/man/man1
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/indent.1

strip $RPM_BUILD_ROOT/usr/bin/indent
stack --fix=64k $RPM_BUILD_ROOT/usr/bin/indent ||:

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/indent.info.gz /usr/info/dir --entry="* indent: (indent).				Program to format source code."

%preun
if [ "$1" = 0 ]; then
	/sbin/install-info --delete /usr/info/indent.info.gz /usr/info/dir --entry="* indent: (indent).                 	 Program to format source code."
fi

%files
%defattr(-,root,root)
/usr/bin/indent
/usr/share/man/man1/indent.1.gz
/usr/info/indent.info*
%doc NEWS README* AUTHORS COPYING ChangeLog

%changelog
* Fri May 05 2000 Edgar Aichinger <eaiching@t0.or.at>
- added german summary and description

* Fri Apr 21 2000 Edgar Aichinger <eaiching@t0.or.at>
- build against mintlibs 0.55.2

* Fri Mar 24 2000 Edgar Aichinger <eaiching@t0.or.at>
- new version, man page to /usr/share/man 
- added %doc (spec)

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
