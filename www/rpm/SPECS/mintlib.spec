%define pkgname mintlib

%rpmint_header

Summary:        Standard C Libraries for MiNT
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.60.1
Release:        3
License:        LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/mintlib
Source:         %{pkgname}-%{version}.tar.xz

Prefix:         %{_prefix}

%if "%{buildtype}" == "cross"
Provides:       cross-mint-%{pkgname}-headers = %{version}
%else
Provides:       %{pkgname}-headers = %{version}
%endif

BuildRequires:  cross-mint-gcc

%rpmint_build_arch

%description
This is the MiNTLib. The MiNTLib is the standard libc for FreeMiNT. It
will also work to some extent on non-MiNT systems, it tries its best to
emulate MiNT-calls on these systems.

On FreeMiNT systems the MiNTLib provides a programming interface that
is close to real *nix systems. It will either emulate system calls or
map them into GEMDOS- resp. FreeMiNT-calls.

These libraries are needed to develop programs which use the standard C
library.

%package -n timezone
Summary:        Time Zone Descriptions
License:        BSD-3-Clause
Group:          System/Base
# FIXME: needs rpm patch
# Version:        2018e

%description -n timezone
These are configuration files that describe available time zones. You
can select an appropriate time zone for your system running tzselect.


%prep
%setup -q -n %{pkgname}-%{version}

%build

%rpmint_cflags

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
export CROSS_TOOL=%{_rpmint_target}

#
# ugly hack until makefiles have been ajusted
#
sed -i "\@^# This is where include@i prefix := ${RPM_BUILD_ROOT}%{_rpmint_prefix}" configvars

make %{?_smp_mflags}

%install

export CROSS_TOOL=%{_rpmint_target}

%if "%{buildtype}" == "cross"
prefix=%{_rpmint_prefix}
%else
prefix=%{_rpmint_target_prefix}
%endif
make prefix=${RPM_BUILD_ROOT}${prefix} install

%if "%{buildtype}" == "cross"
rm -rf ${RPM_BUILD_ROOT}${prefix}/sbin
rm -rf ${RPM_BUILD_ROOT}${prefix}/share/zoneinfo
rm -rf ${RPM_BUILD_ROOT}${prefix}/share/man
%else
%rpmint_gzip_docs
%endif

#
# The Makefile in the include directory
# installs these files to /usr/include, but they don't belonge there
#
pushd ${RPM_BUILD_ROOT}
find . \( -name 00README \
	-o -name COPYING \
	-o -name COPYING.LIB \
	-o -name COPYMINT \
	-o -name BINFILES \
	-o -name MISCFILES \
	-o -name SRCFILES \
	-o -name EXTRAFILES \
	-o -name Makefile \
	-o -name clean-include \) -delete -printf "rm %%p\n"
popd

%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/*
%{_rpmint_libdir}
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/share/man
%{_rpmint_target_prefix}/lib
%endif

%if "%{buildtype}" != "cross"
%files -n timezone
# %config(missingok,noreplace) /etc/localtime
%{_rpmint_target_prefix}/share/zoneinfo
%{_rpmint_target_prefix}/sbin/*
%endif

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%changelog
* Sun Mar 5 2023 Thorsten Otto <admin@tho-otto.de>
- timezone update 2022g
- Install leapseconds data to %%{_datadir}/zoneinfo/; this is now
  required by some scientific applications.

* Mon Aug 31 2020 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Tue Jun 01 2010 Keith Scroggins <kws@radix.net>
- update to 0.59.1 stable release and enabled / added Coldfire libraries to the
- distribution also changed mintbin to require latest package build

* Wed Jan 13 2010 Alan Hourihane <alanh@fairlite.co.uk>
- update to 0.59.0 stable release

* Tue Apr 29 2008 Frank Naumann <fnaumann@freemint.de>
- updated to 0.58.0 stable release
  Please note: the libsocket is now integrated into the libc.

* Sat Dec 03 2005 Frank Naumann <fnaumann@freemint.de>
- updated to 0.57.6 stable release

* Wed Aug 04 2004 Frank Naumann <fnaumann@freemint.de>
- recompiled against gcc update

* Sun Jul 11 2004 Frank Naumann <fnaumann@freemint.de>
- updated to 0.57.5 stable release; this include all previous
  fixes and some enhancements in socket library; look into the
  ChangeLog for more details.

* Fri Jan 23 2004 Frank Naumann <fnaumann@freemint.de>
- updated to 0.57.4 stable release

* Fri Mar 14 2003 Frank Naumann <fnaumann@freemint.de>
- updated to 0.57.3 stable release

* Thu Aug 09 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.57 stable release

* Fri Mar 09 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 0.56.1 stable release

* Fri Dec 08 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 0.56 stable release

* Tue Jul 18 2000 Frank Naumann <fnaumann@freemint.de>
- replaced mfp based profiler support with system independant itimer method
  (stolen from glibc)
- fixed setitimer function
- fixed dsetkey binding

* Wed Jun 07 2000 Frank Naumann <fnaumann@freemint.de>
- added Slbopen/Slbclose systemcall bindings to mintbind.h
- added some small patches for <sys/stat.h>
- temporary fix for setsid() <-> ioctl(TIOCNOTTY) non working interaction

* Fri May 12 2000 Frank Naumann <fnaumann@freemint.de>
- corrected a typo that result in undefined references at linktime

* Wed May 10 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 0.55.3

* Fri Apr 28 2000 Frank Naumann <fnaumann@freemint.de>
- added small <sys/stat.h> patch: S_IFSOCK and S_ISSOCK definitions missing

* Tue Apr 18 2000 Frank Naumann <fnaumann@freemint.de>
- changed base type of time_t to long
- added stat -> Fxattr(nblocks) correction

* Fri Apr 14 2000 Guido Flohr <guido@freemint.de>
- Modified for 0.55
- Moved mshort libs into separate package to simplify removal.
- Crude support for a cross-lib rpm, try out if it works.

* Wed Mar 29 2000 Frank Naumann <fnaumann@freemint.de>
- lot of changes for the final 0.55 version, added all Conflicts

* Mon Feb 28 2000 Frank Naumann <fnaumann@freemint.de>
- changes related to gcc 2.95.2, removed libgcc2 stuff
- removed mbaserel libs
