Summary       : GNU Binary Utility Development Utilities
Summary(de)   : GNU Binary Utility Development Utilities
Summary(fr)   : Utilitaires de développement binaire de GNU
Summary(tr)   : GNU geliþtirme araçlarý
Name          : binutils
Version       : 2.21
Release       : 1
Copyright     : GPL
Group         : Development/Tools

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/binutils/

Prereq        : /sbin/install-info
Requires      : mintbin

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2
Patch0: binutils-2.21-mint-20101209.patch

%description
Binutils is a collection of binary utilities, including:
+ addr2line: converting addresses to file and line;
+ ar: creating modifying and extracting from archives;
+ nm: listing symbols from object files;
+ objcopy: copying and translating object files;
+ objdump: displaying information from object files;
+ ranlib: generating an index for the contents of an archive;
+ size: listing the section sizes of an object or archive file;
+ strings: listing printable strings from files;
+ strip: discarding symbols.

%package -n libiberty
Summary       : GNU libiberty and coding standards.
Group         : Development/Libraries
Prereq        : /sbin/install-info
Conflicts     : binutils <= 2.9.1-6

%description -n libiberty
The GNU libiberty and the info files for the GNU coding standards
and the FAQ for configure.

%prep
%setup -q
%patch0 -p1 -b .mint

%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -O -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--target=m68k-atari-mint \
	--disable-nls

make tooldir=%{_prefix} all info


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install install-info \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man \
	tooldir=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=256k ${RPM_BUILD_ROOT}%{_prefix}/bin/ar ||:

install -m 644 include/libiberty.h ${RPM_BUILD_ROOT}%{_prefix}/include

for i in bfd binutils gas gprof ld ; do
	if [ -f $i/README ]; then cp $i/README README.$i ; fi
	if [ -f $i/NEWS ]; then cp $i/NEWS NEWS.$i ; fi
done

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/info/*.info* ||:
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/as.info.gz || :
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/bfd.info.gz || :
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/binutils.info.gz || :
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/gprof.info.gz || :
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/ld.info.gz || :

%post -n libiberty
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/configure.info.gz || :
/sbin/install-info --info-dir=%{_prefix}/share/info %{_prefix}/share/info/standards.info.gz || :

%preun
if [ $1 = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/as.info.gz || :
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/bfd.info.gz || :
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/binutils.info.gz || :
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/gprof.info.gz || :
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/ld.info.gz || :
fi

%preun -n libiberty
if [ $1 = 0 ] ;then
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/configure.info.gz || :
  /sbin/install-info --delete --info-dir=%{_prefix}/share/info %{_prefix}/share/info/standards.info.gz || :
fi


%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README* NEWS*
%{_prefix}/bin/*
%{_prefix}/include/ansidecl.h
%{_prefix}/include/bfd.h
%{_prefix}/include/bfdlink.h
%{_prefix}/share/info/as.info*
%{_prefix}/share/info/bfd.info*
%{_prefix}/share/info/binutils.info*
%{_prefix}/share/info/gprof.info*
%{_prefix}/share/info/ld.info*
%{_prefix}/lib/ldscripts
%{_prefix}/lib/libbfd.a
%{_prefix}/lib/libbfd.la
%{_prefix}/lib/libopcodes.a
%{_prefix}/lib/libopcodes.la
%{_prefix}/share/man/man*/*

%files -n libiberty
%doc libiberty/COPYING.LIB libiberty/ChangeLog libiberty/README
%{_prefix}/include/libiberty.h
%{_prefix}/share/info/configure.info*
%{_prefix}/share/info/standards.info*
%{_prefix}/lib/libiberty.*

%changelog
* Mon Dec 13 2010 Keith Scroggins <kws@radix.net>
- Initial build of 2.21 version

* Sun May 23 2010 Keith Scroggins <kws@radix.net>
- Initial build of 2.20.1 version

* Fri Jan 08 2010 Keith Scroggins <kws@radix.net>
- Initial build of 2.20 version

* Sun Sep 04 2005 Mark Duckworth <mduckworth@atari-source.com>
- new release due to bugged mintlib

* Tue Aug 30 2005 Mark Duckworth <mduckworth@atari-source.com>
- updated to 2.16.1.
- credits go to all those for original work, and patrice for fixing this!

* Tue Feb 25 2003 Frank Naumann <fnaumann@freemint.de>
- updated to 2.13.2.1

* Tue Apr 05 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib

* Tue Mar 21 2000 Frank Naumann <fnaumann@freemint.de>
- added the gas <-> linker warning patch (from Guido)

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
