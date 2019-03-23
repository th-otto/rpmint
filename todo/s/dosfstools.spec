Summary       : FAT/FAT32/VFAT filesystem checker
Name          : dosfstools
Version       : 2.10
Release       : 1
Copyright     : GPL
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.uni-erlangen.de/pub/Linux/LOCAL/dosfstools/%{name}-%{version}.tar.gz
Patch0: dosfstools-2.10-mint.patch


%description
Utility to check and repair FAT based filesystems. Includes support for
FAT32 and VFAT long filenames.


%prep
%setup -q
%patch0 -p1 -b .mint


%build
cd dosfsck
make CFLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd dosfsck
make install \
	SBINDIR=${RPM_BUILD_ROOT}/sbin \
	MANDIR=${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/* ||:

# correct symbolic links
( cd ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8;
  for file in *.8; do \
    echo "processing $file ..."; \
    target=`readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)

strip ${RPM_BUILD_ROOT}/sbin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}/sbin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files 
%defattr(-,root,root)
%doc CHANGES README.Atari dosfsck/README dosfsck/COPYING
/sbin/*
%{_prefix}/share/man/*/*


%changelog
* Tue Sep 30 2003 Frank Naumann <fnaumann@freemint.de>
- updated to 2.10
- much better memory management (around 33% reduced memory consumption)

* Thu Feb 15 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
