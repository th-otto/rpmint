Summary       : configuration file library
Summary(de)   : Library zum Lesen von Konfigurationsdateien
Name          : conflib
Version       : 0.4.5
Release       : 1
Copyright     : GPL
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.ohse.de/uwe/software/conflib.html

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.ohse.de/uwe/releases/conflib-0.4.5.tar.gz


%description 
A C language library for reading configuration files.
This library makes it relativly easy to read configuration files (one or
more), or parts of them. It supports a lot of different data types and
some types of text interpretations, including \-escapes, ~user, $HOME
and conditional expansions.


%prep
%setup -q
cp /usr/lib/rpm/config.{guess,sub} .


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install prefix=${RPM_BUILD_ROOT}%{_prefix}

# compress info files
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*info*



%post
/sbin/install-info %{_prefix}/info/conflib.info.gz %{_prefix}/info/dir --entry="* Conflib: (conflib.info).         Configuration File Handling."

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/history.info.gz %{_prefix}/info/dir --entry="* Conflib: (conflib.info).         Configuration File Handling."
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc README NEWS ChangeLog
%{_prefix}/include/*.h
%{_prefix}/info/*info*
%{_prefix}/lib/lib*.a


%changelog
* Tue Jan 30 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
