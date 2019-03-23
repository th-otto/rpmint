Summary:	File transfer utilities between Linux and PalmPilots
Name:		pilot-link
Version:	0.9.3
Release:	1

Source:		ftp://ryeham.ee.ryerson.ca/pub/PalmOS/pilot-link.%{version}.tar.bz2 
Patch0:		pilot-link-perl-install.patch.bz2
Patch1:		pilot-link-pixdir.patch.bz2
Patch2:		pilot-link.0.9.3.perl5.6.patch.bz2
Patch3:		pilot-link.0.9.3-mint.patch

Packager: 	Frank Naumann <fnaumann@freemint.de>
Vendor: 	Sparemint

Copyright:	GPL
Group:		Communications
BuildRoot:	/var/tmp/%{name}-root
Prefix: 	%{_prefix}
Requires:	perl

%description
This suite of tools allows you to upload and download programs and
data files between a Unix machine and the PalmPilot.  It has a
few extra utils that will allow for things like syncing the
PalmPilot's calendar app with Ical.  Note that you might still need to
consult the sources for pilot-link if you would like the Python, Tcl,
or Perl bindings.

Install pilot-link if you want to synchronize your Palm with your system.

%package devel
Requires:	pilot-link
Summary:	PalmPilot development header files
Group:		Development/C

%description devel
This package contains the development headers that are used to build
the pilot-link package.  It also includes the static libraries
necessary to build static pilot apps.

If you want to develop PalmPilot synchronizing applications, you'll
need to install pilot-link-devel.

%prep 
%setup -q -n pilot-link.%{PACKAGE_VERSION}
%patch0 -p1 -b .install
%patch1 -p1 -b .pixdir
%patch2 -p1 -b .perl
%patch3 -p1 -b .mint

%build
LIBS="-lsocket" \
CFLAGS="$RPM_OPT_FLAGS" \
LDFLAGS="-s" \
./configure \
	--prefix=$RPM_BUILD_ROOT/%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT

make install prefix=$RPM_BUILD_ROOT/%{_prefix}
mkdir $RPM_BUILD_ROOT/%{_prefix}/share
mv $RPM_BUILD_ROOT/%{_prefix}/man $RPM_BUILD_ROOT/%{_prefix}/share/
gzip -9nf $RPM_BUILD_ROOT/%{_prefix}/share/man/man*/*

strip $RPM_BUILD_ROOT/%{_prefix}/bin/* ||:
stack --fix=960k $RPM_BUILD_ROOT/%{_prefix}/bin/* ||:


#%#post -p /sbin/ldconfig

#%#postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING ChangeLog README TODO
# %{_prefix}/lib/libpisock.so.3.0.1
# %{_prefix}/lib/libpisock.so.3
%{_prefix}/lib/pilot-link/*
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*

%files devel
%defattr(-,root,root)
%{_prefix}/lib/libpicc.a
%{_prefix}/lib/libpisock.a
# %{_prefix}/lib/libpisock.so
# %{_prefix}/lib/libpisock.la
%{_prefix}/include/*

%changelog
* Wed Jun 21 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
