Summary       : A Clone of the ndbm library
Name          : sdbm
Version       : 1.0.2
Release       : 1
Copyright     : GPL
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.ohse.de/uwe/releases/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.ohse.de/uwe/releases/sdbm-1.0.2.tar.gz


%description 
A Clone of the ndbm library


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc README.uo CHANGES
%{_prefix}/include/*.h
%{_prefix}/lib/libsdbm.a
%{_prefix}/share/man/*/*


%changelog
* Tue Jan 30 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
