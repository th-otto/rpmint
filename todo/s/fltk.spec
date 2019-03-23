Summary       : Fast Light Tool Kit (FLTK)
Name          : fltk
Version       : 1.0.11
Release       : 1
Copyright     : LGPL
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.fltk.org

Requires      : XFree86
BuildRequires : XFree86-devel

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.fltk.org/pub/fltk/%{version}/fltk-%{version}-source.tar.gz


%description
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

%package devel
Summary       : Fast Light Tool Kit (FLTK) - development environment
Group         : Development/Libraries
Requires      : XFree86-devel

%description devel
The Fast Light Tool Kit ("FLTK", pronounced "fulltick") is a LGPL'd
C++ graphical user interface toolkit for X (UNIX(r)), OpenGL(r),
and Microsoft(r) Windows(r) NT 4.0, 95, or 98. It was originally
developed by Mr. Bill Spitzak and is currently maintained by a
small group of developers across the world with a central
repository in the US.

Install fltk-devel if you need to develop FLTK applications.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
CXXFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--disable-shared

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}
make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,root)
%doc CHANGES COPYING README
%{_prefix}/bin/fluid
%{_prefix}/include/FL
%{_prefix}/include/Fl
%{_prefix}/lib/libfltk*.a
%{_prefix}/share/doc/fltk/*
%{_prefix}/share/man/man*/*


%changelog
* Thu May 31 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
