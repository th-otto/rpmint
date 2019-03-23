Summary       : Selfmode Manager for USR Sportster Message Plus (Pro)
Name          : smmgr
Version       : 1.1.2
Release       : 2
Copyright     : distributable
Group         : Applications/File

Packager      : Marc-Anton Kehr <m.kehr@ndh.net>
Vendor        : Sparemint

BuildRequires : gsm

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.logic.at/people/preining/software/smmgr-%{version}.tar.gz
Patch0: smmgr-1.1.2.patch


%description
The US Robotics Sportster Message Plus can receive fax and voice messages
on its own and has a 2MB flash memory to store them. They can later be
downloaded using this program. It is also used to conviently change settings
for the independent mode.


%prep
%setup -q
%patch0 -p1 -b .make


%build
make EXTRACFLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
mkdir -p ${RPM_BUILD_ROOT}/var/spool
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
make install \
	PREFIX=${RPM_BUILD_ROOT}%{_prefix} \
	LIBDIR=${RPM_BUILD_ROOT}/var/lib/modem-mgr \
	SPOOLDIR=${RPM_BUILD_ROOT}/var/spool/modem-mgr \
	CONFIGFILE=${RPM_BUILD_ROOT}/etc/smmgr.conf


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
mkdir -p /var/lib/modem-mgr ||:
mkdir -p /var/spool/modem-mgr ||:


%files
%doc README TODO Commands.txt
%attr(0644,root,root)	/etc/smmgr.conf
%attr(0755,root,root)	%{_prefix}/bin/smmgr
%attr(0755,root,root)	%{_prefix}/bin/lsmmgr


%changelog
* Tue Feb 18 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- build against MiNTLib 0.56
- enabled GSM support
- fixed lockfile problem when exiting (thanks to Frank)
