Summary: A perfect hash function generator.
Name: gperf
Version: 2.7
Release: 1
Copyright: GPL
Group: Development/Tools
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp://prep.ai.mit.edu/pub/gnu/gperf-2.7.tar.gz
Patch0: gperf-2.7-egcs.patch
Prereq: /sbin/install-info
BuildRoot: /var/tmp/gperf-root

%description
Gperf is a perfect hash function generator written in C++.  Simply
stated, a perfect hash function is a hash function and a data structure
that allows recognition of a key word in a set of words using exactly
one probe into the data structure.

Install gperf if you need a program that generates perfect hash functions.

%prep
%setup -q
%patch0 -p1 -b .egcs

%build
CC=gcc CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=/usr
make LIBS="../lib/libgp.a -lm"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr

make prefix=$RPM_BUILD_ROOT/usr install

gzip -9nf $RPM_BUILD_ROOT/usr/info/gperf.info*
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/gperf.1
rm -rf $RPM_BUILD_ROOT/usr/man/{dvi,html}
strip $RPM_BUILD_ROOT/usr/bin/gperf
stack --fix=512k $RPM_BUILD_ROOT/usr/bin/gperf || :

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/gperf.info.gz /usr/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete /usr/info/gperf.info.gz /usr/info/dir
fi

%files
%defattr(-,root,root)
%doc README NEWS doc/gperf.html
/usr/bin/gperf
/usr/man/man1/gperf.1.gz
/usr/info/gperf.info*

%changelog
* Sun Feb 13 2000 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- first release for Sparemint
