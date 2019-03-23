Summary       : A file compression utility.
Name          : bzip2
Version       : 1.0.6
Release       : 1
License       : BSD
Group         : Applications/Archiving

Packager      : Thorsten Otto <admin@tho-otto.de>
Vendor        : RPMint
URL           : http://www.bzip.org/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz
Patch0:  bzip2-1.0.6-patch-0001-configure.patch
Patch1:  bzip2-1.0.6-patch-0002-cygming.patch
Patch2:  bzip2-1.0.6-patch-0003-debian-bzgrep.patch
Patch3:  bzip2-1.0.6-patch-0004-unsafe-strcpy.patch
Patch4:  bzip2-1.0.6-patch-0005-progress.patch
Patch5:  bzip2-1.0.6-patch-0006-mint.patch


%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities 
of the best techniques available.  However, bzip2 has the added benefit 
of being approximately two times faster at compression and six times 
faster at decompression than those techniques.  Bzip2 is not the 
fastest compression utility, but it does strike a balance between speed 
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary       : Header files and libraries for developing apps which will use bzip2.
Group         : Development/Libraries
Requires      : bzip2 = %{version}

%description devel
Header files and a static library of bzip2 functions, for developing apps
which will use the library.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1


%build
rm -f aclocal.m4 ltmain.sh
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --add-missing || exit 1

TARGET=m68k-atari-mint
CFLAGS="-O2 -fomit-frame-pointer" \
LDFLAGS="-Wl,-stack,360k -s" \
export PKG_CONFIG_LIBDIR="%{_prefix}/$TARGET/lib/pkgconfig"
export PKG_CONFIG_PATH="$PKG_CONFIG_LIBDIR"
./configure \
	--host=$TARGET \
	--prefix=%{_prefix} \
	--mandir=%{_prefix}/share/man \
	--docdir=%{_prefix}/share/doc \
	--enable-static
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

rm -f ${RPM_BUILD_ROOT}%{_prefix}/lib/*.la

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc LICENSE README README.COMPILATION.PROBLEMS README.XML.STUFF CHANGES ChangeLog manual.html
%{_prefix}/bin/*
%{_prefix}/share/man/*/*

%files devel
%defattr(-,root,root)
%{_prefix}/include/*
%{_prefix}/lib/lib*.a
%{_prefix}/lib/pkgconfig/*.pc


%changelog
* Jan 26  7 2018 Thorsten Otto <admin@tho-otto.de>
- updated to 1.0.6
- updated Packager and Vendor

* Fri Feb  7 2003 Adam Klobukowski <atari@gabo.pl>
- updated to 1.0.2

* Mon Dec 25 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 1.0.1; seperated developer files

* Sun Mar 26 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55
- updated to 0.9.5d

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
