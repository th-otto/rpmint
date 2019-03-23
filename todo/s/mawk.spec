Summary: An interpreter for the awk programming language.
Name: mawk
Version: 1.3.3
Release: 1
Copyright: GPL
Group: Applications/Text
Source: ftp://ftp.oxy.edu/public/mawk-%{version}.tar.gz
Patch0: mawk-1.3.3-misc.patch
BuildRoot: %{_tmppath}/%{name}-root
Vendor: Sparemint
Packager: Keith Scroggins <kws@radix.net>

%description
Mawk is a version of the awk programming language.  Awk interprets a
special-purpose programming language to do quick text pattern matching
and reformatting.  Mawk improves on awk in certain ways and can
sometimes outperform gawk, the standard awk program for Linux.  Mawk
conforms to the POSIX 1003.2 (draft 11.3) definition of awk.

You should install mawk if you use awk.

%prep
%setup -q
%patch0 -p1 -b .misc
CFLAGS="$RPM_OPT_FLAGS" ./configure

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall mandir=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/mawk
%{_mandir}/*/*
%doc ACKNOWLEDGMENT CHANGES INSTALL README

%changelog
* Thu Nov 6 2003 Keith Scroggins <kws@radix.net>
- Initial release of 1.3.3 for FreeMiNT
