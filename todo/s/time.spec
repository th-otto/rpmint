Summary: A GNU utility for monitoring a program's use of system resources.
Name: time
Version: 1.7
Release: 1
License: GPL
Group: Applications/System
Source: ftp://prep.ai.mit.edu/pub/gnu/%{name}/%{name}-%{version}.tar.gz
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-root
Prereq: /sbin/install-info
Vendor: Sparemint
Packager: Martin Tarenskeen <m.tarenskeen@zonnet.nl>

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running, and displays
the results.

%prep
%setup -q

%build
echo "ac_cv_func_wait3=\${ac_cv_func_wait3='yes'}" >> config.cache
%configure
make

%install
rm -rf %{buildroot}

%makeinstall
strip %{buildroot}%{_bindir}/time
gzip %{buildroot}%{_infodir}/time.info

%clean
rm -rf %{buildroot}

%post
/sbin/install-info %{_infodir}/time.info.gz %{_infodir}/dir \
	--entry="* time: (time).		GNU time Utility" 

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/time.info.gz %{_infodir}/dir \
	--entry="* time: (time).		GNU time Utility" 
fi

%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/time
%{_infodir}/time.info.gz

%changelog
* Mon Oct 31 2005 Martin Tarenskeen <m.tarenskeen@zonnet.nl> 1.7-27
- first release for SpareMiNT
