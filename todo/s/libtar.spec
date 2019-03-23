Summary       : libtar - C library for manipulating tar files
Name          : libtar
Version       : 1.2.3
Release       : 1
Copyright     : BSD
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www-dev.cso.uiuc.edu/libtar/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp-dev.cso.uiuc.edu/pub/libtar/libtar-%{version}.tar.gz


%description
libtar is a library for manipulating tar files from within C programs.
Here are some of its features:

  * Handles both POSIX tar file format and the GNU extensions.
  * API provides functions for easy use, such as tar_extract_all().
  * Also provides functions for more granular use, such as 
    tar_append_regfile().


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc COPYRIGHT ChangeLog* README TODO
%{_prefix}/include/*.h
%{_prefix}/lib/lib*.a
%{_prefix}/share/man/*/*


%changelog
* Wed Jun 27 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
