%define pkgname binutils

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

Summary:        GNU Binutils
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.34
Release:        20200821
License:        GFDL-1.3-only AND GPL-3.0-or-later
Group:          Development/Tools/Building

Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint
URL:            http://www.gnu.org/software/binutils/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Patch0: %{pkgname}-%{version}-mint-%{release}.patch

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig

%if "%{buildtype}" != "cross"
BuildRequires:  cross-mint-gcc
BuildRequires:  cross-mint-mintlib
BuildRequires:  cross-mint-fdlibm
%if "%{buildtype}" == "v4e"
%define _arch m5475
%else
%if "%{buildtype}" == "020"
%define _arch m68020
%else
%define _arch m68k
%endif
%endif
%endif
%nil

%description
C compiler utilities: ar, as, gprof, ld, nm, objcopy, objdump, ranlib,
size, strings, and strip. These utilities are needed whenever you want
to compile a program or kernel.

%package doc
Summary:        Documentation files for binutils
Group:          Development/Tools/Building
BuildArch:      noarch

%description doc
Documentation for binutils

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1


%build

%rpmint_cflags
%if "%{buildtype}" == "cross"
unset PKG_CONFIG_LIBDIR
unset PKG_CONFIG_PATH
%endif
WITH_CPU_000=m68000
WITH_CPU_020=m68020-60
WITH_CPU_v4e=5475

GCC=${GCC-gcc}
GXX=${GXX-g++}
BUILD_EXEEXT=
PREFIX=/usr

case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	CYGWIN*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	Darwin*) host=macos; STRIP=strip; TAR_OPTS= ;;
	*) host=linux64
	   if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=linux32; fi
	   ;;
esac
case $host in
	cygwin* | mingw* | msys*) BUILD_EXEEXT=.exe ;;
esac
case $host in
	mingw* | msys*) LN_S="cp -p" ;;
esac
if test $host = linux64; then
	BUILD_LIBDIR=%{_libdir}
else
	BUILD_LIBDIR=%{_prefix}/lib
fi

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
for a in "" -1.16 -1.15 -1.14 -1.13 -1.12 -1.11 -1.10; do
	BUILD=`/usr/share/automake${a}/config.guess 2>/dev/null`
	test "$BUILD" != "" && break
	test "$host" = "macos" && BUILD=`/opt/local/share/automake${a}/config.guess 2>/dev/null`
	test "$BUILD" != "" && break
