Name		: libtool
Version		: 2.2.8
Release		: 1
Copyright	: GPL
Group		: Development/Tools
Summary		: The GNU libtool, which simplifies the use of shared libraries.
Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
Source		: ftp://ftp.gnu.org/pub/gnu/libtool/libtool-%{version}.tar.bz2
Prefix		: %{_prefix}
PreReq		: /sbin/install-info
Requires	: automake
BuildRoot	: /var/tmp/%{name}-root

%description
The libtool package contains the GNU libtool, a set of shell scripts
which automatically configure UNIX and UNIX-like architectures to
generically build shared libraries. Libtool provides a consistent,
portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, you
should install libtool.
%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure --prefix=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install
gzip -9 ${RPM_BUILD_ROOT}%{_prefix}/share/info/*.info*
gzip -9 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_prefix}/share/info/libtool.info.gz %{_prefix}/share/info/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_prefix}/share/info/libtool.info.gz %{_prefix}/share/info/dir
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%doc THANKS TODO ChangeLog
%{_prefix}/bin/*
%{_prefix}/include/*
%{_prefix}/lib/*
%{_prefix}/share/info/libtool.info*
%{_prefix}/share/man/man1/*
%{_prefix}/share/libtool/*
%{_prefix}/share/aclocal/*

%changelog
* Fri Aug 20 2010 Keith Scroggins <kws@radix.net>
- Updated to 2.2.8

* Thu Aug 25 2004 Jens Syckor <js712688@inf.tu-dresden.de>
- Updated to version 1.4.3.

* Sun Jul 19 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Added requirement for automake.

* Sun Jul 18 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Updated to version 1.3.3.
- Added German translations.
