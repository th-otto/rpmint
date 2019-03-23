Summary       : A GNU source-level debugger for C, C++ and Fortran.
Name          : gdb
Version       : 5.0
Release       : 4
Copyright     : GPL
Group         : Development/Other

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://sourceware.cygnus.com/gdb/5/

Prereq        : /sbin/install-info
BuildRequires : ncurses-devel

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://sourceware.cygnus.com/pub/gdb/releases/gdb-%{version}.tar.gz
Patch1: gdb-5.0-mint-bfd.patch
Patch2: gdb-5.0-mint-config.patch
Patch3: gdb-5.0-mint-gdb.patch
Patch4: gdb-5.0-mint-gdbserver.patch
Patch5: gdb-5.0-mint-readline.patch


%description
Gdb is a full featured, command driven debugger. Gdb allows you to
trace the execution of programs and examine their internal state at
any time.  Gdb works for C and C++ compiled with the GNU C compiler
gcc.

If you are going to develop C and/or C++ programs and use the GNU gcc
compiler, you may want to install gdb to help you debug your
programs.

WARNING: You require a FreeMiNT kernel that support new ptrace()
system call. This is true for 1.15.12 and higher (including the
1.16 kernel line).


%prep
%setup -q -n gdb-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1


%build
# recreate configure for bfd backend
cd bfd
autoconf
cd ..

CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--host=m68k-atari-mint \
	--target=m68k-atari-mint

make
make info
cd gdb/gdbserver
make XM_CLIBS=-lsocket
cd ../..
cp gdb/NEWS .


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}/%{_prefix}
make install-info \
	prefix=${RPM_BUILD_ROOT}/%{_prefix}

cd gdb/gdbserver
make install \
	prefix=${RPM_BUILD_ROOT}/%{_prefix}
cd ../..

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*

# strip down, increase stack a little bit
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/gdb.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/gdbint.info.gz %{_prefix}/info/dir
/sbin/install-info %{_prefix}/info/stabs.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_prefix}/info/gdb.info.gz %{_prefix}/info/dir
	/sbin/install-info --delete %{_prefix}/info/gdbint.info.gz %{_prefix}/info/dir
	/sbin/install-info --delete %{_prefix}/info/stabs.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc COPYING COPYING.LIB README NEWS
%{_prefix}/bin/gdb
#%#{_prefix}/bin/gdbserver
%{_prefix}/share/man/man1/gdb.1.gz
#%#{_prefix}/share/man/man1/gdbserver.1.gz
%{_prefix}/info/gdb.info*
%{_prefix}/info/gdbint.info*
%{_prefix}/info/stabs.info*


%changelog
* Thu Nov 28 2000 Frank Naumann <fnaumann@freemint.de>
- recompiled against newer MiNTLib without a signal handling bug
  under 1.15 kernels

* Thu Nov 28 2000 Frank Naumann <fnaumann@freemint.de>
- fixed problems due to missing relocation on inferior termination

* Fri Nov 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
