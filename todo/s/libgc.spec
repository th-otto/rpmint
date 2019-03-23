Summary       : Boehm Conservative Garbage Collection for C/C++
Name          : libgc
Version       : 5.3
Release       : 1
Copyright     : Freely Redistributable
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.hpl.hp.com/personal/Hans_Boehm/gc/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/gc5.3.tar.gz
Patch0: gc-5.3-mint.patch
Patch1: gc-5.3-make.patch

%description
This is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

Since the collector does not require pointers to be tagged, it does not
attempt to ensure that all inaccessible storage is reclaimed.  However,
in our experience, it is typically more successful at reclaiming unused
memory than most C programs using explicit deallocation.  Unlike manually
introduced leaks, the amount of unreclaimed memory typically stays
bounded.

%package devel
Summary       : Boehm Conservative Garbage Collection for C/C++
Group         : Development/Libraries

%description devel
This is a garbage collecting storage allocator that is intended to be
used as a plug-in replacement for C's malloc.

Since the collector does not require pointers to be tagged, it does not
attempt to ensure that all inaccessible storage is reclaimed.  However,
in our experience, it is typically more successful at reclaiming unused
memory than most C programs using explicit deallocation.  Unlike manually
introduced leaks, the amount of unreclaimed memory typically stays
bounded.

Header files and static library for libgc


%prep
%setup -q -n gc
%patch0 -p1 -b .mint
%patch1 -p1 -b .make


%build
make all c++


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{lib,share/man/man1,include/gc/private}

install -m 644 gc.man ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/gc.1
install -m 644 gc.a ${RPM_BUILD_ROOT}%{_prefix}/lib/libgc.a
install -m 644 include/*.h ${RPM_BUILD_ROOT}%{_prefix}/include/gc
install -m 644 include/private/*.h ${RPM_BUILD_ROOT}%{_prefix}/include/gc/private

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%doc README* barrett_diagram
%{_prefix}/include/gc
%{_prefix}/lib/libgc.a
%{_prefix}/share/man/*/*


%changelog
* Thu Jun 21 2001 Frank Naumann <fnaumann@freemint.de>
- initial revision for SpareMiNT
