# Gemlib specfile

# Please note this file is maintained in the freemint CVS repository as
# "lib/gemlib/gemlib.spec.in". Most current version is avaible there and
# any modification should be stored there.

Summary       : GEM libraries and header files
Name          : gemlib
Version       : 0.43.6
Release       : 1
Copyright     : Public Domain
Group         : Development/Libraries

Packager      : Arnaud Bercegeay <arnaud.bercegeay@free.fr>
Vendor        : Sparemint
URL           : http://arnaud.bercegeay.free.fr/gemlib/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz


%description
Contains the standard libraries and header files to develop your own GEM
applications.

Attention, starting from version 0.40.0 the gemlib is heavily modernized
and updated. There are incompatible changes that require modifications
of programs that use this lib too.

Package version numbering has been modified to the one used by the
library itself. Please use the --oldpackage option if upgrading from a
0.40.0 or older gemlib and rpm complains about installed package being
newer than this one.


%prep
%setup -q -n %{name}-%{version}


%build
cd gemlib
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd gemlib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 libgem.a ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 libgem16.a ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 gem.h ${RPM_BUILD_ROOT}%{_prefix}/include
install -m 644 gemx.h ${RPM_BUILD_ROOT}%{_prefix}/include
install -m 644 mt_gem.h ${RPM_BUILD_ROOT}%{_prefix}/include
install -m 644 mt_gemx.h ${RPM_BUILD_ROOT}%{_prefix}/include

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/GEM/include
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/GEM/lib
ln -s %{_prefix}/lib/libgem.a ${RPM_BUILD_ROOT}%{_prefix}/GEM/lib/
ln -s %{_prefix}/lib/libgem16.a ${RPM_BUILD_ROOT}%{_prefix}/GEM/lib/
ln -s %{_prefix}/include/gem.h ${RPM_BUILD_ROOT}%{_prefix}/GEM/include/
ln -s %{_prefix}/include/gemx.h ${RPM_BUILD_ROOT}%{_prefix}/GEM/include/
ln -s %{_prefix}/include/mt_gem.h ${RPM_BUILD_ROOT}%{_prefix}/GEM/include/
ln -s %{_prefix}/include/mt_gemx.h ${RPM_BUILD_ROOT}%{_prefix}/GEM/include/


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc gemlib/ChangeLog*
%{_prefix}/lib/lib*.a
%{_prefix}/include/*.h
%{_prefix}/GEM/lib/lib*.a
%{_prefix}/GEM/include/*.h


%changelog
* Mon Dec 19 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.6

* Mon Oct  3 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.5

* Fri Apr  1 2005 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.4

* Wed Nov  3 2004 Arnaud Bercegeay <arnaud.bercegeay@free.fr>
- updated to version 0.43.3

* Mon Jan  5 2004 Standa Opichal <opichals@seznam.cz>
- updated to version 0.43.1

* Tue Oct 21 2003 Standa Opichal <opichals@seznam.cz>
- version 0.43.0 - new generation gemlib

* Sun Feb 16 2003 Standa Opichal <opichals@seznam.cz>
- updated to version 0.42.99, betaversion of new generation gemlib

* Mon Jul 15 2002 Xavier Joubert <xavier.joubert@free.fr>
- updated to version 0.42.2, modified version numbering

* Thu Feb 27 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 0.40.0

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 11 1999 Guido Flohr <guido@freemint.de>
- Changed vendor to Sparemint
