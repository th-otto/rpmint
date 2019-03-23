Summary: A smaller version of the Bourne shell (sh).
Name: ash
Version: 0.2
Release: 1
License: BSD
Packager: Jens Syckor <js712688@mail.inf.tu-dresden.de>
Vendor: Sparemint
Group: System Environment/Shells
Buildroot: %{_tmppath}/%{name}-%{version}

Source: %{name}-%{version}.tgz

%description
A shell is a basic system program which interprets user's keyboard 
commands. The ash shell is a clone of Berkeley's Bourne shell
(sh). Ash supports all of the standard sh shell commands, but is
considerably smaller than sh.  The ash shell lacks some Bourne shell
features (for example, command-line histories), but it uses a lot less
memory.

You should install ash if you need a lightweight shell with many of
the same capabilities as the sh shell.

%prep
%setup 

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/bin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

install -m 755 sh $RPM_BUILD_ROOT/bin/ash
install -m 644 sh.1 $RPM_BUILD_ROOT%{_mandir}/man1/ash.1


%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
/bin/ash
%{_mandir}/man1/ash.1

%changelog
* Sat Jul 5 2003 Jens Syckor <js712688@inf.tu-dresden.de>
first port for freemint
