%define pkgname gimp

%rpmint_header

%define subver   1.2
%define with_perl 0

Summary: The GNU Image Manipulation Program
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version: 1.2.5
Release: 1
License: GPL-3.0-or-later
Group: Applications/Graphics
Source0: http://download.gimp.org/pub/%{pkgname}/v%{subver}/v%{version}/%{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/gimp/gimp-1.2.5-config.patch
Patch1:  patches/gimp/gimp-1.2.5-png.patch
Patch2:  patches/gimp/gimp-version.patch

Packager: Thorsten Otto <admin@tho-otto.de>
URL: http://www.gimp.org

%rpmint_essential
BuildRequires : autoconf
BuildRequires : automake
BuildRequires : libtool
BuildRequires:  pkgconfig
BuildRequires : make
BuildRequires : perl
%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
BuildRequires : cross-mint-glib-devel
BuildRequires : cross-mint-gtk+-devel >= 1.2.8
BuildRequires : cross-mint-libpng-devel
BuildRequires : cross-mint-libjpeg-devel
BuildRequires : cross-mint-tiff-devel
BuildRequires : cross-mint-gettext-runtime
Requires      : cross-mint-XFree86
Requires      : cross-mint-gtk+
%else
BuildRequires : XFree86-devel
BuildRequires : glib-devel
BuildRequires : gtk+-devel
BuildRequires : libpng-devel
BuildRequires : libjpeg-devel
BuildRequires : tiff-devel
BuildRequires : gettext-runtime
Requires      : XFree86
Requires      : gtk+
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

%rpmint_build_arch

%description
The GIMP (GNU Image Manipulation Program) is a powerful image
composition and editing program, which can be extremely useful for
creating logos and other graphics for Web pages.  The GIMP has many of
the tools and filters you would expect to find in similar commercial
offerings, and some interesting extras as well. The GIMP provides a
large image manipulation toolbox, including channel operations and
layers, effects, sub-pixel imaging and anti-aliasing, and conversions,
all with multi-level undo.

The GIMP includes a scripting facility, but many of the included
scripts rely on fonts that we cannot distribute.  The GIMP FTP site
has a package of fonts that you can install by yourself, which
includes all the fonts needed to run the included scripts.  Some of
the fonts have unusual licensing requirements; all the licenses are
documented in the package.  Get
ftp://ftp.gimp.org/pub/gimp/fonts/freefonts-0.10.tar.gz and
ftp://ftp.gimp.org/pub/gimp/fonts/sharefonts-0.10.tar.gz if you are so
inclined.  Alternatively, choose fonts which exist on your system
before running the scripts.

Install the GIMP if you need a powerful image manipulation
program. You may also want to install other GIMP packages:
gimp-libgimp if you're going to use any GIMP plug-ins and
gimp-data-extras, which includes various extra files for the GIMP.

%package devel
Summary: GIMP plugin and extension development kit
Group: 		Applications/Graphics
%if "%{buildtype}" == "cross"
Requires: 	cross-mint-gtk+-devel >= 1.2.8
%else
Requires: 	gtk+-devel >= 1.2.8
%endif
Requires: 	%{name} = %{version}
%description devel
The gimp-devel package contains the static libraries and header files
for writing GNU Image Manipulation Program (GIMP) plug-ins and
extensions.

Install gimp-devel if you're going to create plug-ins and/or
extensions for the GIMP.  You'll also need to install gimp-limpgimp
and gimp, and you may want to install gimp-data-extras.

%if %{with_perl}
%package perl
Summary: GIMP perl extensions and plugins.
Group:		Applications/Graphics
Requires:	%{name} = %{version}
Requires:	perl

%description perl
The gimp-perl package contains all the perl extensions and perl plugins. 
%endif

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

rm -f aclocal.m4 ltmain.sh ltconfig
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

%define sysconfdir /etc

COMMON_CFLAGS+=" -fno-strict-aliasing"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=%{sysconfdir}
	--disable-shared
	--disable-print
	%{expr: %{with_perl} ? "--enable-perl" : "--disable-perl"}
