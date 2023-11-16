%define pkgname libexif

%rpmint_header

Summary:        An EXIF Tag Parsing Library for Digital Cameras
Name:           %{crossmint}%{pkgname}
Version:        0.6.22
Release:        1
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://libexif.sourceforge.net

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://github.com/libexif/libexif/releases/download/libexif-0_6_22-release/%{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/libexif/libexif-build-date.patch
Patch1:  patches/libexif/libexif-shared.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make

%rpmint_build_arch

%description
This library is used to parse EXIF information from JPEGs created by
digital cameras.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

cp %{S:1} config.sub

cd libexif
	
mv exif-byte-order.h exifbyte.h ; ln -s exifbyte.h exif-byte-order.h
mv exif-content.h    exifcont.h ; ln -s exifcont.h exif-content.h
mv exif-data.h       exifdata.h ; ln -s exifdata.h exif-data.h
mv exif-data-type.h  exiftype.h ; ln -s exiftype.h exif-data-type.h
mv exif-entry.h      exifent.h  ; ln -s exifent.h  exif-entry.h
mv exif-format.h     exifform.h ; ln -s exifform.h exif-format.h
mv exif-ifd.h        exififd.h  ; ln -s exififd.h  exif-ifd.h
mv exif-loader.h     exifload.h ; ln -s exifload.h exif-loader.h
mv exif-log.h        exiflog.h  ; ln -s exiflog.h  exif-log.h
mv exif-mem.h        exifmem.h  ; ln -s exifmem.h  exif-mem.h
mv exif-mnote-data.h exifnote.h ; ln -s exifnote.h exif-mnote-data.h
mv exif-tag.h        exiftag.h  ; ln -s exiftag.h  exif-tag.h
mv exif-utils.h      exifutil.h ; ln -s exifutil.h exif-utils.h

%build

export LANG=POSIX
export LC_ALL=POSIX

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} --with-doc-dir=%{_rpmint_target_prefix}/share/doc/%{pkgname} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-nls
	--disable-shared
"

STACKSIZE="-Wl,-stack,128k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	cwd=`pwd`
	cd "%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/include/libexif"

mv exif-byte-order.h exifbyte.h ; ln -s exifbyte.h exif-byte-order.h
mv exif-content.h    exifcont.h ; ln -s exifcont.h exif-content.h
mv exif-data.h       exifdata.h ; ln -s exifdata.h exif-data.h
mv exif-data-type.h  exiftype.h ; ln -s exiftype.h exif-data-type.h
mv exif-entry.h      exifent.h  ; ln -s exifent.h  exif-entry.h
mv exif-format.h     exifform.h ; ln -s exifform.h exif-format.h
mv exif-ifd.h        exififd.h  ; ln -s exififd.h  exif-ifd.h
mv exif-loader.h     exifload.h ; ln -s exifload.h exif-loader.h
mv exif-log.h        exiflog.h  ; ln -s exiflog.h  exif-log.h
mv exif-mem.h        exifmem.h  ; ln -s exifmem.h  exif-mem.h
mv exif-mnote-data.h exifnote.h ; ln -s exifnote.h exif-mnote-data.h
mv exif-tag.h        exiftag.h  ; ln -s exiftag.h  exif-tag.h
mv exif-utils.h      exifutil.h ; ln -s exifutil.h exif-utils.h

	cd "$cwd"

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

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
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Thu Nov 16 2023 Thorsten Otto <admin@tho-otto.de>
- update header files with sharedlib version

* Tue Mar 7 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
