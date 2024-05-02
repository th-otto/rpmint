%define pkgname python3
%global python_version 3.11
%define         python_pkg_name python311

%rpmint_header

Summary:        Python Interpreter
Name:           %{crossmint}%{pkgname}
Version:        3.11.8
Release:        1
License:        Python-2.0
Group:          Development/Languages/Python

URL:            http://www.python.org/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1:        patches/automake/mintelf-config.sub
Source2:        patches/python3/python3-macros.python3

Patch0:         patches/python3/python3-F00251-change-user-install-location.patch
Patch1:         patches/python3/python3-distutils-reproducible-compile.patch
Patch2:         patches/python3/python3-3.3.0b1-localpath.patch
Patch3:         patches/python3/python3-3.3.0b1-fix_date_time_compiler.patch
Patch4:         patches/python3/python3-3.3.0b1-test-posix_fadvise.patch
Patch5:         patches/python3/python3-subprocess-raise-timeout.patch
Patch6:         patches/python3/python3-bpo-31046_ensurepip_honours_prefix.patch
Patch7:         patches/python3/python3-no-skipif-doctests.patch
Patch8:         patches/python3/python3-skip-test_pyobject_freed_is_freed.patch
Patch9:         patches/python3/python3-fix_configure_rst.patch
Patch10:        patches/python3/python3-support-expat-CVE-2022-25236-patched.patch
Patch11:        patches/python3/python3-skip_if_buildbot-extend.patch
Patch12:        patches/python3/python3-CVE-2023-27043-email-parsing-errors.patch
Patch13:        patches/python3/python3-libexpat260.patch
Patch14:        patches/python3/python3-CVE-2023-6597-TempDir-cleaning-symlink.patch
Patch15:        patches/python3/python3-bsc1221260-test_asyncio-ResourceWarning.patch
Patch16:        patches/python3/python3-bluez-devel.patch
Patch17:        patches/python3/python3-Fix-shebangs.patch
Patch18:        patches/python3/python3-cross-config.patch
Patch19:        patches/python3/python3-mintnosharedmod.patch
Patch20:        patches/python3/python3-mintsetupdist.patch
Patch21:        patches/python3/python3-mint.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  python3
BuildRequires:  pkgconfig
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  %{crossmint}gmp-devel
BuildRequires:  %{crossmint}lzma-devel
BuildRequires:  %{crossmint}bzip2
BuildRequires:  %{crossmint}expat
BuildRequires:  %{crossmint}zlib
BuildRequires:  %{crossmint}ncurses
BuildRequires:  %{crossmint}readline
Provides:       %{crossmint}%{python_pkg_name}-base = %{version}
Provides:       %{crossmint}%{python_pkg_name}-readline
Provides:       %{crossmint}%{python_pkg_name}-sqlite3
Provides:       %{crossmint}%{python_pkg_name}-curses
Provides:       %{crossmint}%{python_pkg_name}-dbm
Provides:       %{crossmint}%{python_pkg_name}-pip
Provides:       %{crossmint}%{python_pkg_name}-tools
Provides:       %{crossmint}python3 = %{python_version}
Provides:       %{crossmint}python3-base = %{python_version}
Provides:       %{crossmint}python3-readline = %{python_version}
Provides:       %{crossmint}python3-sqlite3 = %{python_version}

%rpmint_build_arch

%description
Python is an interpreted, object-oriented programming language, and is
often compared to Tcl, Perl, Scheme, or Java.  You can find an overview
of Python in the documentation and tutorials included in the python-doc
(HTML) or python-doc-pdf (PDF) packages.

%package devel
Summary: The libraries and header files needed for Python development.
Requires: python = %{version}
Group: Development/Libraries

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package docs
Summary: Documentation for the Python programming language.
Group: Documentation

%description docs
The python-docs package contains documentation on the Python
programming language and interpreter.  The documentation is provided
in ASCII text files and in LaTeX source files.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n Python-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

# drop Autoconf version requirement
sed -i 's/^AC_PREREQ/dnl AC_PREREQ/' configure.ac

autoreconf -fiv
rm -f config.sub
cp %{S:1} config.sub

# prevent make from trying to rebuild asdl stuff, which requires existing
# python installation
touch Parser/asdl* Python/Python-ast.c Include/Python-ast.h

# drop in-tree libffi and expat
rm -rf Modules/_ctypes/libffi* Modules/_ctypes/darwin
# Cannot remove it because of gh#python/cpython#92875
# rm -rf Modules/expat

# drop duplicate README from site-packages
rm -f Lib/site-packages/README.txt

