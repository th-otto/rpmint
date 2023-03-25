%define pkgname freetype2

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

Summary       : A free and portable TrueType font rendering engine.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 2.8.1
Release       : 2
License       : GPL-2.0-or-later
Group         : System Environment/Libraries

%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-libpng-devel
BuildRequires : cross-mint-zlib-devel
BuildRequires : cross-mint-libbz2-devel
Provides      : cross-mint-freetype2-devel = %{version}
%else
BuildRequires : libpng-devel
BuildRequires : zlib-devel
BuildRequires : libbz2-devel
Provides      : freetype2-devel = %{version}
%endif

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : http://www.freetype.org/

Obsoletes     : freetype-demo < %{version}
Conflicts     : freetype-demo < %{version}

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
Source3: patches/automake/mintelf-config.sub
Patch0:  patches/{%pkgname}/freetype2-bugzilla-308961-cmex-workaround.patch
Patch1:  patches/{%pkgname}/freetype2-static-config.patch
Patch2:  patches/{%pkgname}/freetype2-demos.patch

%rpmint_build_arch


%description
The FreeType engine is a free and portable TrueType font rendering
engine. It has been developed to provide TrueType support to a great
variety of platforms and environments.

Note that FreeType is a *library*. It is not a font server for your
favorite platform, even though it was designed to be used in many of
them. Note also that it is *not* a complete text-rendering library.
Its purpose is simply to open and manage font files, as well as load,
hint and render individual glyphs efficiently. You can also see it as
a "TrueType driver" for a higher-level library, though rendering text
with it is extremely easy, as demo-ed by the test programs.

%package devel
Summary       : A free and portable TrueType font rendering engine.
Group         : System Environment/Libraries
Requires      : %{name} = %{version}

%description devel
The FreeType engine is a free and portable TrueType font rendering
engine. It has been developed to provide TrueType support to a great
variety of platforms and environments.

Note that FreeType is a *library*. It is not a font server for your
favorite platform, even though it was designed to be used in many of
them. Note also that it is *not* a complete text-rendering library.
Its purpose is simply to open and manage font files, as well as load,
hint and render individual glyphs efficiently. You can also see it as
a "TrueType driver" for a higher-level library, though rendering text
with it is extremely easy, as demo-ed by the test programs.

This package includes the header files documentations and libraries
necessary to develop applications that use freetype.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -b 1 -a 2 -n freetype-%{version}
%patch0 -p1
%patch1 -p1
cd ft2demos-%{version}
%patch2 -p1
cd ..

cp "%{S:3}" builds/unix/config.sub

%build
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%rpmint_cflags

COMMON_CFLAGS+=" -std=gnu99 -D_GNU_SOURCE"

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--with-bzip2
	--with-png
	--with-zlib
	--disable-shared
	--enable-static
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/freetype-config
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/freetype-config.1

	make -C ft2demos-%{version} TOP_DIR=.. AR=%{_rpmint_target}-ar

	install -m 755 ft2demos-%{version}/bin/ftbench  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftdump   %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftlint   %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ttdebug  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftdiff   %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftgamma  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftgrid   %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftmulti  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftstring %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	install -m 755 ft2demos-%{version}/bin/ftview   %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin

	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
	%endif
	
	make -C ft2demos-%{version} TOP_DIR=.. clean
	make clean
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
%doc docs
%{_isysroot}%{_rpmint_target_prefix}/bin/ftbench
%{_isysroot}%{_rpmint_target_prefix}/bin/ftdump
%{_isysroot}%{_rpmint_target_prefix}/bin/ftlint
%{_isysroot}%{_rpmint_target_prefix}/bin/ttdebug
%{_isysroot}%{_rpmint_target_prefix}/bin/ftdiff
%{_isysroot}%{_rpmint_target_prefix}/bin/ftgamma
%{_isysroot}%{_rpmint_target_prefix}/bin/ftgrid
%{_isysroot}%{_rpmint_target_prefix}/bin/ftmulti
%{_isysroot}%{_rpmint_target_prefix}/bin/ftstring
%{_isysroot}%{_rpmint_target_prefix}/bin/ftview

%files devel
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/freetype2.m4
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}/*.pc
%endif


%changelog
* Fri Mar 24 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 2.8.1

* Tue Jul 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0.4, dropped old 1.x libs

* Fri Mar 16 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0 and 1.4

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- correct Packager and Vendor
- added Summary(de)
