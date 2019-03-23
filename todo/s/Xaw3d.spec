Summary       : A version of the MIT Athena widget set for X.
Summary(de)   : 3D-Version des MIT Athena-Widgetsatzes fuer X
Name          : Xaw3d
Version       : 1.5
Release       : 2
Copyright     : MIT
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.x.org/contrib/widgets/Xaw3d/

BuildRequires : XFree86-devel
Requires      : XFree86-devel
Prereq        : fileutils

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.x.org/contrib/widgets/Xaw3d/R6.3/%{name}-%{version}.tar.gz
Patch0: Xaw3d-1.1-shlib.patch
Patch1: Xaw3d-1.3-glibc.patch
Patch2: xaw3d.patch
Patch3: Xaw3d-1.3-static.patch
Patch4: Xaw3d-ia64.patch


%description
Xaw3d is an enhanced version of the MIT Athena Widget set for
the X Window System.  Xaw3d adds a three-dimensional look to applications
with minimal or no source code changes.

You should install Xaw3d-devel if you are going to develop applications
using the Xaw3d widget set.

%description -l de
Xaw3d ist eine verbesserte Version des MIT Athena-Widgetsatzes für X.
Xaw3d gibt Programmen einen 3D-Look, ohne, daß der Source verändert werden
muß.

Sie sollten Xaw3d-devel installieren, falls Sie Xaw3d-Anwendungen
entwickeln wollen.


%prep
%setup -q -c
cd xc/lib/Xaw3d
%patch0 -p0
ln -s .. X11
%patch1 -p4
%patch2 -p4
%patch3 -p0
%patch4 -p4


%build
cd xc/lib/Xaw3d
xmkmf
make CDEBUGFLAGS="${RPM_OPT_FLAGS}" CXXDEBUGFLAGS="${RPM_OPT_FLAGS} -O"


%install
rm -rf ${RPM_BUILD_ROOT}

cd xc/lib/Xaw3d
make install DESTDIR=${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/X11R6/include/X11


%clean
rm -rf ${RPM_BUILD_ROOT}


%post
if [ ! -d %{_prefix}/X11R6/include/X11/Xaw3d ] ; then
	rm -f %{_prefix}/X11R6/include/X11/Xaw3d
	ln -sf ../Xaw3d %{_prefix}/X11R6/include/X11
fi


%files
%defattr(-,root,root)
%{_prefix}/X11R6/lib/*.a
%{_prefix}/X11R6/include/X11/Xaw3d


%changelog
* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
