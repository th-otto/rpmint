Summary       : Snownews - a console RSS/RDF newsreader
Name          : snownews
Version       : 1.5.7
Release       : 1
Copyright     : GPL
Group         : Applications/Internet

Packager      : Jan Krupka <jkrupka@volny.cz>
Vendor        : Sparemint
URL           : http://home.kcore.de/~kiza/software/snownews/

BuildRequires : ncurses, libxml2

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://home.kcore.de/~kiza/software/snownews/download/snownews-1.5.7.tar.gz
Patch0: snownews-1.5.7-mint.patch

%description
Snownews is a console RSS/RDF newsreader. It supports all versions of RSS natively
and other formats via plugins.

%prep
%setup -q
%patch0 -p1
./configure --prefix=%{_prefix} --charset=ISO-8859-1

%build
make

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}
make DESTDIR="${RPM_BUILD_ROOT}" install-locales
make DESTDIR="${RPM_BUILD_ROOT}" install-man

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
cp snownews ${RPM_BUILD_ROOT}%{_prefix}/bin/
cp opml2snow ${RPM_BUILD_ROOT}%{_prefix}/bin/
cp snowsync ${RPM_BUILD_ROOT}%{_prefix}/bin/
cd ${RPM_BUILD_ROOT}%{_prefix}/bin/ 
ln -fs opml2snow snow2opml
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/snownews


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README* AUTHOR COPYING CREDITS Changelog
%{_prefix}/bin/*
%{_prefix}/share/locale/*/*/*
%{_prefix}/man/man*/*



%changelog
* Sun Aug 7 2005  Jan Krupka <jkrupka@volny.cz>
- update to new version, new spec file
* Sat Jul 4 2004  Jens Syckor <js712688@inf.tu-dresden.de>
- update to new version
* Sat May 8 2004  Jens Syckor <js712688@inf.tu-dresden.de>
- update to new version
* Sat Mar 20 2004  Jens Syckor <js712688@inf.tu-dresden.de>
- initial Sparemint release

