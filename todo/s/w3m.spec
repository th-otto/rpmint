Summary       : w3m - a text based Web browser and pager
Name          : w3m
Version       : 0.1.10
Release       : 1
Copyright     : Unknown
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://ei5nazha.yz.yamagata-u.ac.jp/~aito/w3m/eng/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.firedrake.org/w3m/w3m-%{version}.tar.gz
Patch0: w3m-0.1.10-mint.patch
Patch1: w3m-0.1.10-mint-config.patch


%description
w3m is a World Wide Web (WWW) text based  client.  It  has
English and Japanese help files and an option menu and can
be configured to use  either  language.  It  will  display
hypertext  markup  language  (HTML)  documents  containing
links to files residing on the local system,  as  well  as
files  residing  on  remote  systems.  It can display HTML
tables and frames.  In addition,  it  can  be  used  as  a
"pager" in much the same manner as "more" or "less".  Cur-
rent versions of w3m run on Unix (Solaris,  SunOS,  HP-UX,
Linux,  FreeBSD,  and  EWS4800)  and  on Microsoft Windows
9x/NT.

Note: The rpm comes preconfigured with lynx-like 
      keybindings, support for english language and cookies
      and SSL.

==========================================================================
This packages was compiled with -m68020-060. This means you need at least
a machine with an 68020 CPU and an FPU to use the programs herein.
==========================================================================


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
make
chmod -x Bonus/*


%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/w3m
install -m755 w3m ${RPM_BUILD_ROOT}%{_prefix}/bin/
install -m644 *.html ${RPM_BUILD_ROOT}%{_prefix}/lib/w3m/
install -m644 doc/w3m.1 ${RPM_BUILD_ROOT}%{_prefix}/man/man1/

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/man1/*

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
rm -rf ${RPM_BUILD_ROOT}


%post
cat <<EOF
==========================================================================
This packages was compiled with -m68020-060. This means you need at least
a machine with an 68020 CPU and an FPU to use the programs herein.
==========================================================================
EOF


%files
%doc README Bonus/ doc/
%{_prefix}/lib/w3m/*
%{_prefix}/bin/*
%{_prefix}/man/man1/*


%changelog
* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
