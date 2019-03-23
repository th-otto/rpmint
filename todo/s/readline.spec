Summary       : A library for editing typed in command lines.
Name          : readline
Version       : 4.2
Release       : 1
Copyright     : GPL
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.cwru.edu/pub/bash/%{name}-%{version}.tar.gz
Patch0: readline-4.2-mint.patch


%description
The readline library reads a line from the terminal and returns it,
allowing the user to edit the line with standard emacs editing keys.
The readline library allows programmers to provide an easy to use and
more intuitive interface for users.

If you want to develop programs that will use the readline library,
you'll also need to install the readline-devel package.

%package devel
Summary       : Development files for programs which will use the readline library.
Group         : Development/Libraries
Requires      : readline = %{PACKAGE_VERSION}

%description devel
The readline library will read a line from the terminal and return it.
Use of the readline library allows programmers to provide an easy
to use and more intuitive interface for users.

If you want to develop programs which will use the readline library,
you'll need to have the readline-devel package installed.  You'll also
need to have the readline package installed.


%prep
%setup -q
%patch0 -p1 -b .mint

cp /usr/lib/rpm/config.{guess,sub} support/


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--with-curses
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}/%{_prefix}

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*info*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/*

 
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/history.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/readline.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/rluserman.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/history.info.gz %{_prefix}/info/dir
   /sbin/install-info --delete %{_prefix}/info/readline.info.gz %{_prefix}/info/dir
   /sbin/install-info --delete %{_prefix}/info/rluserman.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc CHANGES COPYING README USAGE
%doc doc/*.html doc/*.ps
%{_prefix}/share/man/man*/*
%{_prefix}/info/*info*

%files devel
%defattr(-,root,root)
%{_prefix}/include/readline
%{_prefix}/lib/lib*.a


%changelog
* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
