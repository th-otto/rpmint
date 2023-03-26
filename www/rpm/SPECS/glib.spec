%define pkgname glib

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

# Note that this is NOT a relocatable package

Summary: Handy library of utility functions
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version: 1.2.8
Release: 2
License: LGPL
Group: Libraries
Source0: https://download.gnome.org/sources/%{pkgname}/1.2/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/glib/glib-1.2.8-configure.patch
Patch1:  patches/glib/glib-1.2.8-inline.patch

Packager: Thorsten Otto <admin@tho-otto.de>
URL: http://www.gtk.org

%rpmint_essential
BuildRequires : autoconf
BuildRequires : automake
BuildRequires : libtool
BuildRequires : make
%if "%{buildtype}" == "cross"
Provides      : cross-mint-glib-devel = %{version}
%else
Provides      : glib-devel = %{version}
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

%rpmint_build_arch

%description
Handy library of utility functions. Development libs and headers
files.
#are in glib-devel.
#
#%#package devel
#Summary: GIMP Toolkit and GIMP Drawing Kit support library
#Group: X11/Libraries
#
#%#description devel
#Static libraries and header files for the support library for the GIMP's X
#libraries, which are available as public libraries.  GLIB includes generally
#useful data structures.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

rm -f aclocal.m4 acinclude.m4 ltmain.sh ltconfig
rm -rf autom4te.cache
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache
rm -f config.sub
cp %{S:1} config.sub

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--with-threads=none
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make # %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/glib-config
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/glib-config.1*

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilib
	%rpmint_remove_pkg_configs
	# remove obsolete glibconfig.h for multilib
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/*/glib/include/glibconfig.h
	rmdir %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/*/glib/include || :
	rmdir %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/*/glib || :

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif

	make distclean
done

%install

%rpmint_cflags

%rpmint_strip_archives

mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig

# move glibconfig.h
mv %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/glib/include/glibconfig.h %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/include/glib-1.2
rmdir %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/glib/include || :
rmdir %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/glib || :

cat << EOF > %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/glib.pc
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: GLib
Description: C Utility Library
Version: %{version}
Libs: -lglib
Cflags: -I\${includedir}/glib-1.2
EOF

cat << EOF > %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/gmodule.pc
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: GModule
Description: Dynamic module loader for GLib
Requires: glib
Version: %{version}
Libs: -lgmodule
Cflags:
EOF

cat << EOF > %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/gthread.pc
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: GThread
Description: Thread support for GLib
Requires: glib
Version: %{version}
Libs: -lgthread
Cflags:
EOF

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

#%#post -p /sbin/ldconfig

#%#postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
#%#{prefix}/lib/libglib-1.2.so.*
#%#{prefix}/lib/libgthread-1.2.so.*
#%#{prefix}/lib/libgmodule-1.2.so.*

#%#files devel
#%#defattr(-, root, root)
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/lib*.so
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif

%changelog
* Sat Mar 25 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Jul 06 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
