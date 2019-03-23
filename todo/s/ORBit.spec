Summary       : A high-performance CORBA Object Request Broker.
Name          : ORBit
Version       : 0.5.7
Release       : 1
License       : LGPL/GPL
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.labs.redhat.com/orbit/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.labs.redhat.com/pub/ORBit/%{name}-%{version}.tar.gz


%description
ORBit is a high-performance CORBA (Common Object Request Broker 
Architecture) ORB (object request broker). It allows programs to 
send requests and receive replies from other programs, regardless 
of the locations of the two programs. CORBA is an architecture that 
enables communication between program objects, regardless of the 
programming language they're written in or the operating system they
run on.

You will need to install this package and ORBIT-devel if you want to 
write programs that use CORBA technology.

%package devel
Summary       : Development libraries, header files and utilities for ORBit.
Group         : Development/Libraries
Requires      : ORBit = %{version}
Requires      : glib indent

%description devel
ORBit is a high-performance CORBA (Common Object Request Broker
Architecture) ORB (object request broker) with support for the 
C language.

This package contains the header files, libraries and utilities 
necessary to write programs that use CORBA technology. If you want to
write such programs, you'll also need to install the ORBIT package.


%prep
%setup -q
for I in . popt libIDL; do
	(cd $I; aclocal
	libtoolize --force
	automake
	autoconf
	autoheader)
done


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*


%post devel
/sbin/install-info %{_prefix}/info/libIDL.info.gz %{_prefix}/info/dir

%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/libIDL.info.gz %{_prefix}/info/dir
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)

%doc AUTHORS COPYING ChangeLog NEWS README TODO
%doc -P libIDL/COPYING libIDL/ChangeLog libIDL/AUTHORS
%doc -P libIDL/README* libIDL/NEWS libIDL/BUGS libIDL/tstidl.c

%{_prefix}/bin/orbit-event-server
%{_prefix}/bin/orbit-name-server
%{_prefix}/bin/name-client
%{_prefix}/bin/orbit-ird


%files devel
%defattr(-,root,root)
%{_prefix}/bin/orbit-idl
%{_prefix}/bin/orbit-config
%{_prefix}/bin/libIDL-config
%{_prefix}/include/*
%{_prefix}/info/libIDL.info.gz
%{_prefix}/lib/*.sh
%{_prefix}/lib/lib*.a
%{_prefix}/share/aclocal/*


%changelog
* Fri Jan 05 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
