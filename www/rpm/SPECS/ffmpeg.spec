%define pkgname ffmpeg

%rpmint_header

Summary:        Set of libraries for working with various multimedia formats
Name:           %{crossmint}%{pkgname}
Version:        6.0
Release:        1
License:        GPL-3.0-or-later
Group:          Productivity/Multimedia/Video/Editors and Convertors

Packager:       %{packager}
URL:            https://ffmpeg.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://www.ffmpeg.org/releases/%{pkgname}-%{version}.tar.xz
Patch1: patches/ffmpeg/ffmpeg-arm6l.patch
Patch2: patches/ffmpeg/ffmpeg-new-coder-errors.patch
Patch3: patches/ffmpeg/ffmpeg-codec-choice.patch
Patch6: patches/ffmpeg/ffmpeg-avfilter-vf_libplacebo-remove-deprecated-field.patch
Patch10: patches/ffmpeg/ffmpeg-chromium.patch
Patch99: patches/ffmpeg/ffmpeg-mint.patch

%rpmint_essential
BuildRequires:  pkgconfig
BuildRequires:  make
BuildRequires:  %{crossmint}libmp3lame-devel
BuildRequires:  %{crossmint}libaom-devel
BuildRequires:  %{crossmint}freetype2-devel
BuildRequires:  %{crossmint}libfribidi-devel
BuildRequires:  %{crossmint}libpng-devel
BuildRequires:  %{crossmint}libxml2-devel
BuildRequires:  %{crossmint}libogg-devel
BuildRequires:  %{crossmint}libopus-devel
BuildRequires:  %{crossmint}libvorbis-devel
BuildRequires:  %{crossmint}libtheora-devel
BuildRequires:  %{crossmint}libvpx-devel
BuildRequires:  %{crossmint}libwebp-devel
BuildRequires:  %{crossmint}zlib-devel
BuildRequires:  %{crossmint}libfdk-aac-devel
BuildRequires:  %{crossmint}libx264-devel
BuildRequires:  %{crossmint}libx265-devel
BuildRequires:  %{crossmint}liblcms2-devel
BuildRequires:  pkgconfig(%{crossmint}openssl)
Provides:       %{crossmint}ffmpeg-tools = %{version}
Provides:       %{crossmint}libavcodec-devel = %{version}
Provides:       %{crossmint}libavfilter-devel = %{version}
Provides:       %{crossmint}libavdevice-devel = %{version}
Provides:       %{crossmint}libavformat-devel = %{version}
Provides:       %{crossmint}libavutil-devel = %{version}
Provides:       %{crossmint}libpostproc-devel = %{version}
Provides:       %{crossmint}libswresample-devel = %{version}
Provides:       %{crossmint}libswscale-devel = %{version}

%rpmint_build_arch

%description
FFmpeg is a multimedia framework, able to decode, encode,
transcode, mux, demux, stream, filter and play several formats
that humans and machines have created.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch6 -p1
%patch10 -p1
%patch99 -p1

%build

%rpmint_cflags
COMMON_CFLAGS+=" -fno-strict-aliasing"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-cross-compile
	--pkg-config=${TARGET}-pkg-config
	--target-os=freemint
	--cross-prefix=${TARGET}-
	--arch=m68k
	--enable-static
	--disable-shared
	--disable-pic
	--enable-libxml2
	--enable-libvorbis
	--enable-libtheora
	--enable-libopus
	--enable-libmp3lame
	--enable-libfribidi
	--enable-libfreetype
	--enable-libfdk-aac
	--enable-libaom
	--enable-lcms2
	--enable-libvpx
	--enable-libwebp
	--enable-libx264
	--enable-libx265
	--disable-debug
	--enable-gpl
	--enable-version3
	--enable-nonfree
	--enable-openssl
	--disable-xlib
	--disable-libxcb
"
STACKSIZE="-Wl,-stack,512k"

extratools="aviocat cws2fws ffescape ffeval ffhash fourcc2pixfmt graph2dot ismindex pktdumper probetest qt-faststart seek_print sidxindex trasher"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	"./configure" ${CONFIGURE_FLAGS} \
	--extra-cxxflags="$CPU_CFLAGS $COMMON_CFLAGS" \
	--extra-cflags="$CPU_CFLAGS $COMMON_CFLAGS" \
	--extra-ldflags="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE" \
	--libdir="%{_rpmint_target_prefix}/lib$multilibdir" || exit 1

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	for i in $extratools; do
		make "tools/$i"
		cp -a "tools/$i" "%{buildroot}%{_rpmint_bindir}"
	done

	# Install private headers required by libav-tools
	for i in libavformat/options_table.h libavformat/os_support.h \
	  libavformat/internal.h libavcodec/options_table.h libavutil/libm.h \
	  libavutil/internal.h libavutil/colorspace.h libavutil/timer.h \
	  libavutil/x86/emms.h libavutil/aarch64/timer.h libavutil/arm/timer.h \
	  libavutil/bfin/timer.h libavutil/ppc/timer.h libavutil/x86/timer.h; do
		mkdir -p "%{buildroot}%{_rpmint_includedir}/ffmpeg/private/"`dirname $i`
		cp -a $i "%{buildroot}%{_rpmint_includedir}/ffmpeg/private/$i"
	done

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

	make clean
	for i in $extratools; do
		rm -f tools/$i tools/$i.o
	done
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
%license COPYING.GPLv2 LICENSE.md
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/share/man
%{_isysroot}%{_rpmint_target_prefix}/share/doc/%{pkgname}
%{_isysroot}%{_rpmint_target_prefix}/share/%{pkgname}
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif



%changelog
* Mon Nov 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
