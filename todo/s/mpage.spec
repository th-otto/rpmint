Summary       : A tool for printing multiple pages of text on each printed page.
Name          : mpage
Version       : 2.5.1
Release       : 1
Copyright     : BSD
Group         : Applications/Publishing

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.mesa.nl/

Requires      : ghostscript

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.mesa.nl/pub/mpage/mpage251pre.tgz
Patch0: mpage25-config.patch
Patch1: mpage24-dvips.patch
Patch2: mpage-debian.patch
Patch3: mpage-tempfile.patch
Patch4: mpage25-j.patch


%description
The mpage utility takes plain text files or PostScript(TM) documents
as input, reduces the size of the text, and prints the files on a
PostScript printer with several pages on each sheet of paper.  Mpage
is very useful for viewing large printouts without using up tons of
paper.  Mpage supports many different layout options for the printed
pages.

Mpage should be installed if you need a useful utility for viewing
long text documents without wasting paper.


%prep
%setup -q -n mpage-2.5.1
%patch0 -p1 -b .config
#patch1 -p1 -b .dvips
%patch2 -p1 -b .debian
%patch3 -p1 -b .tempfile
%patch4 -p1 -b .jp


%build
make PAGESIZE=A4 \
	BINDIR=%{_prefix}/bin \
	LIBDIR=%{_prefix}/share \
	MANDIR=%{_prefix}/share/man/man1


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/{mpage,man/man1}

make install \
	PREFIX=${RPM_BUILD_ROOT}/%{_prefix} \
	BINDIR=${RPM_BUILD_ROOT}/%{_prefix}/bin \
	LIBDIR=${RPM_BUILD_ROOT}/%{_prefix}/share \
	MANDIR=${RPM_BUILD_ROOT}/%{_prefix}/share/man/man1

strip ${RPM_BUILD_ROOT}/usr/bin/mpage ||:
stack --fix=128k ${RPM_BUILD_ROOT}/usr/bin/mpage ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc CHANGES Copyright README NEWS TODO
%{_prefix}/bin/mpage
%{_prefix}/share/man/man*/*
%{_prefix}/share/mpage


%changelog
* Thu May 31 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
