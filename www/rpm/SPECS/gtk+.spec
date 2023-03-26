%define pkgname gtk+

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

Summary       : The GIMP ToolKit (GTK+), a library for creating GUIs for X.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 1.2.8
Release       : 2
License       : LGPL
Group         : Development/Libraries

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : http://www.gtk.org/

%rpmint_essential
BuildRequires : autoconf
BuildRequires : automake
BuildRequires : libtool
BuildRequires : make
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
BuildRequires : cross-mint-glib-devel
Requires      : cross-mint-XFree86
Requires      : cross-mint-glib
Provides      : cross-mint-gtk+-devel = %{version}
%else
Prereq        : /sbin/install-info
BuildRequires : XFree86-devel
BuildRequires : glib-devel
Requires      : XFree86
Requires      : glib
Provides      : gtk+-devel = %{version}
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gimp.org/pub/gtk/v1.2/%{pkgname}-%{version}.tar.gz
Source1: gtkrc-default
Source2: patches/automake/mintelf-config.sub
Source3: patches/gtk/gtk-acinclude.m4
Patch0:  patches/gtk/gtk+-1.2.8-mint-x11.patch
Patch1:  patches/gtk/gtk+-1.2.8-configure.patch
Patch2:  patches/gtk/gtk+-1.2.8-fontsel.patch

%rpmint_build_arch


%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

Install gtk+-devel if you need to develop GTK+ applications.  You'll also
need to install the gtk+ package.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -n %{pkgname}-%{version} -q
# better we fix the xserver font things
#%%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -f aclocal.m4 acinclude.m4 ltmain.sh ltconfig
cp %{S:3} acinclude.m4
rm -rf autom4te.cache
libtoolize --force || exit 1
aclocal || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache
rm -f config.sub
cp %{S:2} config.sub


%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--with-xinput=xfree
	--enable-debug=no
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
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/gtk-config
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/gtk-config.1*


	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilib
	%rpmint_remove_pkg_configs
	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done


%install

%rpmint_cflags

%rpmint_strip_archives

mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig

cat << EOF > %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/gtk+.pc
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: GTK+
Description: GIMP Tool Kit
Version: %{version}
Requires: gdk
Libs: -lgtk
Cflags: 
EOF

cat << EOF > %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/gdk.pc
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include

Name: GDK
Description: GIMP Drawing Kit
Version: %{version}
Requires: glib
Libs: -lgdk -lXext -lX11 -lm
Cflags: -I\${includedir}/gtk-1.2
EOF

install -m 444 %{SOURCE1} %{buildroot}%{_isysroot}/etc/gtk/gtkrc

# i18n garbage with this one.
rm -f %{buildroot}%{_isysroot}/etc/gtk/gtkrc

cat > %{buildroot}%{_isysroot}/etc/gtk/gtkrc << EOF
style "gtk-tooltips-style" {
  bg[NORMAL] = "#ffffc0"
}

widget "gtk-tooltips" style "gtk-tooltips-style"
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


%if "%{buildtype}" != "cross"
%post
/sbin/install-info %{_rpmint_target_prefix}/share/info/gdk.info.gz %{_rpmint_target_prefix}/share/info/dir --entry="* gdk: (gtk+).                                  GDK, the General Drawing Kit."
/sbin/install-info %{_rpmint_target_prefix}/share/info/gtk.info.gz %{_rpmint_target_prefix}/share/info/dir --entry="* gtk: (gtk+).                                  GTK, the GIMP Toolkit."

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_rpmint_target_prefix}/share/info/gdk.info.gz %{_rpmint_target_prefix}/share/info/dir --entry="* gdk: (gtk+).                                  GDK, the General Drawing Kit."
  /sbin/install-info --delete %{_rpmint_target_prefix}/share/info/gtk.info.gz %{_rpmint_target_prefix}/share/info/dir --entry="* gtk: (gtk+).                                  GTK, the GIMP Toolkit."
fi
%endif


%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%doc docs/html
%config(noreplace) %{_isysroot}/etc/gtk/gtkrc
%config %{_isysroot}/etc/gtk/gtkrc.*
%{_isysroot}%{_rpmint_target_prefix}/share/themes/Default
%{_isysroot}%{_rpmint_target_prefix}/share/locale/*/*/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif


%changelog
* Sat Mar 25 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
