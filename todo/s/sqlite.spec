%define name sqlite
%define version 3.2.2
%define release 1

Name: %{name}
Summary: SQLite is a C library that implements an embeddable SQL database engine
Version: %{version}
Release: %{release}
Source: %{name}-%{version}.tar.gz
Group: System/Libraries
URL: http://www.hwaci.com/sw/sqlite/
License: Public Domain
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description
SQLite is a C library that implements an embeddable SQL database engine.
Programs that link with the SQLite library can have SQL database access
without running a separate RDBMS process. The distribution comes with a
standalone command-line access program (sqlite) that can be used to
administer an SQLite database and which serves as an example of how to
use the SQLite library.

%package -n %{name}-devel
Summary: Header files and libraries for developing apps which will use sqlite
Group: Development/C
Requires: %{name} = %{version}-%{release}

%description -n %{name}-devel
The sqlite-devel package contains the header files and libraries needed
to develop programs that use the sqlite database library.

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="%optflags -DNDEBUG=1" CXXFLAGS="%optflags -DNDEBUG=1" ./configure --prefix=%{_prefix} --enable-static --disable-shared --disable-tcl

make

%install
install -d $RPM_BUILD_ROOT/%{_prefix}
install -d $RPM_BUILD_ROOT/%{_prefix}/bin
install -d $RPM_BUILD_ROOT/%{_prefix}/include
install -d $RPM_BUILD_ROOT/%{_prefix}/lib
make install prefix=$RPM_BUILD_ROOT/%{_prefix}

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}/*

%files -n %{name}-devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/sqlite3.pc
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
