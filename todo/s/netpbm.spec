Summary       : A library for handling different graphics file formats.
Name          : netpbm
Version       : 9.5
Release       : 1
Copyright     : freeware
Group         : System Environment/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://download.sourceforge.net/pub/sourceforge/netpbm/

BuildRequires : libjpeg-devel, libtiff-devel, libpng

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://download.sourceforge.net/pub/sourceforge/netpbm/netpbm-%{version}.tgz
Source1: jpeg-to-pnm.fpi
Source2: pnm-to-ps.fpi
Source3: bmp-to-pnm.fpi
Source4: gif-to-pnm.fpi
Source5: rast-to-pnm.fpi
Source6: tiff-to-pnm.fpi
Source7: png-to-pnm.fpi
Patch0:  netpbm-9.5-install.patch
Patch1:  netpbm-9.5-pktopbm.patch
Patch2:  netpbm-9.5-pnmtotiff.patch
Patch3:  netpbm-9.5-pstopnm.patch
Patch4:  netpbm-9.5-lsocket.patch
Patch5:  netpbm-9.5-namespace.patch
Patch6:  netpbm-9.5-staticlib.patch


%description
The netpbm package contains a library of functions which support
programs for handling various graphics file formats, including .pbm
(portable bitmaps), .pgm (portable graymaps), .pnm (portable anymaps),
.ppm (portable pixmaps) and others.

%package devel
Summary       : Development tools for programs which will use the netpbm libraries.
Group         : Development/Libraries
#Requires      : netpbm = %{version}
Requires      : libjpeg-devel, libtiff-devel, libpng

%description devel
The netpbm-devel package contains the header files and static libraries,
etc., for developing programs which can handle the various graphics file
formats supported by the netpbm libraries.

Install netpbm-devel if you want to develop programs for handling the
graphics file formats supported by the netpbm libraries.
#You'll also need to have the netpbm package installed.

%package progs
Summary       : Tools for manipulating graphics files in netpbm supported formats.
Group         : Applications/Multimedia
#Requires      : netpbm = %{version}

%description progs
The netpbm-progs package contains a group of scripts for manipulating the
graphics files in formats which are supported by the netpbm libraries.  For
example, netpbm-progs includes the rasttopnm script, which will convert a
Sun rasterfile into a portable anymap.  Netpbm-progs contains many other
scripts for converting from one graphics file format to another.

If you need to use these conversion scripts, you should install
netpbm-progs.
#You'll also need to install the netpbm package.


%prep
%setup -q
%patch0 -p1 -b .install
%patch1 -p1 -b .pktopbm
%patch2 -p1 -b .pnmtotiff
%patch3 -p1 -b .pstopnm
%patch4 -p1 -b .lsocket
%patch5 -p1 -b .namespace
%patch6 -p1 -b .staticlib


%build
make \
	CC=gcc \
	CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" \
	STATICLIB=Y \
	JPEGINC_DIR=%{_prefix}/include \
	PNGINC_DIR=%{_prefix}/include \
	TIFFINC_DIR=%{_prefix}/include \
	JPEGLIB_DIR=%{_prefix}/lib \
	PNGLIB_DIR=%{_prefix}/lib \
	TIFFLIB_DIR=%{_prefix}/lib


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

PATH="`pwd`:${PATH}" make install \
	CC=gcc \
	CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" \
	STATICLIB=Y \
	JPEGINC_DIR=${RPM_BUILD_ROOT}%{_prefix}/include \
	PNGINC_DIR=${RPM_BUILD_ROOT}%{_prefix}/include \
	TIFFINC_DIR=${RPM_BUILD_ROOT}%{_prefix}/include \
	JPEGLIB_DIR=%{_prefix}/lib \
	PNGLIB_DIR=%{_prefix}/lib \
	TIFFLIB_DIR=%{_prefix}/lib \
	INSTALL_PREFIX=${RPM_BUILD_ROOT}%{_prefix} \
	INSTALLBINARIES=${RPM_BUILD_ROOT}%{_prefix}/bin \
	INSTALLHDRS=${RPM_BUILD_ROOT}%{_prefix}/include \
	INSTALLLIBS=${RPM_BUILD_ROOT}%{_prefix}/lib \
	INSTALLMANUALS1=${RPM_BUILD_ROOT}%{_prefix}/share/man/man1 \
	INSTALLMANUALS3=${RPM_BUILD_ROOT}%{_prefix}/share/man/man3 \
	INSTALLMANUALS5=${RPM_BUILD_ROOT}%{_prefix}/share/man/man5

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/rhs/rhs-printfilters
for filter in $RPM_SOURCE_DIR/*.fpi ; do
    install -m755 $filter \
	${RPM_BUILD_ROOT}%{_prefix}/lib/rhs/rhs-printfilters
done

# Install header files.
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include
install -m644 pbm/pbm.h ${RPM_BUILD_ROOT}%{_prefix}/include/
install -m644 pbmplus.h ${RPM_BUILD_ROOT}%{_prefix}/include/
install -m644 pgm/pgm.h ${RPM_BUILD_ROOT}%{_prefix}/include/
install -m644 pnm/pnm.h ${RPM_BUILD_ROOT}%{_prefix}/include/
install -m644 ppm/ppm.h ${RPM_BUILD_ROOT}%{_prefix}/include/

# Install the static-only librle.a
install -m644 urt/{rle,rle_config}.h ${RPM_BUILD_ROOT}%{_prefix}/include/
install -m644 urt/librle.a ${RPM_BUILD_ROOT}%{_prefix}/lib/

# Fixup symlinks.
ln -sf gemtopnm ${RPM_BUILD_ROOT}%{_prefix}/bin/gemtopbm
ln -sf pnmtoplainpnm ${RPM_BUILD_ROOT}%{_prefix}/bin/pnmnoraw

# Fixup perl paths in the two scripts that require it.
perl -pi -e 's^/bin/perl^%/usr/bin/perl^' \
${RPM_BUILD_ROOT}%{_prefix}/bin/{ppmfade,ppmshadow}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,root)
%doc COPYRIGHT.PATENT GPL_LICENSE.txt HISTORY README README.CONFOCAL
%{_prefix}/include/*.h
%{_prefix}/lib/lib*.a
%{_prefix}/share/man/man3/*

%files progs
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/lib/rhs/rhs-printfilters/jpeg-to-pnm.fpi
%{_prefix}/lib/rhs/rhs-printfilters/pnm-to-ps.fpi
%{_prefix}/lib/rhs/rhs-printfilters/bmp-to-pnm.fpi
%{_prefix}/lib/rhs/rhs-printfilters/gif-to-pnm.fpi
%{_prefix}/lib/rhs/rhs-printfilters/rast-to-pnm.fpi
%{_prefix}/lib/rhs/rhs-printfilters/tiff-to-pnm.fpi
%{_prefix}/lib/rhs/rhs-printfilters/png-to-pnm.fpi
%{_prefix}/share/man/man1/*
%{_prefix}/share/man/man5/*


%changelog
* Sun Dec 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
