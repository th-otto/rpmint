# This is a rpm spec file for polipo-1.0.4

%define name            polipo
%define release         2
%define version         1.0.4

Summary:    polipo-1.0.4 Proxy Server
License:    Free
Name:       %{name}
Version:    %{version}
Release:		%{release}
Source:     http://freehaven.net/~chrisd/polipo/polipo-1.0.4.tar.gz
Group:      Network/Daemons
Prefix: 		%{_prefix}
Docdir: 		%{_prefix}/doc
BuildRoot: 	%{_tmppath}/%{name}-root
URL:			http://www.pps.jussieu.fr/~jch/software/polipo/
Patch0:  	polipo-1.0.4-Makefile.patch
Patch1: 		polipo-1.0.4-chunk.c.patch
Patch2:		polipo-1.0.4-polipo.h.patch
Patch3:		polipo-1.0.4-config.sample.patch

%description
Polipo is a small and fast caching web proxy (a web cache, an HTTP 
proxy, a proxy server). 
By virtue of being a (mostly) compliant HTTP/1.1 proxy, Polipo has all 
the uses of traditional web proxies. It is typically used as a web proxy 
for a single computer or a small network, although there's no 
fundamental reason why it shouldn't be used by a larger one. 

%prep
%setup -q
# this patch also comments out info generation, otherwise build fails because of parsing errors.
%patch0 
%patch1 -p1
%patch2
%patch3

%build

#export CFLAGS="${RPM_OPT_FLAGS} -m68020-60" 
#make TARGET=$RPM_BUILD_ROOT

#export CFLAGS="${RPM_OPT_FLAGS} -mcpu=5475" 
#make TARGET=$RPM_BUILD_ROOT

#export CFLAGS="-m68000 -O0 -g -DHAVE_GMT_OFF" 
export CFLAGS="${RPM_OPT_FLAGS} -m68000" 
make TARGET=$RPM_BUILD_ROOT

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT%{_prefix}/doc/polipo
mkdir -p $RPM_BUILD_ROOT/etc/polipo
mkdir -p $RPM_BUILD_ROOT/var/cache/polipo
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/polipo/www/doc

install -m 644 forbidden.sample $RPM_BUILD_ROOT/etc/polipo/forbidden
install -m 644 config.sample $RPM_BUILD_ROOT/etc/polipo/config
install -m 644 INSTALL $RPM_BUILD_ROOT/%{_prefix}/share/polipo/www/doc/index.html
make install TARGET=$RPM_BUILD_ROOT prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/*
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/*

# Uncomment this when info building works:
#rm -rf ${RPM_BUILD_ROOT}%{_prefix}/info/dir
#rm -rf ${RPM_BUILD_ROOT}%{_prefix}/info/dir.old.gz
#rm -rf ${RPM_BUILD_ROOT}%{_prefix}/info/dir.old

%files
%defattr(-,root,root)
%{_prefix}/bin/polipo
%doc README INSTALL COPYING forbidden.sample config.sample
%attr(0644,root,root) %{_prefix}/share/man/man1/*
# info currently does not work with freemint ( old texi version )
#%attr(0644,root,root) %{_prefix}/info/polipo.info.gz
%{_prefix}/share/polipo/www/*
/var/cache/polipo/
%config /etc/polipo/config
%config /etc/polipo/forbidden

%changelog
* Thu Aug 07 2010 Ole Loots <ole@monochrom.net>
- Initial Sparemint release of version 1.0.4, added config patch, fixed www docs