# Don't fail on warnings when building documentation
sed -i -e '/^SPHINXERRORHANDLING/s/-W//' Doc/Makefile

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--build=`./config.guess`
	--with-platlibdir=lib
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/python
	--disable-ipv6
	--disable-shared --enable-static
	--enable-unicode=ucs4
	--with-system-expat
	--without-thread
	--without-ensurepip
	--with-build-python=python3
	--config-cache
"
COMMON_CFLAGS+=" -fwrapv -DOPENSSL_LOAD_CONF"
STACKSIZE="-Wl,-stack,512k"

CPU_ARCHNAME_000=-000
CPU_ARCHNAME_020=-020
CPU_ARCHNAME_v4e=-v4e

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	eval archname=\${CPU_ARCHNAME_$CPU}

cat << EOF > config.cache
ac_cv_file__dev_ptmx=no
ac_cv_file__dev_ptc=no
ac_cv_lib_intl_textdomain=yes
ac_cv_func_pthread_condattr_setclock=no
ac_cv_have_pthread_t=no
ac_cv_func_pthread_kill=no
ac_cv_func_pthread_sigmask=no
ac_cv_header_pthread_h=no
EOF

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE -s" \
	AR="%{_rpmint_target_ar}" \
	RANLIB="%{_rpmint_target_ranlib}" \
	STRIP="%{_rpmint_target_strip}" \
	PYTHON_FOR_BUILD=python3 \
	LIBS=-liconv \
	sh ./configure ${CONFIGURE_FLAGS}

	make %{?_smp_mflags}
	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make DESTDIR="${buildroot}" TARGET=${TARGET} SYSROOT=%{_rpmint_sysroot} install

	# RPM macros
	mkdir -p ${buildroot}/etc/rpm
	install -m 644 %{S:2} ${buildroot}/etc/rpm/macros.python3

	# scripts
	rm -f ${buildroot}%{_rpmint_target_prefix}/bin/pydoc3*
	install -m 755 Tools/scripts/pydoc3 ${buildroot}%{_rpmint_target_prefix}/bin/pydoc%{python_version}
	ln -s pydoc%{python_version} ${buildroot}%{_rpmint_target_prefix}/bin/pydoc3
	install -m 755 Tools/scripts/2to3 ${buildroot}%{_rpmint_target_prefix}/bin/2to3-%{python_version}
	install -m 755 Tools/scripts/pyvenv ${buildroot}%{_rpmint_target_prefix}/bin/pyvenv-%{python_version} || :

	make clean > /dev/null

	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias	
	rm -f %{buildroot}%{_rpmint_bindir}/*-config

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

	chmod u+w %{buildroot}%{_rpmint_libdir}/*.a
	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_rpmint_libdir}$multilibdir
		mv %{buildroot}%{_rpmint_libdir}/*.a %{buildroot}%{_rpmint_libdir}$multilibdir
	fi
	
	# remove hard links and replace them with symlinks
	# keeping python2.7 the default
	for dir in bin include lib ; do
	    rm -f ${buildroot}%{_rpmint_target_prefix}/$dir/python
	done
	rm -f ${buildroot}%{_rpmint_target_prefix}/lib/pkgconfig/python.pc

	# remove wrapper scripts for packages not built
	rm -f ${buildroot}%{_rpmint_target_prefix}/bin/idle*

	# the directory for modules must exist; getpath.c depends on it
	mkdir -p ${buildroot}%{_rpmint_target_prefix}/lib/python%{python_version}/lib-dynload
	
	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif
done

%install

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_isysroot}/etc
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/lib/python%{python_version}
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/python%{python_version}
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif

%files docs
%defattr(-,root,root)
%license LICENSE
%doc README.rst Doc


%changelog
* Mon Apr 15 2024 Thorsten Otto <admin@tho-otto.de>
- Update to version 3.11.8

* Mon Apr 10 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 3.6.4

* Tue Sep 14 2004 Mark Duckworth <mduckworth@atari-source.com>
- Updated to the latest version

* Mon Aug 30 2004 Mark Duckworth <mduckworth@atari-source.com>
- Built against latest gemlib
- Fixed stacksize issues
- Fixed lack of stripped binary

* Sat Mar 20 2004 Mark Duckworth <mduckworth@atari-source.com>
- Changed packager due to new maintainer
- gdbm, zlib and sockets all work fine as far as I can tell.
- Bittorrent client tested works (curses one fails, headless works)

* Tue Sep 19 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- 1st release for Sparemint.
- Removed gdbm and zlib support until such time as I can get
  them to work with Python. These two modules, plus the socket module
	fail, although sockets only fail because of MiNTNet's limitations.
- Removed the tkinter package, as it doesn't really make sense for MiNT.

* Thu Sep 14 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- 1st built for Sparemint
