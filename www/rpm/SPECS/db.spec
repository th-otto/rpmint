%define pkgname db

%rpmint_header

Summary:        Berkeley DB Database Library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        4.8.30
Release:        1
License:        BSD-3-Clause
Group:          System/Libraries

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://oracle.com/technetwork/products/berkeleydb/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/db/db-%{version}.patch
Patch1:  patches/db/db-rpm-no-fsync.patch
Patch2:  patches/db/db-malloc-align.patch
Patch3:  patches/db/db-lockstub.patch
Patch4:  patches/db/db-thread.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
Provides:       %{name}-devel = %{version}

%rpmint_build_arch

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
Berkeley DB includes B+tree, Extended Linear Hashing, Fixed and Variable-length
record access methods, transactions, locking, logging, shared memory caching
and database recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation for
building programs which use Berkeley DB.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

cd dist
./s_config
rm -f config.sub
cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -fno-strict-aliasing"
STACKSIZE="-Wl,-stack,256k"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-compat185
	--disable-dump185
	--disable-mutexsupport
"

cd build_unix

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"../dist/configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make DESTDIR="${buildroot}" install

	# Fix header file installation
	if ! test -d ${buildroot}%{_rpmint_target_prefix}/include/db4; then
		mkdir -p ${buildroot}%{_rpmint_target_prefix}/include/db4
		mv ${buildroot}%{_rpmint_target_prefix}/include/*.h ${buildroot}%{_rpmint_target_prefix}/include/db4
	fi
	rm -f ${buildroot}%{_rpmint_target_prefix}/include/{db,db_185,db_cxx}.h
	chmod 644 ${buildroot}%{_rpmint_target_prefix}/include/db4/*.h
	echo "#include <db4/db.h>" > ${buildroot}%{_rpmint_target_prefix}/include/db.h
	echo "#include <db4/db_185.h>" > ${buildroot}%{_rpmint_target_prefix}/include/db_185.h
	echo "#include <db4/db_cxx.h>" > ${buildroot}%{_rpmint_target_prefix}/include/db_cxx.h
	
	# remove dangling tags symlink from examples.
	cd ..
	rm -f examples_cxx/tags
	rm -f examples_c/tags

	# Move documentation to the right directory
	if test ! -d ${buildroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}; then
		mkdir -p ${buildroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}
		mv ${buildroot}%{_rpmint_target_prefix}/docs/* ${buildroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}
		cp -a examples_cxx examples_c ${buildroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}
		cp -a LICENSE README ${buildroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}
	fi
	rm -rf ${buildroot}%{_rpmint_target_prefix}/docs

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	chmod 755 ${buildroot}%{_rpmint_target_prefix}/bin/*

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif

	cd build_unix
	make distclean
done


%install

%rpmint_cflags

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
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}



%changelog
* Wed Mar 29 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.8.30

* Wed Dec 13 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
