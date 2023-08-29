#
# spec file for package source-highlight
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define soname  4
Name:           source-highlight
Version:        3.1.9
Release:        5.8
Summary:        Source Code Highlighter with Support for Many Languages
License:        GPL-3.0-only
Group:          Productivity/Publishing/Other
URL:            https://www.gnu.org/software/src-highlite
Source0:        https://ftp.gnu.org/gnu/src-highlite/source-highlight-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/src-highlite/source-highlight-%{version}.tar.gz.sig
Source2:        %{name}.keyring
Source3:        baselibs.conf
Source4:        patches/source-highlight/source-highlight-apache2.conf
Patch0:         patches/source-highlight/source-highlight-doxygen_disable_timestamp_in_footer.patch
# PATCH-FIX-OPENSUSE use-lessopen.patch boo#1016309 fcrozat@suse.com -- use lessopen, not lesspipe
Patch1:         patches/source-highlight/source-highlight-use-lessopen.patch
# PATCH-FIX-UPSTREAM
Patch2:         patches/source-highlight/source-highlight-0001-Remove-throw-specifications.patch
BuildRequires:  bison
BuildRequires:  ctags
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  graphviz-gd
BuildRequires:  help2man
BuildRequires:  libboost_regex-devel
BuildRequires:  libicu-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  texinfo
Requires(post): %{install_info_prereq}
Requires(preun): %{install_info_prereq}

%description
Source-highlight reads source language specifications dynamically, thus it can
be easily extended (without recompiling the sources) for handling new
languages. It also reads output format specifications dynamically, and thus it
can be easily extended (without recompiling the sources) for handling new
output formats. The syntax for these specifications is quite easy (take a look
at the manual).

%package -n libsource-highlight%{soname}
Summary:        Source Code Highlighting C++ Library
Group:          System/Libraries
# libsource-highlight is only used by gdb, which does not use the ctags
# feature. Use a recommendation instead of a hard requirement, bsc#1193401
Recommends:     ctags

%description -n libsource-highlight%{soname}
Source-highlight reads source language specifications dynamically, thus it can
be easily extended (without recompiling the sources) for handling new
languages. It also reads output format specifications dynamically, and thus it
can be easily extended (without recompiling the sources) for handling new
output formats. The syntax for these specifications is quite easy (take a look
at the manual).

libsource-highlight is a C++ library that provides the features of
Source-highlight.

%package -n libsource-highlight-devel
Summary:        Source Code Highlighting C++ Library
Group:          Development/Libraries/C and C++
Requires:       libsource-highlight%{soname} = %{version}-%{release}
Requires(post): %{install_info_prereq}
Requires(preun): %{install_info_prereq}

%description -n libsource-highlight-devel
Source-highlight reads source language specifications dynamically, thus it can
be easily extended (without recompiling the sources) for handling new
languages. It also reads output format specifications dynamically, and thus it
can be easily extended (without recompiling the sources) for handling new
output formats. The syntax for these specifications is quite easy (take a look
at the manual).

libsource-highlight is a C++ library that provides the features of
Source-highlight.

%package cgi
Summary:        Source Code Highlighting CGI
Group:          Productivity/Networking/Web/Utilities
Requires:       apache2

%description cgi
Source-highlight reads source language specifications dynamically, thus it can
be easily extended (without recompiling the sources) for handling new
languages. It also reads output format specifications dynamically, and thus it
can be easily extended (without recompiling the sources) for handling new
output formats. The syntax for these specifications is quite easy (take a look
at the manual).

This package contains a CGI that can be used to highlight source code on
your webserver using source-highlight.

%prep
%autosetup -p1

sed -i 's/\r//g' doc/*.css

%build
BOOST_REGEX=$(/bin/ls -1 "%{_libdir}"/libboost_regex*mt*.so 2>/dev/null | head -1)
[ -n "$BOOST_REGEX" ] || BOOST_REGEX=$(/bin/ls -1 "%{_libdir}"/libboost_regex*.so 2>/dev/null | head -1)
if [ -n "$BOOST_REGEX" ]; then
    BOOST_REGEX="${BOOST_REGEX##*/lib}"
    BOOST_REGEX="${BOOST_REGEX%.so}"
    BOOST_REGEX_PARAM="--with-boost-regex=${BOOST_REGEX}"
else
    BOOST_REGEX_PARAM=""
fi

%configure \
  "$BOOST_REGEX_PARAM" \
  --with-bash-completion="%{_sysconfdir}/bash_completion.d" \
  --with-doxygen \
  --enable-static=no
%make_build
%make_build -C src source-highlight-cgi

%install
%make_install

install -d "%{buildroot}/srv/source-highlight"
libtool --mode=install install -m 0755 src/source-highlight-cgi "%{buildroot}/srv/source-highlight/source-highlight.cgi"
install -D -m0644 "%{SOURCE4}" "%{buildroot}%{_sysconfdir}/apache2/conf.d/%{name}.conf"

