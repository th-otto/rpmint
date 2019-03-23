Summary       : Throttleable lightweight httpd server
Name          : thttpd
Version       : 2.23beta1
Release       : 2
Copyright     : distributable (BSD)
Group         : Networking

Packager      : Marc-Anton Kehr <m.kehr@ndh.net>
Vendor        : Sparemint
URL           : http://www.acme.com/software/thttpd/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.acme.com/software/thttpd/thttpd-%{PACKAGE_VERSION}.tar.gz
Patch0: thttpd_MiNT.patch

%description
Thttpd is a very compact no-frills httpd serving daemon that can handle
very high loads.  While lacking many of the advanced features of
Apachee, thttpd operates without forking and is extremely efficient in
memory use.  Basic support for cgi scripts, authentication, and ssi is
provided for.  Advanced features include the ability to throttle traffic.


%prep
%setup -q
%patch -p1


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
CXXFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix}
make \
	prefix=%{_prefix} \
	BINDIR=%{_prefix}/sbin \
	MANDIR=%{_prefix}/share/man \
	WEBDIR=/home/httpd/html \
	WEBGROUP=httpd \
	CGIBINDIR=/home/httpd/cgi-bin


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/home/httpd/cgi-bin
mkdir -p ${RPM_BUILD_ROOT}/home/httpd/logs
mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

install -m 755 contrib/redhat-rpm/thttpd.init ${RPM_BUILD_ROOT}/etc/rc.d/init.d/thttpd
install -m 644 contrib/redhat-rpm/thttpd.conf ${RPM_BUILD_ROOT}/etc/

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	BINDIR=${RPM_BUILD_ROOT}%{_prefix}/sbin \
	MANDIR=${RPM_BUILD_ROOT}%{_prefix}/share/man \
	WEBDIR=${RPM_BUILD_ROOT}/home/httpd/html \
	WEBGROUP=httpd \
	CGIBINDIR=${RPM_BUILD_ROOT}/home/httpd/cgi-bin

# correct some things
chown -R 0.0 ${RPM_BUILD_ROOT}%{_prefix}/share/man ||:
chmod 555 ${RPM_BUILD_ROOT}/home/httpd/cgi-bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%pre
grep '^httpd:' /etc/passwd >/dev/null || \
	/usr/sbin/useradd -r httpd

%post
/sbin/chkconfig --add thttpd

%preun
/sbin/chkconfig --del thttpd


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,bin,bin)
%doc [A-Z]*
%attr(2755, httpd, httpd) %{_prefix}/sbin/makeweb
%{_prefix}/sbin/htpasswd
%{_prefix}/sbin/syslogtocern
%{_prefix}/sbin/thttpd
%{_prefix}/share/man/man*/*
%attr(-, httpd, httpd) /home/httpd
%attr(0755, root, root) /etc/rc.d/init.d/thttpd
%config /etc/thttpd.conf


%changelog
* Sun Jul 28 2002 Marc-Anton Kehr <m.kehr@ndh.net>
- First release for Sparemint