done
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`

%if "%{buildtype}" == "cross"
bfd_targets="--enable-targets=$BUILD"
%else
# we don't want the build target in a native build
bfd_targets=""
%endif
enable_plugins=--disable-plugins
enable_lto=--disable-lto

# binutils ld does not have support for darwin target anymore
test "$host" = "macos" && bfd_targets=""

ranlib=ranlib
# add opposite of default mingw32 target for binutils,
# and also host target
case "${TARGET}" in
    x86_64-*-mingw32*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
	    bfd_targets="${bfd_targets}i686-pc-mingw32"
    	;;
    i686-*-mingw*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
    	bfd_targets="${bfd_targets}x86_64-w64-mingw64"
        ;;
%if "%{buildtype}" != "cross"
    *-*-*mintelf*)
    	enable_lto=--enable-lto
    	ranlib=gcc-ranlib
        ;;
%endif
    *-*-*elf* | *-*-linux* | *-*-darwin*)
    	enable_lto=--enable-lto
        enable_plugins=--enable-plugins
    	ranlib=gcc-ranlib
        ;;
esac
case "${TARGET}" in
    m68k-atari-mintelf*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
    	bfd_targets="${bfd_targets}m68k-atari-mint"
		;;
    m68k-atari-mint*)
    	if test -n "${bfd_targets}"; then bfd_targets="${bfd_targets},"; else bfd_targets="--enable-targets="; fi
    	bfd_targets="${bfd_targets}m68k-atari-mintelf"
		;;
esac

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD="-s"
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
STACKSIZE=
CPU_CFLAGS=
multilibdir=
with_cpu=
%if "%{buildtype}" != "cross"
eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
eval multilibdir=\${CPU_LIBDIR_$CPU}
eval with_cpu=\${WITH_CPU_$CPU}
CFLAGS_FOR_BUILD+=" ${CPU_CFLAGS}"
LDFLAGS_FOR_BUILD+=" ${CPU_CFLAGS}"
CXXFLAGS_FOR_BUILD+=" ${CPU_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"
%endif

case $host in
	macos*)
		GCC=/usr/bin/clang
		GXX=/usr/bin/clang++
		export MACOSX_DEPLOYMENT_TARGET=10.6
		CFLAGS_FOR_BUILD="-pipe -O2 -arch x86_64"
		CXXFLAGS_FOR_BUILD="-pipe -O2 -stdlib=libc++ -arch x86_64"
		LDFLAGS_FOR_BUILD="-Wl,-headerpad_max_install_names -arch x86_64"
		;;
esac

export CC="${GCC}"
export CXX="${GXX}"

%if "%{buildtype}" == "cross"
strip="strip -p"
%else
ranlib=${TARGET}-${ranlib}
strip="${TARGET}-strip -p"
%endif

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir build-dir
cd build-dir

../configure \
	--target="${TARGET}" \
%if "%{buildtype}" != "cross"
	--host="${TARGET}" \
%endif
	--build="$BUILD" \
	--prefix="${PREFIX}" \
%if "%{buildtype}" == "cross"
	--libdir="$BUILD_LIBDIR" \
%else
	--libdir="${PREFIX}/lib" \
%endif
	--bindir="${PREFIX}/bin" \
		--libexecdir='${libdir}' \
		CFLAGS="$CFLAGS_FOR_BUILD" \
		CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
		LDFLAGS="$LDFLAGS_FOR_BUILD ${STACKSIZE}" \
		$bfd_targets \
		--with-pkgversion="$REVISION" \
		--with-stage1-ldflags= \
		--with-boot-ldflags="$LDFLAGS_FOR_BUILD" \
		--with-gcc --with-gnu-as --with-gnu-ld \
		--disable-werror \
		--disable-threads \
		--enable-new-dtags \
		--enable-relro \
		--enable-default-hash-style=both \
		$enable_lto \
		$enable_plugins \
		--disable-nls \
		--with-system-zlib \
		--with-system-readline \
%if "%{buildtype}" == "cross"
		--with-sysroot="${PREFIX}/${TARGET}/sys-root"
%else
		--with-cpu=$with_cpu \
		--with-build-sysroot="/usr/${TARGET}/sys-root"
%endif

make %{?_smp_mflags}

# not quite right, but do the install already here;
# rpmbuild will use a different script during install,
# and our local variables are lost

case $host in
	mingw*) if test "${PREFIX}" = /usr; then PREFIX=${MINGW_PREFIX}; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
	macos*) if test "${PREFIX}" = /usr; then PREFIX=/opt/cross-mint; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
esac

make DESTDIR="${RPM_BUILD_ROOT}" prefix="${PREFIX}" libdir='${exec_prefix}/lib'$multilibdir bindir="${PREFIX}/bin" install-strip

mkdir -p "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"

tools="addr2line ar as nm ld ld.bfd objcopy objdump ranlib strip readelf dlltool dllwrap size strings elfedit gprof c++filt"
%if "%{buildtype}" == "cross"
cd "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"
for i in $tools; do
	if test -x ../../bin/${TARGET}-$i; then
		rm -f ${i} ${i}${BUILD_EXEEXT}
		$LN_S ../../bin/${TARGET}-$i${BUILD_EXEEXT} $i
	fi
done
%else
for i in $tools; do
	cd "${RPM_BUILD_ROOT}${PREFIX}/bin"
	test -f "$i" || continue
	rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
	mv $i ${TARGET}-$i
	$LN_S ${TARGET}-$i $i
	cd "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"
	rm -f ${i} ${i}${TARGET_EXEEXT}
	$LN_S ../../bin/$i${TARGET_EXEEXT} $i
%endif
cd "${RPM_BUILD_ROOT}${PREFIX}/bin"
rm -f ${TARGET}-ld ${TARGET}-ld${BUILD_EXEEXT}
$LN_S ${TARGET}-ld.bfd${BUILD_EXEEXT} ${TARGET}-ld${BUILD_EXEEXT}
cd "${RPM_BUILD_ROOT}"

${strip} ${PREFIX#/}/bin/*
rm -f ${BUILD_LIBDIR#/}/libiberty.a

rm -f ${PREFIX#/}/share/info/dir
%if "%{buildtype}" == "cross"
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man
%else
for f in ${PREFIX#/}/share/man/*/* ${PREFIX#/}/share/info/*; do
	case $f in
	*.gz) ;;
	*) rm -f ${f}.gz; gzip -9 $f ;;
	esac
done
%endif



%install

%rpmint_cflags

# already done above
# make install DESTDIR=${RPM_BUILD_ROOT}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/*
%if "%{buildtype}" == "cross"
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/*
%{_rpmint_target_prefix}/%{_rpmint_target}/lib/*
%else
%{_rpmint_target_prefix}/include/*
%{_rpmint_target_prefix}/lib/*
%endif

%if "%{buildtype}" != "cross"
%files doc
%defattr(-,root,root)
%{_rpmint_target_prefix}/share/man/*/*
%{_rpmint_target_prefix}/share/info/*
%endif



%changelog
* Fri Aug 21 2020 Thorsten Otto <admin@tho-otto.de>
- first RPMint spec file for binutils 2.34
