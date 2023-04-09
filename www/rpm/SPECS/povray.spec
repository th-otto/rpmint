%define pkgname povray

%rpmint_header

Summary:        Ray Tracer
Name:           %{crossmint}%{pkgname}
Version:        3.6.1
Release:        1
License:        AGPL-3.0 and CC-BY-SA-3.0
Group:          Productivity/Graphics/Visualization/Raytracers

Packager:       %{packager}
URL:            http://www.povray.org

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub

Patch0: patches/povray/povray36-autoconf.patch

%rpmint_essential
BuildRequires:  make
BuildRequires:  ncurses-devel

%rpmint_build_arch

%description
The Persistence of Vision Ray tracer creates three-dimensional,
photo-realistic images using a rendering technique called ray tracing.
It reads in a text file containing information describing the objects
and lighting in a scene and generates an image of that scene from the
view point of a camera also described in the text file. Ray tracing is
not a fast process by any means, (the generation of a complex image can
take several hours) but it produces very high quality images with
realistic reflections, shading, perspective, and other effects.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

rm -f aclocal.m4 ltmain.sh
aclocal
autoconf
autoheader
automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cd libraries/png
aclocal
autoconf
autoheader
automake --foreign --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig
cd ../..

cd libraries/zlib
aclocal
autoconf
autoheader
automake --foreign --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig
cd ../..

# autoreconf may have overwritten config.sub
cp %{S:1} config/config.sub

cp -a config/config.sub libraries/zlib/config.sub
cp -a config/config.sub libraries/png/config.sub
cp -a config/config.sub libraries/jpeg/config.sub
cp -a config/config.sub libraries/tiff/config.sub

# hack jpeg library configure script
sed -i "s|export CFLAGS|CC=%{_rpmint_target_gcc}; AR=%{_rpmint_target_ar}; RANLIB=%{_rpmint_target_ranlib}; export CFLAGS CC AR RANLIB|" "libraries/jpeg/configure.gnu"
sed -i "s|AR= ar rc|AR = %{_rpmint_target_ar} rcs|" "libraries/jpeg/makefile.cfg"

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-lib-checks
"
STACKSIZE="-Wl,-stack,256k"

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
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	COMPILED_BY="Thorsten Otto for MiNT" \
	CC="%{_rpmint_target_gcc}" \
	AR="%{_rpmint_target_ar}" \
	RANLIB="%{_rpmint_target_ranlib}"

	make %{?_smp_mflags} || exit 1
	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" install || exit 1
	make distclean

	# --docdir cannot be passed to top level configure script,
	# because some scripts in sub-directories bail on that
	# Fix that here.
	if ! test -d %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}-3.6; then
		mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages
		mv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}-3.6 %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}-3.6
	fi

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif
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
%license COPYING
%doc README AUTHORS ChangeLog NEWS
%config %{_isysroot}/etc/povray/3.6/povray.conf
%config %{_isysroot}/etc/povray/3.6/povray.ini
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Sun Apr 09 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