find %{buildroot} -type f -name "*.la" -delete -print

rm -rf "%{buildroot}%{_docdir}/%{name}/html"
rm -rf "%{buildroot}%{_datadir}/doc"

chmod 0644 AUTHORS ChangeLog COPYING CREDITS NEWS README THANKS TODO.txt

%if 0%{?suse_version} >= 1030
%fdupes -s "%{buildroot}%{_datadir}/"
%endif

%post
%install_info --info-dir="%{_infodir}" "%{_infodir}/source-highlight".info%{ext_info}

%preun
%install_info_delete --info-dir="%{_infodir}" "%{_infodir}/source-highlight".info%{ext_info}

%post -n libsource-highlight-devel
%install_info --info-dir="%{_infodir}" "%{_infodir}/source-highlight-lib".info%{ext_info}

%preun -n libsource-highlight-devel
%install_info_delete --info-dir="%{_infodir}" "%{_infodir}/source-highlight-lib".info%{ext_info}

%post   -n libsource-highlight%{soname} -p /sbin/ldconfig
%postun -n libsource-highlight%{soname} -p /sbin/ldconfig

%files
%license COPYING
%doc AUTHORS ChangeLog CREDITS NEWS README THANKS TODO.txt
%config %{_sysconfdir}/bash_completion.d/source-highlight
%{_bindir}/*
%{_datadir}/source-highlight
%{_mandir}/man1/*.1%{?ext_man}
%{_infodir}/source-highlight.info%{ext_man}

%files -n libsource-highlight%{soname}
%{_libdir}/libsource-highlight.so.%{soname}
%{_libdir}/libsource-highlight.so.%{soname}.*.*

%files -n libsource-highlight-devel
%{_includedir}/srchilite
%{_libdir}/libsource-highlight.so
%{_libdir}/pkgconfig/source-highlight.pc
%{_infodir}/source-highlight-lib.info%{?ext_info}

%files cgi
%config(noreplace) %{_sysconfdir}/apache2/conf.d/source-highlight.conf
%dir %{_sysconfdir}/apache2
%dir %{_sysconfdir}/apache2/conf.d
%dir /srv/source-highlight
/srv/source-highlight/source-highlight.cgi

%changelog
* Tue Apr 26 2022 Dirk Müller <dmueller@suse.com>
- add gpg signature validation
- use https:// as source reference
* Fri Dec 17 2021 Danilo Spinella <danilo.spinella@suse.com>
- Replace ctags hard requirement with a recommendation for
  libsource-highlight, fixes bsc#1193401
- Run spec-cleaner
* Tue Jun  1 2021 Christophe Giboudeaux <christophe@krop.fr>
- Add GCC 11 compatibility fix:
  * 0001-Remove-throw-specifications.patch
- Update source-highlight-doxygen_disable_timestamp_in_footer.patch
  to allow using %%autosetup
* Mon Dec 28 2020 Martin Pluskal <mpluskal@suse.com>
- Do not use keyring for now as key signing key is not properly
  published
- Modernise spec-file and simplify depenency conditionals
* Tue Dec 22 2020 Arjen de Korte <suse+build@de-korte.org>
- restore keyring as sig is available from upstream
* Thu Aug 20 2020 Dirk Mueller <dmueller@suse.com>
- update to 3.1.9:
  * changed esc.style to work better with dark theme terminals
  * updated C and C++ to more recent standards
  * fixed zsh.lang
  * added new Python keywords
  * added Rust
  * added ixpe
  * added vim
- remove keyring as sig no longer is available
* Thu Feb  2 2017 adam.majer@suse.de
- use individual libboost-*-devel packages instead of boost-devel
* Mon Mar  7 2016 fcrozat@suse.com
- Add use-lessopen.patch: use lessopen.sh instead of lesspipe in
  src-hilite-lesspipe.sh, since our less package ships with
  lessopen.sh (boo#1016309).
* Wed Apr  1 2015 mpluskal@suse.com
- Update to 3.1.8
  * src/lang.map: .f mapped to fotran
  * src/sh.lang: do not consider $' a variable
  * https://savannah.gnu.org/bugs/?36613
- Use correct requires for info
* Wed Mar 18 2015 mpluskal@suse.com
- Add baselibs.conf to sources
* Tue Mar 17 2015 mpluskal@suse.com
- Cleanup spec file with spec-cleaner
- Add gpg signature
- Use graphviz-gd instead of graphiz-gnome
- Disable build of static library
- Remove source-highlight-rpmlintrc
* Fri Mar 28 2014 schwab@suse.de
- Build with graphiz-gnome, needed for png support in dot
* Sun Dec 29 2013 benoit.monin@gmx.fr
- update to 3.1.7:
  * language definition for Lilypond
  * language definition for R statistics programming language
  * language definition for ISLISP
  * improved Erlang definition file
  * new output format: ESC 256 ascii code
* Wed May 16 2012 coolo@suse.com
- remove explicit lib requires that are even wrong in parts
* Wed May  9 2012 coolo@suse.com
- format sources to readd preamble
* Mon Feb 13 2012 coolo@suse.com
- patch license to follow spdx.org standard
* Mon Jan  2 2012 pascal.bleser@opensuse.org
- update to 3.1.6:
  * language definition file for T/Foswiki TML markup
  * new output format: ODF (e.g. for LibreOffice or to generate ODF
    color-highlighted snippets to be used by ODF back-ends, like asciidoc-odf)
  * new output format: MediaWiki
* Sun Sep  4 2011 pascal.bleser@opensuse.org
- soname bumped from 3 to 4
- dropped source-highlight-boost_ldflags_lib64.patch, was merged upstream
- update to 3.1.5:
  * boost m4 macro finds boost in lib64
  * boost m4 macro files are not installed
  * updated php lang definition with new php 5 keywords
  * language definition for Scheme
  * language definition for Po files
  * language definition for Opa
  * language definition for Javalog
  * language definition for UPC
  * fixed a bug in scala.lang dealing with keywords
  * updated sql.lang
  * Emacs lisp files highlighted as Lisp
  * improved logtalk.lang
  * embed inputlang in the output file
  * highlight _ in variable declarations
  * correctly highlight for less when filenames contain spaces
* Tue Jun 15 2010 pascal.bleser@opensuse.org
- update to 3.1.4:
  * php handles embedded html
  * html handles embedded css and javascript
  * Google's Protocol Buffers language definition added
  * CakePhp template files highlighted as php
  * haskell literate programming highlighting
  * vala language definition
  * lisp language definition
* Wed Jan 20 2010 pascal.bleser@opensuse.org
- update to 3.1.3:
  * --tab option is correcly handled
  * bash is highlighted
* Thu Dec 24 2009 pascal.bleser@opensuse.org
- update to 3.1.2:
  * language for files starting with <? and <!doctype is now
    inferred
  * some language definitions were added: manifest files, asm,
    applescript, vbscript, awk, bat, clipper, cobol, D, Erlang, and
    compiler output errors
  * a style for label and path was added
  * label elements are recognized in C/C++
  * logtalk.lang was improved
  * email regular expression in url.lang was improved
* Wed Sep 23 2009 pascal.bleser@opensuse.org
- SONAME change from 1 to 3
- added baselibs.conf
- update to 3.1.1:
  * access to static global LangDefManager, LangMaps is provided through the
    class Instances
  * a mechanism for setting a global data directory value was added, together
    with library utility functions to retrieve .lang and .outlang files
  * the SourceHighlight class returns the output file extension
  * the background color for the document is kept empty if it is not specified
    in the style file
  * the utils.h file is installed in the header directory
  * White is a standard color in style files
  * language definition files for Texinfo and Haskell were added
* Fri Jun 12 2009 pascal.bleser@opensuse.org
- update to 3.1:
  * some library utility functions to retrieve .style and .css files were added
  * a language definition for Oz was added
* Wed May 20 2009 pascal.bleser@opensuse.org
- moved to openSUSE Build Service (devel:tools)
* Tue May 19 2009 pascal.bleser@opensuse.org
- package the CGI into a -cgi subpackage
- update to 3.0.1:
  * fixed library manual link in index.html
  * doxyfile is now distributed
  * better formatting for < and > in latex output
  * doxygen documentation can be built even when building in a separate
    directory
  * added man page for source-highlight-settings
* Sat May  9 2009 pascal.bleser@opensuse.org
- update to 3.0:
  * source-highlight now also provides a C++ library
  * --regex-range has been added (highlight only specified lines of an input
    file)
  * --docdir is used for the documentation directory
  * the --binary-output command line option has been added
  * the program source-highlight-settings has been added to write a
    configuration file for source-highlight
  * language definitions for generic configuration files and for pkg-config
    files have been added
  * the input language is now also discovered using the whole file name
  * in .lang files, it is now possible to specify the exit level
- changes from 2.11.1:
  * language definitions for Fortran, Caml, and JavaScript were improved
  * ada language definition file was added
- changes from 2.11:
  * language definitions for Scala and Xorg configuration files were added
  * the procedure for regular expression matching was improved
  * boost regex library discovery in the configure script was improved
  * the configuration file for bash_completion was added
  * it is now possible to highlight only specific ranges of lines
* Tue Sep  9 2008 guru@unixtech.be
- update to 2.10:
  * formatting is applied even when generating anchors and references
  * noref is handled also for output languages using onestyle (e.g., xhtml)
  * improved fortran highlighting
  * improved python highlighting
  * fixed title in docbook output
  * language definition for ldap files (e.g., ldiff files)
  * language definition for autoconf files
  * improved m4 language definition
  * improved logtalk language definition
  * url.lang handles ~ in urls
  * language definition for glsl.lang (provided by Cesare Tirabassi)
