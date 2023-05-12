%define pkgname wget

%rpmint_header

Summary:        Retrieve files from the World Wide Web using HTTP and FTP
Name:           %{crossmint}%{pkgname}
Version:        1.21.3
Release:        1
License:        GPL-3.0-or-later
Group:          Applications/Networking

Packager:       %{packager}
URL:            https://www.gnu.org/software/sed/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/wget/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/wget/wget-wgetrc.patch
Patch1: patches/wget/wget-libproxy.patch
Patch2: patches/wget/wget-1.14-no-ssl-comp.patch
Patch3: patches/wget/wget-fix-pod-syntax.patch
Patch4: patches/wget/wget-errno-clobber.patch
Patch5: patches/wget/wget-remove-env-from-shebang.patch
Patch6: patches/wget/wget-do-not-propagate-credentials.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  pkgconfig(%{crossmint}openssl)
BuildRequires:  %{crossmint}c-ares-devel

%rpmint_build_arch

%description
Wget enables you to retrieve WWW documents or FTP files from a server.
This can be done in script files or via the command line.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--disable-threads
	--config-cache
	--with-ssl=openssl
	--with-cares
	--without-metalink
"
STACKSIZE="-Wl,-stack,128k"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
EOF
	%rpmint_append_gnulib_cache
}

build_dir=`pwd`

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	cd "$build_dir"

	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	sed -i 's/\/usr\/bin\/env perl -w/\/usr\/bin\/perl -w/' util/rmold.pl

	echo '#undef HAVE_PTHREAD_H' >> src/config.h
	echo "#undef HAVE_PTHREAD_API" >> src/config.h
	echo "#undef HAVE_PTHREAD_MUTEX_RECURSIVE" >> src/config.h
	echo "#undef HAVE_PTHREAD_RWLOCK" >> src/config.h
	echo "#undef SIZEOF_PTHREAD_MUTEX_T" >> src/config.h
	echo "#undef USE_POSIX_THREADS" >> src/config.h
	echo "#undef SETLOCALE_NULL_ALL_MTSAFE" >> src/config.h
	echo "#define SETLOCALE_NULL_ALL_MTSAFE 1" >> src/config.h
	echo "#undef SETLOCALE_NULL_ONE_MTSAFE" >> src/config.h
	echo "#define SETLOCALE_NULL_ONE_MTSAFE 1" >> src/config.h
	
	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	cd "$build_dir"
	make clean >/dev/null
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
%license COPYING*
%doc AUTHORS COPYING ChangeLog MAILING-LIST NEWS README
%doc doc/sample.wgetrc util/rmold.pl
%config(noreplace) %{_isysroot}/etc/wgetrc
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share



%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}


%changelog
* Thu May 11 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.21.3

* Mon Dec 08 2003 Adam Klobukowski <atari@gabo.pl>
- updated to version 1.9.1

* Thu Oct 23 2003 Adam Klobukowski <atari@gabo.pl>
- updated to version 1.9

* Wed Dec 26 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 1.8.1

* Mon Jul 09 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 1.7

* Sat Mar 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to version 1.6