"
STACKSIZE="-Wl,-stack,512k"

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
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/gimp-config

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files for multilib
	%rpmint_remove_pkg_configs

	#
	# fix multilib layout of module & plug-ins
	#
	if test "$multilibdir" != ""; then
		mkdir -p %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir
		mv %{buildroot}%{_rpmint_libdir}$multilibdir/gimp/%{subver}/plug-ins/* %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir
		rmdir %{buildroot}%{_rpmint_libdir}$multilibdir/gimp/%{subver}/plug-ins
		mkdir -p %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/modules$multilibdir
		mv %{buildroot}%{_rpmint_libdir}$multilibdir/gimp/%{subver}/modules/* %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/modules$multilibdir
		rmdir %{buildroot}%{_rpmint_libdir}$multilibdir/gimp/%{subver}/modules
		rmdir %{buildroot}%{_rpmint_libdir}$multilibdir/gimp/%{subver}
		rmdir %{buildroot}%{_rpmint_libdir}$multilibdir/gimp
	fi

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir/*
		rmdir %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir
		rm -f %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/modules$multilibdir/*
		rmdir %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/modules$multilibdir
	else
		%{_rpmint_target_strip} %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir/* || :
		if test "$multilibdir" != ""; then
			mkdir -p %{buildroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/plug-ins
			mv %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir/* %{buildroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/plug-ins
			rmdir %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir
			mkdir -p %{buildroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/modules
			mv %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/modules$multilibdir/* %{buildroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/modules
			rmdir %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/modules$multilibdir
		fi
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_libdir}/gimp/%{subver}/plug-ins$multilibdir/* || :
	%endif

	make distclean
done

%install

%rpmint_cflags

%rpmint_strip_archives

# fix symlinks
rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp.1
rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimptool.1
rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp-remote.1
rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/gimprc.5
ln -sf gimp-%{subver}.1.gz %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp.1.gz
ln -sf gimptool-%{subver}.1.gz %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimptool.1.gz
ln -sf gimp-remote-%{subver}.1.gz %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp-remote.1.gz
ln -sf gimprc-%{subver}.5.gz %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/gimprc.5.gz

mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig
cat << EOF > %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/gimp-%{subver}.pc
prefix=%{_rpmint_target_prefix}
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
includedir=\${prefix}/include
gimpdatadir=\${prefix}/share/gimp/%{subver}
gimpplugindir=\${libdir}/gimp/%{subver}
libsnogui=-lgimp

Name: Gimp
Description: GNU Image Manipulation Program
Version: %{version}
Requires: gtk+
Libs: -lgimpui -lgimp
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


#
# This perl madness will drive me batty
#
touch gimp-perl
%if %{with_perl}
eval perl '-V:archname'
find %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/perl5 -type f -print | sed "s@^%{buildroot}@@g" | grep -v perllocal.pod > gimp-perl
%endif

#
# Plugins and modules change often (grab the executeable ones)
#
echo "%%defattr (0755, bin, bin)" > gimp-plugin-files
find %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver} -type f -exec file {} \; | grep -v perl | cut -d':' -f 1 | sed "s@^%{buildroot}@@g"  >>gimp-plugin-files

#
# Now pull the perl ones out.
#
echo "%%defattr (0755, bin, bin)" > gimp-perl-plugin-files
echo "%%dir %{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/plug-ins" >> gimp-perl-plugin-files
find %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver} -type f -exec file {} \; | grep perl | cut -d':' -f 1 | sed "s@^%{buildroot}@@g" >>gimp-perl-plugin-files

#
# Auto detect the lang files.
#
if [ -f /usr/lib/rpm/find-lang.sh ] ; then
 /usr/lib/rpm/find-lang.sh %{buildroot} %{pkgname}
 /usr/lib/rpm/find-lang.sh %{buildroot} gimp-libgimp
 /usr/lib/rpm/find-lang.sh %{buildroot} gimp-std-plugins
 /usr/lib/rpm/find-lang.sh %{buildroot} gimp-script-fu
 cat %{pkgname}.lang gimp-std-plugins.lang gimp-script-fu.lang \
    | sed "s:(644, root, root, 755):(644, bin, bin, 755):" > gimp-all.lang
fi

#
# Tips
#
echo "%%defattr (644, bin, bin, 755)" >gimp-tips-files
echo "%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/tips/gimp_tips.txt" >> gimp-tips-files
for I in `ls %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/tips/gimp*.[a-z]*.txt | sed "s@^%{buildroot}@@g"`; do
   tip_lang=`basename $I | cut -d'.' -f2`
   echo "%%lang($tip_lang)    $I" >> gimp-tips-files
done

#
# Build the master filelists generated from the above mess.
#
cat gimp-plugin-files gimp-all.lang gimp-tips-files > gimp.files
cat gimp-perl gimp-perl-plugin-files > gimp-perl-files


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


#%%post -p /sbin/ldconfig

#%%postun -p /sbin/ldconfig

%files -f gimp.files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog MAINTAINERS NEWS README TODO
%doc docs/*.txt ABOUT-NLS README.i18n README.perl README.win32
%dir %{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}
%dir %{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/tips
%dir %{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}
%dir %{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/modules
%dir %{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}/plug-ins

%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/brushes/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/fractalexplorer/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/gfig/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/gflare/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/gimpressionist/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/gradients/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/help/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/palettes/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/patterns/
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/scripts/

%{_isysroot}%{sysconfdir}/gimp/%{subver}/gimprc
%{_isysroot}%{sysconfdir}/gimp/%{subver}/gimprc_user
%{_isysroot}%{sysconfdir}/gimp/%{subver}/gtkrc
%{_isysroot}%{sysconfdir}/gimp/%{subver}/gtkrc_user
%{_isysroot}%{sysconfdir}/gimp/%{subver}/unitrc
%{_isysroot}%{sysconfdir}/gimp/%{subver}/ps-menurc

%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/gimp_logo.ppm
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/gimp_splash.ppm

%defattr (0755, bin, bin)
%{_isysroot}%{_rpmint_target_prefix}/share/gimp/%{subver}/user_install

#%%{_isysroot}%%{_rpmint_target_prefix}/lib/libgimp-%%{subver}.so.%%{microver}.0.0
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/libgimp-%%{subver}.so.%%{microver}
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/libgimpui-%%{subver}.so.%%{microver}.0.0
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/libgimpui-%%{subver}.so.%%{microver}
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/libgck-%%{subver}.so.%%{microver}.0.0
#%%{_isysroot}%%{_rpmint_target_prefix}/lib/libgck-%%{subver}.so.%%{microver}

%{_isysroot}%{_rpmint_target_prefix}/bin/gimp-%{subver}
%{_isysroot}%{_rpmint_target_prefix}/bin/gimp-remote-%{subver}
%{_isysroot}%{_rpmint_target_prefix}/bin/gimp
%{_isysroot}%{_rpmint_target_prefix}/bin/gimp-remote
%if %{with_perl}
%{_isysroot}%{_rpmint_target_prefix}/bin/gimpdoc-%{subver}
%{_isysroot}%{_rpmint_target_prefix}/bin/embedxpm-%{subver}
%{_isysroot}%{_rpmint_target_prefix}/bin/xcftopnm-%{subver}
%{_isysroot}%{_rpmint_target_prefix}/bin/gimpdoc
%{_isysroot}%{_rpmint_target_prefix}/bin/embedxpm
%{_isysroot}%{_rpmint_target_prefix}/bin/xcftopnm
%endif

%defattr (0644, bin, man)
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp-%{subver}.1.gz
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp.1.gz
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp-remote-%{subver}.1.gz
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimp-remote.1.gz
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/gimprc-%{subver}.5.gz
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/gimprc.5.gz


%files devel
%defattr(-, root, root)
%{_isysroot}%{_rpmint_target_prefix}/bin/gimptool-%{subver}
%{_isysroot}%{_rpmint_target_prefix}/bin/gimptool
%{_isysroot}%{_rpmint_target_prefix}/include/libgimp/
%{_isysroot}%{_rpmint_target_prefix}/include/gck/
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%dir %{_isysroot}%{_rpmint_target_prefix}/lib/gimp/%{subver}
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/gimp.m4
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimptool-%{subver}.1.gz
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gimptool.1.gz
%{_isysroot}%{_rpmint_target_prefix}/share/gimp
%{_isysroot}%{_rpmint_target_prefix}/share/locale/*/*/gimp-libgimp*
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif

%if %{with_perl}
%files perl -f gimp-perl-files
%endif

%changelog
* Sat Mar 25 2023 Thorsten Otto <admin@tho-otto.de>
- New RPMint spec file
