%define pkgname zita-resampler

%rpmint_header

Summary:        C++ library for resampling audio signals
Name:           %{crossmint}%{pkgname}
Version:        1.8.0
Release:        1
License:        GPL-3.0-only
Group:          Development/Libraries/C and C++

Packager:       %{packager}
URL:            https://kokkinizita.linuxaudio.org/linuxaudio/zita-resampler/resampler.html

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://kokkinizita.linuxaudio.org/linuxaudio/downloads/%{pkgname}-%{version}.tar.bz2
Patch0:  patches/%{pkgname}/zita-resampler-mint.patch

%rpmint_essential
BuildRequires:  make
BuildRequires:  %{crossmint}pthread-devel
Provides:       %{crossmint}libzita-resampler-devel

%rpmint_build_arch

%description
Libzita-resampler is a C++ library for resampling audio signals. It is
designed to be used within a real-time processing context, to be fast,
and to provide high-quality sample rate conversion.

The library operates on signals represented in single-precision
floating point format. For multichannel operation both the input and
output signals are assumed to be stored as interleaved samples.

The API allows a trade-off between quality and CPU load. For the latter
a range of approximately 1:6 is available. Even at the highest quality
setting libzita-resampler will be faster than most similar libraries,
e.g. libsamplerate.

The source distribution includes the resample application. Input format
is any file readable by libsndfile, output is either WAV (WAVEX for
more than 2 channels) or CAF. Apart from resampling you can change the
sample format to 16-bit, 24-bit or float, and for 16-bit output, add
dithering. Available dithering types are rectangular, triangular, and
Lipschitz&apos; optimised error feedback filter. Some examples of dithering
can be seen at https://kokkinizita.linuxaudio.org/linuxaudio/dithering.html.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -fno-strict-aliasing -ffast-math"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	cd source
	
	make clean
	make \
	   CXX=${TARGET}-g++ \
	   CC=${TARGET}-gcc \
	   AR=${TARGET}-ar \
	   RANLIB=${TARGET}-ranlib \
	   CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	   PREFIX=%{_rpmint_sysroot}/usr \
	   LIBDIR='$(PREFIX)/lib'$multilibdir \
	   DESTDIR=%{buildroot} \
	   %{?_smp_mflags} install

	cd ../apps
	make clean
	make \
	   CXX=${TARGET}-g++ \
	   CC=${TARGET}-gcc \
	   AR=${TARGET}-ar \
	   RANLIB=${TARGET}-ranlib \
	   CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	   PREFIX=%{_rpmint_sysroot}/usr \
	   LIBDIR='$(PREFIX)/lib'$multilibdir \
	   MANDIR='$(PREFIX)/share/man/man1' \
	   DESTDIR=%{buildroot} \
	   %{?_smp_mflags} install
	cd ..
	
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
%license COPYING
%doc AUTHORS README
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/zita-resampler
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Tue Apr 04 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
