%define name            ccache
%define release         2
%define version         2.4

Summary:	A fast C/C++ compiler cache
License:        GPL
Name:           %{name}
Version:        %{version}
Release:        %{release}
Source:         %{name}-%{version}.tar.gz
Prefix: 		%{_prefix}
Docdir: 	   %{_prefix}/doc
BuildRoot: 	%{_tmppath}/%{name}-root
Group:          Development/Tools
Packager:      	Ole Loots <ole@monochrom.net>
Vendor:        	Sparemint

Patch0:		ccache-2.4-unify.c.patch
Patch1:		ccache-2.4-ccache.h.patch

%description
ccache is a compiler cache. It speeds up recompilation of C/C++ code by caching 
previous compilations and detecting when the same compilation is being done again. 
This often results in a significant speedup in common compilations.

%prep
%setup -q
%patch0 -p1 
%patch1 -p1

%build
export CFLAGS="${RPM_OPT_FLAGS}"
export CXXFLAGS="${RPM_OPT_FLAGS}"
./configure --prefix=%{_prefix}
make

%install
# Uncomment this if you are sure RPM_BUILD_ROOT is not /
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin 
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/man/man1
make install prefix=${RPM_BUILD_ROOT}%{_prefix} \
mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man
install -m 755 ccache ${RPM_BUILD_ROOT}%{_prefix}/bin
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/*

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/*

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README COPYING
%attr(0755,root,root) %{_prefix}/bin/ccache
%attr(0644,root,root) %{_prefix}/share/man/man1/*

%changelog
* Tue Jun 10 2010 Ole Loots <ole@monochrom.net>
- Some improvements made to the spec file, located binary to /usr/bin

* Wed Jun 9 2010 Ole Loots <ole@monochrom.net>
- Initial Sparemint release of version 2.4
