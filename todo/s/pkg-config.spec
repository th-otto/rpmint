%define	name		pkgconfig
%define	version		0.15.0
%define	release		1

Summary:	A tool for determining compilation options.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Vendor:		Sparemint
Packager:	Keith Scroggins <kws@radix.net>
Group:		Development/Tools
URL:		http://pkgconfig.gnu.org
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The pkgconfig tool determines compilation options. For each required
library, it reads the configuration file and outputs the necessary
compiler and linker flags.

%prep
%setup -q

%build
LIBS=-lsocket ./configure --prefix=/usr --target=m68k-atari-mint \
	--host=m68k-atari-mint --build=m68k-atari-mint
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/pkg-config
%{_datadir}/aclocal/pkg.m4
/usr/man/man1/pkg-config.1

%changelog
* Mon Jan 05 2004 Keith Scroggins <kws@radix.net>
- Initial release for MiNT
