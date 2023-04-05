Summary       : An archiving and compression utility for LHarc format archives.
Name          : lha
Version       : 1.14i
Release       : 1
Copyright     : freeware
Group         : Applications/Archiving

Packager      : Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor        : Sparemint
URL           : http://www2m.meshnet.or.jp/~dolphin/lha/lha-unix.htm

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www2m.biglobe.ne.jp/~dolphin/lha/prog/%{name}-114i.tar.gz
Patch0: lha-1.14i-make.patch
Patch1: lha-1.14e-ext.patch


%description
LhA is an archiving and compression utility for LHarc format archive.
LhA is mostly used in the Amiga and in the DOS world, but can be used 
under Linux to extract files from .lha and .lzh archives. 

Install the LhA package if you need to extract files from .lha or .lzh
Amiga or DOS archives, or if you have to build LhA archives to
be read on the Amiga or DOS.

%prep
%setup -q -n %{name}-114i
%patch0 -p0
%patch1 -b .ext


%build
make OPTIMIZE="${RPM_OPT_FLAGS} -DHAVE_NO_LCHOWN"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
install -m755 -s src/lha ${RPM_BUILD_ROOT}%{_prefix}/bin
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/lha || :


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/bin/lha


%changelog
* Fri Mar 30 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.14i

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
