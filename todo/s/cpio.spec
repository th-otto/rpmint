Summary: A GNU archiving program.
Name: cpio
Version: 2.4.2
Release: 3
Copyright: GPL
Group: Applications/Archiving
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp://prep.ai.mit.edu/pub/gnu/cpio-2.4.2.tar.gz
Patch0: cpio-2.3-lstat.patch
Patch1: cpio-2.4.2-glibc.patch
Patch2: cpio-2.4.2-mtime.patch
Patch3: cpio-2.4.2-svr4compat.patch
Patch4: cpio-2.4.2-glibc21.patch
Patch5: cpio-2.4.2-longlongdev.patch
#Prereq: /sbin/install-info /sbin/rmt
Prereq: /sbin/install-info
Buildroot: /var/tmp/cpio-root

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
# patch 0 not applied
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .svr4compat
%patch4 -p1 -b .glibc21
%patch5 -p1 -b .longlongdev

%build
./configure --prefix=/usr --bindir=/bin --libexecdir=/sbin
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/usr bindir=$RPM_BUILD_ROOT/bin libexecdir=$RPM_BUILD_ROOT/sbin install
stack --fix=64k $RPM_BUILD_ROOT/bin/cpio || :
gzip -9nf $RPM_BUILD_ROOT/usr/info/cpio.*
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/cpio.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/cpio.info.gz /usr/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete /usr/info/cpio.info.gz /usr/info/dir
fi

%files
%doc README NEWS
/bin/cpio
#/bin/mt
/usr/info/cpio.*
/usr/man/man1/cpio.1.gz

%changelog
* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
