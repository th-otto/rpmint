Name          : bash-completion
Summary       : bash-completion offers programmable completion for bash 2.05
Version       : 20020304
Release       : 1
License       : GPL
Group         : System Environment/Shells

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.caliban.org/bash/

Requires      : bash >= 2.05a, base >= 1.4, grep, sed
BuildArch     : noarch

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source: http://www.caliban.org/files/bash/%{name}-%{version}.tar.bz2


%description
bash-completion is a collection of shell functions that take advantage of
the programmable completion feature of bash 2.04 and later.

To use this collection, you ideally need bash 2.05a or later. You can also use
bash 2.05 if you apply the group name completion patch available at
http://www.caliban.org/files/bash/bash-2.05-group_completion.patch.
Alternatively, you can just comment out the lines that contain
'comp{lete,gen} -g'.

If you're using bash 2.04, in addition to commenting out the lines discussed
in the previous paragraph, you'll also to comment out the '-o <option>'
part of each invocation of 'complete' and edit /etc/bashrc to reflect this
version in the $BASH_VERSION test.


%prep
%setup -n bash_completion


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc
install -m644 bash_completion ${RPM_BUILD_ROOT}/etc


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README Changelog contrib/
/etc/bash_completion


%changelog
* Tue Mar 05 2002 Frank Naumann <fnaumann@freemint.de>
- first release for sparemint
