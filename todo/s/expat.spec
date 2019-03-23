Summary       : Expat is an XML 1.0 parser written in C.
Name          : expat
Version       : 1.95.2
Release       : 1
Copyright     : MIT/X
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://expat.sourceforge.net/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://download.sourceforge.net/expat/expat-%{version}.tar.gz
Patch0: expat-1.95.2-mint.patch


%description
Expat is an XML 1.0 parser written in C by James Clark.  It aims to be
fully conforming. It is currently not a validating XML parser.


%prep
%setup -q
%patch0 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix}

make lib xmlwf


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc COPYING Changes MANIFEST README doc/reference.html doc/style.css
%{_prefix}/bin/*
%{_prefix}/include/*
%{_prefix}/lib/*


%changelog
* Mon Sep 24 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
