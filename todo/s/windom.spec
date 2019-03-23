# windom-dev specfile

Summary       : WinDom development library and header file
Name          : windom
Version       : 2.0.0
Release       : 1
Copyright     : LGPL
Group         : Development/Libraries

Packager      : Arnaud Bercegeay <arnaud.bercegeay@free.fr>
Vendor        : Sparemint
URL           : http://windom.sf.net

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz


%description
Contains the WINDOM library and header file.

%prep
%setup -q -n %{name}-%{version}


%build
cd src
make -f gcc.mak


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include/windom
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
cd lib/gcc
install -m 644 libwindom.a ${RPM_BUILD_ROOT}%{_prefix}/lib
cd ../../include
install -m 644 windom.h ${RPM_BUILD_ROOT}%{_prefix}/include
install -m 644 mt_wndm.h ${RPM_BUILD_ROOT}%{_prefix}/include
cd windom
install -m 644 list.h ${RPM_BUILD_ROOT}%{_prefix}/include/windom
install -m 644 udlib.h ${RPM_BUILD_ROOT}%{_prefix}/include/windom


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
#%doc gemlib/ChangeLog*
%{_prefix}/lib/libwindom.a
%{_prefix}/include/*.h
%{_prefix}/include/windom/*.h


%changelog
* Mon Feb 20 2006 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated for windom 2.0.0-1

* Tue Feb 14 2006 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated for windom 2.0.0-RC2

* Tue Dec 20 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- Initial version of the windom package for windom 2.0.0-RC1
