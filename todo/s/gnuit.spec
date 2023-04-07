Name: 		git
Summary: 	A set of GNU Interactive Tools.
Version: 	4.3.20
Release: 	1
License:	GPL
Group: 		Applications/File
Packager:	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
Source: 	ftp://ftp.gnu.org:/pub/gnu/git/git-%{version}.tar.gz
Patch0:		git-4.3.20-mint-config.patch
URL: 		http://www.cs.unh.edu/~tudor
BuildRoot:	/var/tmp/git-root
Prereq: 	/sbin/install-info
Requires:	texinfo texi2html

%description
GIT (GNU Interactive Tools) provides an extensible file system browser,
an ASCII/hexadecimal file viewer, a process viewer/killer and other
related utilities and shell scripts.  GIT can be used to increase the
speed and efficiency of copying and moving files and directories, invoking
editors, compressing and uncompressing files, creating and expanding
archives, compiling programs, sending mail and more.  GIT uses standard
ANSI color sequences, if they are available.

You should install the git package if you are interested in using its file
management capabilities.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr 
make

%install
make prefix=$RPM_BUILD_ROOT/usr/ install-strip
gzip -9nf $RPM_BUILD_ROOT/usr/info/git.info*

%files
%doc COPYING ChangeLog LSM NEWS PLATFORMS PROBLEMS README INSTALL doc/git.html
/usr/bin/*
/usr/bin/.gitaction
/usr/man/man1/*
/usr/info/git*
/usr/share/git/.gitrc*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /usr/info/git.info.gz /usr/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete /usr/info/git.info.gz /usr/info/dir
fi

%changelog
* Fri Feb 5 2004 Keith Scroggins <kws@radix.net>
- Initial build of git (GNU Interactive Tools) for MiNT
