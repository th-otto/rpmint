Summary       : PostScript Utilities
Name          : psutils
Version       : 1.17
Release       : 1
Copyright     : distributable
Group         : Applications/Publishing

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.dcs.ed.ac.uk/home/ajcd/psutils/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.dcs.ed.ac.uk/pub/ajcd/psutils-p17.tar.gz
Patch0: psutils-p17-Makefile.patch
Patch1: psutils-p17-misc.patch

# Patch1 derived from
# jurix.jura.uni-sb.de/pub/linux/source/networking/printing/psutils.dif


%description
This archive contains some utilities for manipulating PostScript documents.
Page selection and rearrangement are supported, including arrangement into
signatures for booklet printing, and page merging for n-up printing.


%prep
%setup -q -n psutils
%patch0 -p1
%patch1 -p1


%build
make -f Makefile.unix RPM_OPT_FLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install -f Makefile.unix \
	MANDIR=${RPM_BUILD_ROOT}%{_prefix}/share/man/man1 \
	DESTDIR=${RPM_BUILD_ROOT}

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(0644, root, root, 0755)
%doc README LICENSE
%attr(0755, root, root) %{_prefix}/bin/*
%{_prefix}/share/man/*/*
%{_prefix}/lib/psutils


%changelog
* Thu May 29 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
