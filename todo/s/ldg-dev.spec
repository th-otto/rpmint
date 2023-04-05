# LDG-dev specfile

Summary       : LDG development library and header file
Name          : ldg-dev
Version       : 2.33
Release       : 2
Copyright     : LGPL
Group         : Development/Libraries

Packager      : Arnaud Bercegeay <arnaud.bercegeay@free.fr>
Vendor        : Sparemint
URL           : http://ldg.sf.net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz
Patch0: ldg-cpu.patch

%description
Contains the LDG library and header file required to build a LDG
library, or an application that use LDG libraries.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .cpu

%build
cd src/devel
make -f gcc.mak
make -f gcc020-60.mak
#make -f gcc5475.mak

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60
#mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475
cd lib/gcc
install -m 644 libldg.a ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 m68020-60/libldg.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60
#install -m 644 m5475/libldg.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475
cd ../../include
install -m 644 ldg.h ${RPM_BUILD_ROOT}%{_prefix}/include


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
#%doc gemlib/ChangeLog*
%{_prefix}/lib/lib*.a
%{_prefix}/lib/m68020-60/lib*.a
#%{_prefix}/lib/m5475/lib*.a
%{_prefix}/include/*.h


%changelog
* Tue Aug 17 2010 Keith Scroggins <kws@radix.net>
- Added 68020-60 library and support for Coldfire, but some assembly needs to
- be patched for the Coldfire build.

* Wed Nov 02 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- Initial version of the ldg-dev package
