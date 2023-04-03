%define pkgname chkconfig

%rpmint_header

%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        1.0.7
Release:        3
Summary:        A system tool for maintaining the /etc/rc.d hierarchy.
License:        GPL-2.0-or-later
Group:          System/Base
Source:         ftp://ftp.redhat.com/pub/redhat/code/chkconfig/chkconfig-%{version}.tar.gz
Patch0:         patches/%{pkgname}/chkconfig-nommap.patch
Patch1:         patches/%{pkgname}/chkconfig-mint.patch

BuildRequires:  gettext-runtime
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gettext-devel
BuildRequires:  cross-mint-newt-devel
BuildRequires:  cross-mint-popt-devel
%else
BuildRequires:  gettext-devel
BuildRequires:  newt-devel
BuildRequires:  popt-devel
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%rpmint_build_arch

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc.d, so system administrators don't have to
manually edit the symbolic links as often.

%package -n ntsysv
Summary: A system tool for maintaining the /etc/rc.d hierarchy.
Group: System Environment/Base

%description -n ntsysv
ntsysv updates and queries runlevel information for system
services.  ntsysv relieves system administrators of having to
directly manipulate the numerous symbolic links in /etc/rc.d.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	make CC="%{_rpmint_target}-gcc $CPU_CFLAGS" CFLAGS="-O2 -fomit-frame-pointer"

	# compress manpages
	%rpmint_gzip_docs
done

%install

make instroot=%{buildroot}%{_isysroot} MANDIR=/usr/share/man install

mkdir -p %{buildroot}%{_isysroot}/etc/rc.d/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p %{buildroot}%{_isysroot}/etc/rc.d/rc${n}.d
done
gzip -9nf %{buildroot}%{_isysroot}/usr/share/man/man8/*.8

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if "%{buildtype}" != "cross"
%post
%{_sbindir}/update-alternatives \
  --install /bin/ksh ksh %{_bindir}/lksh 15 \
  --slave %{_rpmint_target_prefix}/bin/ksh usr-bin-ksh %{_rpmint_target_prefix}/bin/lksh \
  --slave %{_rpmint_target_prefix}/share/man/man1/ksh.1%{?ext_man} ksh.1%{?ext_man} %{_rpmint_target_prefix}/share/man/man1/lksh.1%{?ext_man}

%preun
if test $1 -eq 0 ; then
    %{_sbindir}/update-alternatives --remove ksh /bin/lksh
fi

%postun
test -x %{_bindir}/mksh && awk '
($1 != "/bin/mksh") && ($1 != "%{_bindir}/mksh") {
    line[n++] = $0
}
END {
    for (i = 0; i < n; i++) {
        print line[i] >"%{_sysconfdir}/shells"
    }
}' '%{_sysconfdir}/shells' || true
%endif

%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_sysroot}/sbin
%{_rpmint_sysroot}%{_rpmint_target_prefix}/sbin
%{_rpmint_datadir}
%else
/etc/rc.d/*
/sbin
%{_rpmint_target_prefix}/sbin
%{_rpmint_target_prefix}/share
%ghost /etc/alternatives/ksh
%ghost /etc/alternatives/usr-bin-ksh
%ghost /etc/alternatives/ksh.1%{?ext_man}
%endif

%changelog
* Sun Mar 19 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Sun Dec 26 1999 Guido Flohr <guido@atari.org>
- Built against fixed libnewt to support monochrome terminals.

* Tue Dec 14 1999 Guido Flohr <guido@atari.org>
- Rebuild against MiNTLib 0.54.1c.
- Changed manpath to /usr/share/man.

* Sun Sep 19 1999 Guido Flohr <guido@atari.org>
- Initial release for Sparemint.

* Mon Aug 23 1999 Jeff Johnson <jbj@redhat.com>
- don't use strchr to skip unwanted files, look at extension instead (#4166).

* Thu Aug  5 1999 Bill Nottingham <notting@redhat.com>
- fix --help, --verson

* Mon Aug  2 1999 Matt Wilson <msw@redhat.com>
- rebuilt ntsysv against newt 0.50

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- fix i18n problem in usage message (#4233).
- add --help and --version.

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- release for Red Hat 6.0

* Thu Apr  8 1999 Matt Wilson <msw@redhat.com>
- added support for a "hide: true" tag in initscripts that will make
  services not appear in ntsysv when run with the "--hide" flag

* Thu Apr  1 1999 Matt Wilson <msw@redhat.com>
- added --hide flag for ntsysv that allows you to hide a service from the
  user.

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- fix glob, once and for all. Really. We mean it.

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- revert fix for services@levels, it's broken
- change default to only edit the current runlevel

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- don't remove scripts that don't support chkconfig

* Tue Mar 09 1999 Erik Troan <ewt@redhat.com>
- made glob a bit more specific so xinetd and inetd don't cause improper matches

* Thu Feb 18 1999 Matt Wilson <msw@redhat.com>
- removed debugging output when starting ntsysv

* Thu Feb 18 1999 Preston Brown <pbrown@redhat.com>
- fixed globbing error
- fixed ntsysv running services not at their specified levels.

* Tue Feb 16 1999 Matt Wilson <msw@redhat.com>
- print the value of errno on glob failures.

* Sun Jan 10 1999 Matt Wilson <msw@redhat.com>
- rebuilt for newt 0.40 (ntsysv)

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- add ru.po.

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- translation updates

* Thu Oct 08 1998 Cristian Gafton <gafton@redhat.com>
- updated czech translation (and use cs instead of cz)

* Tue Sep 22 1998 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
- added pt_BR translations
- added more translatable strings
- support for i18n init.d scripts description

* Sun Aug 02 1998 Erik Troan <ewt@redhat.com>
- built against newt 0.30
- split ntsysv into a separate package

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- added numerous translations

* Mon Mar 23 1998 Erik Troan <ewt@redhat.com>
- added i18n support

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- added --back
