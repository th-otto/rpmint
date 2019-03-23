Summary		: A Concurrent Versioning system similar to but better than CVS.
Name		: subversion
Version		: 1.5.6
Release		: 1
License		: BSD
Group		: Utilities/System

Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
URL		: http://subversion.tigris.org

Prefix		: %{_prefix}
Docdir		: %{_prefix}/doc
BuildRoot	: %{_tmppath}/%{name}-root

Source0: subversion-%{version}.tar.bz2

%description
Subversion is a concurrent version control system which enables one or more
users to collaborate in developing and maintaining a hierarchy of files and
directories while keeping a history of all changes.  Subversion only stores
the differences between versions, instead of every complete file.  Subversion
also keeps a log of who, when, and why changes occurred.

As such it basically does the same thing CVS does (Concurrent Versioning System)
but has major enhancements compared to CVS and fixes a lot of the annoyances
that CVS users face.

%package devel
Group: Utilities/System
Summary: Development package for Subversion developers.
%description devel
The subversion-devel package includes the static libraries and include files
for developers interacting with the subversion package.

%prep
%setup -q

%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} --disable-shared --enable-all-static \
	--disable-mod-activation --disable-neon-version-check \
	--with-ssl --with-apr=%{_prefix} --with-apr-util=%{_prefix}

make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:

strip ${RPM_BUILD_ROOT}%{_bindir}/svn
strip ${RPM_BUILD_ROOT}%{_bindir}/svnadmin
strip ${RPM_BUILD_ROOT}%{_bindir}/svndumpfilter
strip ${RPM_BUILD_ROOT}%{_bindir}/svnlook
strip ${RPM_BUILD_ROOT}%{_bindir}/svnserve
strip ${RPM_BUILD_ROOT}%{_bindir}/svnsync
strip ${RPM_BUILD_ROOT}%{_bindir}/svnversion

stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svn
stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svnadmin
stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svndumpfilter
stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svnlook
stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svnserve
stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svnsync
stack -S 256k ${RPM_BUILD_ROOT}%{_bindir}/svnversion

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc BUGS CHANGES COMMITTERS COPYING HACKING INSTALL README
%doc subversion/LICENSE
%{_bindir}/svn
%{_bindir}/svnadmin
%{_bindir}/svndumpfilter
%{_bindir}/svnlook
%{_bindir}/svnserve
%{_bindir}/svnsync
%{_bindir}/svnversion
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
%{_libdir}/libsvn*.a
%{_libdir}/libsvn*.la
/usr/include/subversion-1


%changelog
* Sat Mar 14 2008 Keith Scroggins <kws@radix.net>
- Updated to latest version

* Wed Jan 09 2008 Keith Scroggins <kws@radix.net>
- Initial build for MiNT
