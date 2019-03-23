# Version of Apache
%define version 1.3.31

Summary: Apache Web server
Name: apache
Version: %{version}
Release: 1
Packager: Keith Scroggins <kws@radix.net>
Vendor: Sparemint
URL: http://httpd.apache.org/
Source0: apache_%{version}.tar.gz
Patch0: apache_1.3.29-mint.patch
Copyright: Apache
Group: System Environment/Daemons
BuildRoot: /var/tmp/apache-%{version}-buildroot
Conflicts: apache_ssl
Requires: perl
Buildrequires: perl, mintlib >= 0.55.3-5, gdbm

%package devel
Summary: Apache Web server development tools
Group: Development/Libraries

%description
Apache is an HTTP server designed as a plug-in replacement for
the NCSA server version 1.3 (or 1.4). It fixes numerous bugs in
the NCSA server and includes many frequently requested new
features, and has an API which allows it to be extended to meet
users' needs more easily.

This package includes all files necessary to run the Apache Web
server.

%description devel
Apache is an HTTP server designed as a plug-in replacement for
the NCSA server version 1.3 (or 1.4). It fixes numerous bugs in
the NCSA server and includes many frequently requested new
features, and has an API which allows it to be extended to meet
users' needs more easily.

This package includes all files necessary to build your own Apache
modules. With Sparemint, this is currently quite useless, as there
is no shared object support yet.

%prep

%setup -q -n apache_%{version}
%patch0 -p1

%build

OPTIM="-O2" ./configure \
	--with-perl=/usr/bin/perl \
	--without-confadjust \
	--server-uid=httpd \
	--server-gid=httpd \
	--with-layout=RedHat \
	--enable-module=most \
	--disable-module=auth_db \
	--disable-module=auth_anon \
	--disable-module=digest \
	--disable-module=headers \
	--disable-module=cern_meta \
	--disable-module=info \
	--disable-module=log_agent \
	--disable-module=log_referer \
	--disable-module=usertrack \
	--disable-module=so
make

%install
rm -rf $RPM_BUILD_ROOT
make install-quiet root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
ln -s /usr/sbin/apachectl $RPM_BUILD_ROOT/etc/rc.d/init.d/apache

find $RPM_BUILD_ROOT/usr/share/man -type f -print0 | xargs -0 gzip -9

%clean
rm -rf $RPM_BUILD_ROOT

%pre
grep "^httpd:" /etc/passwd >/dev/null
if [ $? -ne 0 ]
then
	# Unfortunately, there's no adduser-command yet :-/
	echo "httpd:*:80:80:Mr. Web Server:/var/www" >> /etc/passwd
	sort -n -t : -k 3 -o /etc/passwd /etc/passwd
fi
grep "^httpd:" /etc/group >/dev/null
if [ $? -ne 0 ]
then
	# Unfortunately, there's no addgroup-command yet :-/
	echo "httpd:*:80:httpd" >> /etc/group
	sort -n -t : -k 3 -o /etc/group /etc/group
fi

%files
%defattr(-,root,root)
%doc ABOUT_APACHE Announcement INSTALL LICENSE README* WARNING-WIN.TXT
/usr/bin
/usr/sbin/ab
/usr/sbin/apachectl
/usr/sbin/httpd
/usr/sbin/logresolve
/usr/sbin/rotatelogs
/usr/lib/apache
/usr/share/man
/etc/rc.d/init.d/apache
%config /etc/httpd/conf/access.conf
/etc/httpd/conf/access.conf.default
%config /etc/httpd/conf/httpd.conf
/etc/httpd/conf/httpd.conf.default
%config /etc/httpd/conf/magic
/etc/httpd/conf/magic.default
%config /etc/httpd/conf/mime.types
/etc/httpd/conf/mime.types.default
%config /etc/httpd/conf/srm.conf
/etc/httpd/conf/srm.conf.default
%config(noreplace) /var/www/html
%attr(755,root,root) %config(noreplace) /var/www/cgi-bin/printenv
%attr(755,root,root) %config(noreplace) /var/www/cgi-bin/test-cgi
%config(noreplace) /var/www/icons
%attr(-,httpd,httpd) /var/cache
/var/log
/var/run

%files devel
%defattr(-,root,root)
/usr/sbin/apxs
%dir /usr/include/apache

%changelog
* Fri Aug 13 2004 Keith Scroggins <kws@radix.net>
- Updated to Apache 1.3.31

* Fri Nov 14 2003 Keith Scroggins <kws@radix.net>
- Updated packages to version 1.3.29 of Apache and fixed 1 patch to apply to 
- latest source code.  Still using patches from 1.3.14 by previous packager.

* Tue Dec 12 2000 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- Initial release for Sparemint
