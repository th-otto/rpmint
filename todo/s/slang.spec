Summary: The library and header files for the S-Lang extension language
Name: slang
Version: 1.4.9
Release: 1
License: GPL
Vendor: Sparemint
Group: System Environment/Libraries
Source0: %{name}-%{version}.tar.gz
URL: http://www.s-lang.org/
Packager: Keith Scroggins <kws@radix.net>
BuildRoot:%{_tmppath}/%{name}-%{version}-root

%description
S-Lang is an interpreted language and a programming library. The S-Lang
language was designed so that it can be easily embedded into a program to
provide the program with a powerful extension language. The S-Lang library,
provided in this package, provides the S-Lang extension language.  S-Lang's
syntax resembles C, which makes it easy to recode S-Lang procedures in C if
you need to.

%prep
%setup -q 
CFLAGS="$RPM_OPT_FLAGS" ./configure --target=m68k-atari-mint 

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/slang

%makeinstall install_lib_dir=$RPM_BUILD_ROOT%{_libdir} \
	install_include_dir=$RPM_BUILD_ROOT%{_includedir}/slang install


# Remove documentation files.
rm -rf $RPM_BUILD_ROOT/usr/doc

strip --strip-debug $RPM_BUILD_ROOT%{_libdir}/*.a ||:

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_includedir}/*
%attr(0444,root,root) %{_libdir}/*.a


%changelog
* Tue Nov 04 2003 Keith Scroggins <kws@radix.net>
- Initial build of Slang for FreeMiNT
