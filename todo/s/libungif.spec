Summary       : A library for manipulating GIF format image files.
Name          : libungif
Version       : 4.1.0
Release       : 1
Copyright     : X Consortium-like
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://prtr-13.ucsc.edu/~badger/software/libungif/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source: ftp://prtr-13.ucsc.edu/pub/libungif/%{name}-%{version}b1.tar.gz
Patch0: libungif-4.1.0-stdarg.patch
Patch1: libungif-4.1.0b1-mintconf.patch


%description
The libungif package contains a shared library of functions for
loading and saving GIF format image files.  The libungif library can
load any GIF file, but it will save GIFs only in uncompressed format
(i.e., it won't use the patented LZW compression used to save "normal"
compressed GIF files).

Install the libungif package if you need to manipulate GIF files.  You
should also install the libungif-progs package.

%package devel
Summary       : Development tools for programs which will use the libungif library.
Group         : Development/Libraries
#Requires      : %{name} = %{version}

%description devel
This package contains the static libraries, header files and
documentation necessary for development of programs that will use the
libungif library to load and save GIF format image files.

You should install this package if you need to develop programs which
will use libungif library functions.
#You'll also need to install the libungif package.

%package progs
Summary       : Programs for manipulating GIF format image files.
Group         : Applications/Multimedia
#Requires      : %{name} = %{version}

%description progs
The libungif-progs package contains various programs for manipulating
GIF format image files.
#
#Install this package if you need to manipulate GIF format image files.
#You'll also need to install the libungif package.


%prep
%setup -q -n %{name}-%{version}b1
%patch0 -p1 -b .stdarg
%patch1 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS}" CXXFLAGS="${RPM_OPT_FLAGS} -O" \
./configure \
	--prefix=%{_prefix}
make all LIBS=-lsocket


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}
ln -sf libungif.a ${RPM_BUILD_ROOT}%{_prefix}/lib/libgif.a

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

chmod 644 ${RPM_BUILD_ROOT}%{_prefix}/lib/lib*.a
chmod 644 COPYING README UNCOMPRESSED_GIF NEWS ONEWS
chmod 644 doc/* util/giffiltr.c util/gifspnge.c


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,root)
%doc COPYING README UNCOMPRESSED_GIF NEWS ONEWS
%doc doc/* util/giffiltr.c util/gifspnge.c
%{_prefix}/include/*.h
%{_prefix}/lib/lib*.a
%{_prefix}/lib/lib*.la

%files progs
%defattr(-,root,root)
%{_prefix}/bin/*


%changelog
* Sun Dec 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
