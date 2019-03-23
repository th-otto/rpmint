Summary: An uncompressor for .arj format archive files.
Name: unarj
Version: 2.41a
Release: 3
Group: Applications/Archiving
Copyright: distributable
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp://sunsite.unc.edu/pub/Linux/utils/compress/unarj241a.tar.gz
BuildRoot: /var/tmp/unarj-root

%description
The UNARJ program is used to uncompress .arj format archives.  The
.arj format archive was mostly used on DOS machines.

Install the unarj package if you need to uncompress .arj format
archives.

%prep
%setup -q -n unarj241a

%build
RPM_OPT_FLAGS="-g -O2 -fomit-frame-pointer"
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin

install -m 755 unarj $RPM_BUILD_ROOT/usr/bin
stack --fix=64k $RPM_BUILD_ROOT/usr/bin/unarj || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc unarj.doc
/usr/bin/unarj

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- correct Packager and Vendor
