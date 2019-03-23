Summary: A public domain Yacc parser generator.
Name: byacc
Version: 1.9
Release: 3
Copyright: public domain
Group: Development/Tools
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp://ftp.cs.berkeley.edu/ucb/4bsd/byacc.1.9.tar.Z
Patch0: byacc-1.9-fixmanpage.patch
BuildRoot: /var/tmp/byacc-root

%description
Byacc (Berkeley Yacc) is a public domain LALR parser generator which
is used by many programs during their build process.  

If you are going to do development on your system, you will want to install
this package.

%prep
%setup -q -c
%patch -p1 -b .fixmanpage

%build
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1}

install -m 755 -s yacc $RPM_BUILD_ROOT/usr/bin/yacc
stack --fix=64k $RPM_BUILD_ROOT/usr/bin/yacc || :
install -m 644 yacc.1 $RPM_BUILD_ROOT/usr/man/man1/yacc.1
ln -sf yacc $RPM_BUILD_ROOT/usr/bin/byacc
ln -sf yacc.1 $RPM_BUILD_ROOT/usr/man/man1/byacc.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/yacc
/usr/bin/byacc
/usr/man/man1/yacc.1
/usr/man/man1/byacc.1

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- correct Packager and Vendor
