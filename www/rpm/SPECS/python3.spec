%define pkgname python3
%global python_version 3.6

%rpmint_header

Summary:        Python Interpreter
Name:           %{crossmint}%{pkgname}
Version:        3.6.4
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

Patch0:         patches/python3/python3-3.0b1-record-rpm.patch
Patch1:         patches/python3/python3-3.6.0-multilib-new.patch
Patch2:         patches/python3/python3-3.3.0b1-localpath.patch
Patch3:         patches/python3/python3-3.3.0b1-fix_date_time_compiler.patch
Patch4:         patches/python3/python3-3.3.0b1-curses-panel.patch
Patch5:         patches/python3/python3-3.3.0b1-test-posix_fadvise.patch
Patch6:         patches/python3/python3-3.3.3-skip-distutils-test_sysconfig_module.patch
Patch7:         patches/python3/python3-subprocess-raise-timeout.patch
Patch8:         patches/python3/python3-0001-allow-for-reproducible-builds-of-python-packages.patch
Patch9:         patches/python3/python3-distutils-reproducible-compile.patch
Patch10:        patches/python3/python3-skip_random_failing_tests.patch
Patch11:        patches/python3/python3-fix-localeconv-encoding-for-LC_NUMERIC.patch
Patch12:        patches/python3/python3-sorted_tar.patch
Patch13:        patches/python3/python3-mint.patch
Patch14:        patches/python3/python3-mintnosharedmod.patch
Patch15:        patches/python3/python3-cross-config.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  python3

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
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

# drop Autoconf version requirement
sed -i 's/^AC_PREREQ/dnl AC_PREREQ/' configure.ac

autoreconf -fiv
rm -f config.sub
cp %{S:1} config.sub

# prevent make from trying to rebuild asdl stuff, which requires existing
# python installation
touch Parser/asdl* Python/Python-ast.c Include/Python-ast.h

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--build=`./config.guess`
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/python
	--disable-ipv6
	--with-fpectl
	--disable-shared --enable-static
	--enable-unicode=ucs4
	--with-system-expat
	--without-thread
	--without-ensurepip
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
	install -m 755 Tools/scripts/pydoc3 ${buildroot}%{_rpmint_target_prefix}/bin/pydoc3-%{python_version}
	install -m 755 Tools/scripts/2to3 ${buildroot}%{_rpmint_target_prefix}/bin/2to3-%{python_version}
	install -m 755 Tools/scripts/pyvenv ${buildroot}%{_rpmint_target_prefix}/bin/pyvenv-%{python_version}
	
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
%{_isysroot}%{_rpmint_target_prefix}/include/python%{python_version}m
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
