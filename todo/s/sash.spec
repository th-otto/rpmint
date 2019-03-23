Summary       : A stand-alone shell with built-in commands
Name          : sash
Version       : 3.6
Release       : 1
Copyright     : FSR, Other License(s), see package
Group         : System/Shells

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://www.tip.net.au/~dbell/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.tip.net.au/~dbell/programs/%{name}-%{version}.tar.gz
Patch0: sash-3.6-mint.patch	


%description
A very simple stand alone shell with built in commands.

This package includes:

-chgrp, -chmod, -chown, -cmp, -cp, -dd, -echo,
-ed, -grep, -gunzip, -gzip, -kill, -ln, -ls, -mkdir,
-mknod, -more, -mount, -mv, -printenv, -pwd, -rm,
-rmdir, -sync, -tar, -touch, -umount, -where

Authors:
--------
    David I. Bell <dbell@canb.auug.org.au>


%prep
%setup -q
%patch0 -p1


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -m 755 ${RPM_BUILD_ROOT}
mkdir -m 755 ${RPM_BUILD_ROOT}/usr
mkdir -m 755 ${RPM_BUILD_ROOT}/usr/bin
mkdir -m 755 ${RPM_BUILD_ROOT}/usr/share
mkdir -m 755 ${RPM_BUILD_ROOT}/usr/share/man
mkdir -m 755 ${RPM_BUILD_ROOT}/usr/share/man/man1

make install \
	DESTDIR=${RPM_BUILD_ROOT} \
	MANDIR=/usr/share/man/man1

chmod 755 ${RPM_BUILD_ROOT}/usr/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc README
%{_prefix}/bin/sash
%{_prefix}/share/man/man*/*


%changelog
* Tue Jan 13 2004 Frank Naumann <fnaumann@freemint.de>
- corrected specfile for Sparemint

* Tue Jan 06 2004 Keith Scroggins <kws@radix.net>
- Initial build for MiNT
