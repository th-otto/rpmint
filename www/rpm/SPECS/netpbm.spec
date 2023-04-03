%define pkgname netpbm

%rpmint_header

Summary:        A Graphics Conversion Package
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        10.91.1
Release:        1
License:        BSD-3-Clause AND GPL-2.0-or-later AND IJG AND MIT
Group:          Productivity/Graphics/Convertors

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://netpbm.sourceforge.net/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Source2: %{pkgname}-jpeg-to-pnm.fpi
Source3: %{pkgname}-pnm-to-ps.fpi
Source4: %{pkgname}-bmp-to-pnm.fpi
Source5: %{pkgname}-gif-to-pnm.fpi
Source6: %{pkgname}-rast-to-pnm.fpi
Source7: %{pkgname}-tiff-to-pnm.fpi
Source8: %{pkgname}-png-to-pnm.fpi

Patch0: patches/%{pkgname}/netpbm-0000-make.patch
Patch1: patches/%{pkgname}/netpbm-0003-tmpfile.patch
Patch2: patches/%{pkgname}/netpbm-0004-security-code.patch
Patch3: patches/%{pkgname}/netpbm-0005-security-scripts.patch
Patch4: patches/%{pkgname}/netpbm-0006-gcc-warnings.patch
Patch5: patches/%{pkgname}/netpbm-0007-makeman-py3.patch
Patch6: patches/%{pkgname}/netpbm-0008-signed-char.patch
Patch7: patches/%{pkgname}/netpbm-0009-big-endian.patch
Patch8: patches/%{pkgname}/netpbm-0010-disable-jasper.patch
Patch9: patches/%{pkgname}/netpbm-0012-mint.patch
Patch10: patches/%{pkgname}/netpbm-namespace.patch

%rpmint_essential
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-libjpeg-devel
BuildRequires:  cross-mint-libtiff-devel
BuildRequires:  cross-mint-libpng-devel
Provides:       cross-mint-libnetpbm-devel
%else
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
Provides:       libnetpbm-devel
%endif

%rpmint_build_arch

%description
These are the Portable Bitmap Plus Utilities.

This package provides tools for graphics conversion. Using these
tools, images can be converted from virtually any format into any
other format. A few of the supported formats include: GIF,
PC-Paintbrush, IFF ILBM, Gould Scanner file, MTV ray tracer, Atari
Degas .pi1 and .pi3, Macintosh PICT, HP Paintjet file, QRT raytracer,
AUTOCAD slide, Atari Spectrum (compressed and uncompressed), Andrew
Toolkit raster object, and many more. On top of that, man pages are
included for all tools.

%package devel
Summary       : Development tools for programs which will use the netpbm libraries.
Group         : Development/Libraries
Requires      : %{name} = %{version}
%if "%{buildtype}" == "cross"
Requires      :  cross-mint-libjpeg-devel
Requires      :  cross-mint-libtiff-devel
Requires      :  cross-mint-libpng-devel
%else
Requires      :  libjpeg-devel
Requires      :  libtiff-devel
Requires      :  libpng-devel
%endif

%description devel
The netpbm-devel package contains the header files and static libraries,
etc., for developing programs which can handle the various graphics file
formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries.


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
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $LTO_CFLAGS"
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -lm ${STACKSIZE}"


	# netpbm has _interactive_ configure perl script
	cp config.mk.in config.mk # recomended by upstream, see doc/INSTALL
	sed -i 's:NETPBMLIBTYPE = unixshared:NETPBMLIBTYPE = unixstatic:' config.mk
	sed -i 's:NETPBMLIBSUFFIX = so:NETPBMLIBSUFFIX = a:' config.mk
	sed -i 's:TIFFLIB = -ltiff:TIFFLIB = -ltiff -llzma -lzstd:' config.mk
	sed -i 's:PNGLIB = NONE:PNGLIB = -lpng -lz:' config.mk
	sed -i 's:STRIPFLAG = -s:STRIPFLAG =:' config.mk

	sed -i "s:CC = cc:CC = ${TARGET}-gcc:" config.mk
	sed -i "s:AR = ar:AR = ${TARGET}-ar:" config.mk
	sed -i "s:RANLIB = ranlib:RANLIB = ${TARGET}-ranlib:" config.mk
	sed -i "s:\#CFLAGS= -O2 -std1:CFLAGS = $CFLAGS:" config.mk
	sed -i "s:\#LDFLAGS += -noshare:LDFLAGS = $LDFLAGS:" config.mk
	sed -i 's:CC_FOR_BUILD = \$(CC):CC_FOR_BUILD = gcc:' config.mk
	sed -i 's:LD_FOR_BUILD = \$(LD):LD_FOR_BUILD = gcc:' config.mk
	sed -i 's:CFLAGS_FOR_BUILD = \$(CFLAGS_CONFIG):CFLAGS_FOR_BUILD = :' config.mk
	sed -i 's:LDFLAGS_FOR_BUILD = \$(LDFLAGS):LDFLAGS_FOR_BUILD = :' config.mk

	make %{?_smp_mflags}

	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/pkgconfig
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/include/%{pkgname}
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/%{pkgname}
	rm -rf package
	make pkgdir=`pwd`/package package
	
	rm -f package/bin/g3topbm # conflict with g3utils
	# rm -f package/bin/pstopnm # disable due security reasons, e. g. [bsc#1105592]
	mv  package/bin/* 		%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	mv	package/staticlink/*.a 	%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir
	mv	package/misc/* 		%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/%{pkgname}

	sed -e "s/@VERSION@/%{version}/" -e 's/-I@INCLUDEDIR@//' -e 's/-L@LINKDIR@//' package/pkgconfig_template > %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/pkgconfig/%{pkgname}.pc
	
	cp -prd package/include/%{pkgname}/. %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/include/%{pkgname}
	
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters
	install -m 755 %{S:2} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/jpeg-to-pnm.fpi
	install -m 755 %{S:3} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/pnm-to-ps.fpi
	install -m 755 %{S:4} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/bmp-to-pnm.fpi
	install -m 755 %{S:5} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/gif-to-pnm.fpi
	install -m 755 %{S:6} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/rast-to-pnm.fpi
	install -m 755 %{S:7} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/tiff-to-pnm.fpi
	install -m 755 %{S:8} %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/png-to-pnm.fpi

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
%doc doc/COPYRIGHT.PATENT doc/GPL_LICENSE.txt doc/HISTORY README doc/USERDOC
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/lib/rhs/rhs-printfilters/*.fpi
%{_isysroot}%{_rpmint_target_prefix}/share/%{pkgname}/*

%files devel
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif


%changelog
* Sun Apr 02 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 10.91.1

* Sun Dec 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
