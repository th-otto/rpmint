%define pkgname python2
%global python_version 2.7

%rpmint_header

Summary:        Python Interpreter
Name:           %{crossmint}%{pkgname}
Version:        2.7.14
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
Source2:        patches/python2/python2-python.csh
Source3:        patches/python2/python2-python.sh
Source4:        patches/python2/python2-pythonstart

Patch0:         patches/%{pkgname}/python2-2.7-dirs.patch
Patch1:         patches/python2/python2-distutils-rpm-8.patch
Patch2:         patches/python2/python2-2.7.5-multilib.patch
Patch3:         patches/python2/python2-2.5.1-sqlite.patch
Patch4:         patches/python2/python2-2.7.4-canonicalize2.patch
Patch5:         patches/python2/python2-2.6-gettext-plurals.patch
Patch6:         patches/python2/python2-2.6b3-curses-panel.patch
Patch7:         patches/python2/python2-sparc_longdouble.patch
Patch8:         patches/python2/python2-2.7.2-fix_date_time_compiler.patch
Patch9:         patches/python2/python2-bundle-lang.patch
Patch10:        patches/python2/python2-2.7-libffi-aarch64.patch
Patch11:        patches/python2/python2-bsddb6.diff
Patch12:        patches/python2/python2-2.7.9-ssl_ca_path.patch
Patch13:        patches/python2/python2-ncurses-6.0-accessors.patch
Patch14:        patches/python2/python2-reproducible.patch
Patch15:        patches/python2/python2-fix-shebang.patch
Patch16:        patches/python2/python2-skip_random_failing_tests.patch
Patch17:        patches/python2/python2-sorted_tar.patch
Patch18:        patches/python2/python2-path.patch
Patch19:        patches/python2/python2-mint.patch
Patch20:        patches/python2/python2-mintnosharedmod.patch
Patch21:        patches/python2/python2-mintsetupdist.patch
Patch22:        patches/python2/python2-math.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake

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
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

# drop Autoconf version requirement
sed -i 's/^version_required/dnl version_required/' configure.ac

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
	sh ./configure ${CONFIGURE_FLAGS}

	make %{?_smp_mflags}
	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make DESTDIR="${buildroot}" SYSROOT=%{_rpmint_sysroot} install

	make clean > /dev/null

	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias	

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	rm -f %{buildroot}%{_rpmint_bindir}/*-config

	chmod u+w %{buildroot}%{_rpmint_libdir}/*.a
	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_rpmint_libdir}$multilibdir
		mv %{buildroot}%{_rpmint_libdir}/*.a %{buildroot}%{_rpmint_libdir}$multilibdir
	fi
	
	# remove hard links and replace them with symlinks
	for dir in bin include lib ; do
	    rm -f ${buildroot}%{_rpmint_target_prefix}/$dir/python
	    ln -s python%{python_version} ${buildroot}%{_rpmint_target_prefix}/$dir/python
	done

	########################################
	# startup script
	########################################
	install -d -D -m 755 ${buildroot}/etc/profile.d
	install -m 644 %{S:4} ${buildroot}/etc/pythonstart
	install -m 644 %{S:3} ${buildroot}/etc/profile.d/python.sh
	install -m 644 %{S:2} ${buildroot}/etc/profile.d/python.csh

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
%{_isysroot}%{_rpmint_target_prefix}/lib/python
%{_isysroot}%{_rpmint_target_prefix}/lib/python%{python_version}
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/python
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
%doc README Doc


%changelog
* Sun Apr 09 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 2.7.14

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
