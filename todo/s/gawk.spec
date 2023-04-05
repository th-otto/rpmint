Summary       : The GNU version of the awk text processing utility.
Summary(de)   : Die GNU Version von dem awk Textprocessor.
Name          : gawk
Version       : 3.0.6
Release       : 1
Copyright     : GPL
Group         : Applications/Text

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.gnu.org/gnu/gawk/

Prereq        : /sbin/install-info
Provides      : awk

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.gz
Source1: ftp://ftp.gnu.org/gnu/gawk/gawk-%{version}-ps.tar.gz
Patch0:  gawk-3.0-unaligned.patch
Patch1:  gawk-3.0.6-mint.patch


%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.


%prep
%setup -q -b 1
%patch0 -p1 -b .unaligned
%patch1 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS} -Uatarist" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}/usr bindir=${RPM_BUILD_ROOT}/bin

strip ${RPM_BUILD_ROOT}/bin/gawk
stack --fix=256k ${RPM_BUILD_ROOT}/bin/gawk || :

strip ${RPM_BUILD_ROOT}%{_prefix}/libexec/awk/*
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/libexec/awk/* || :

# compress manuals
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/gawk.info*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/*/*

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
ln -sf gawk.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/awk.1
ln -sf ../../bin/gawk ${RPM_BUILD_ROOT}%{_prefix}/bin/awk 
ln -sf ../../bin/gawk ${RPM_BUILD_ROOT}%{_prefix}/bin/gawk 


%post
/sbin/install-info %{_prefix}/info/gawk.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/gawk.info.gz %{_prefix}/info/dir
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc README COPYING ACKNOWLEDGMENT FUTURES INSTALL LIMITATIONS NEWS PORTS 
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps
/bin/*
%{_prefix}/bin/*
%{_prefix}/info/*info*
%{_prefix}/libexec/awk
%{_prefix}/share/awk
%{_prefix}/share/man/*/*


%changelog
* Tue Mar 20 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 3.0.6

* Mon Sep 20 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- package provide awk now

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
- added Summary(de)
