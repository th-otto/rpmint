Distribution  : Exuberant Ctags
Summary       : A multi-language source code indexing tool
Name          : ctags
Version       : 5.0.1
Release       : 1
Copyright     : GPL
Group         : Development/Tools

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://ctags.sourceforge.net/

Requires      : vim >= 6.0

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://ctags.sourceforge.net/archives/ctags-%{version}.tar.gz


%description
Exuberant Ctags generates an index (or tag) file of language objects
found in source files for many popular programming languages. This index
makes it easy for text editors and other tools to locate the indexed
items. Exuberant Ctags improves on traditional ctags because of its
multilanguage support, its ability for the user to define new languages
searched by regular expressions, and its ability to generate emacs-style
TAGS files.

Install ctags if you are going to use your system for programming.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--disable-etags

make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

# strip binaries
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(0644,root,root,0755)
%doc COPYING EXTENDING.html FAQ NEWS QUOTES README
%attr(0755,root,root) %{_prefix}/bin/*
%{_prefix}/share/man/man*/*


%changelog
* Thu Oct 04 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
