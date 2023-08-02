%define gcc_major_ver 12
%define pkgname gcc%{gcc_major_ver}

%rpmint_header

%define build_fastcall 0
%if %{gcc_major_ver} == 4
%define build_fastcall 1
%endif
%if "%{?build_32bit}" == ""
%define build_32bit 0
%endif

%define build_cp 1
%define build_fortran 1
%define build_objc 0
%define build_objcp 0
%define build_go 0
%define build_ada 1
%define build_d 0
%if %{gcc_major_ver} < 7
%define build_fortran 0
%endif
%if %{gcc_major_ver} < 13
%define build_modula 0
%endif
# D currently does not work natively because of missing libphobos
%if "%{buildtype}" != "cross"
%define build_d 0
%endif

%if %{build_objcp}
%define build_cp 1
%define build_objc 1
%endif

Summary:        The system GNU C Compiler
Name:           %{crossmint}%{pkgname}
Version:        12.3.0
Release:        3
%define releasedate 20230719
License:        GPL-3.0+
Group:          Development/Languages/C and C++
%if "%{buildtype}" != "cross"
Provides:       c_compiler
%endif
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}gcc = %{version}-%{release}
%if %{build_32bit}
Provides:       %{crossmint}gcc-32bit = %{version}-%{release}
%endif
%endif

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://gcc.gnu.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

%define gmp_version https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz
%define mpfr_version https://www.mpfr.org/mpfr-3.1.4/mpfr-3.1.4.tar.xz
%define mpc_version https://ftp.gnu.org/gnu/mpc/mpc-1.0.3.tar.gz
%define isl_version https://libisl.sourceforge.io/isl-0.18.tar.xz

Source0: https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
Source2: gmp-for-gcc.sh
Source3: %{gmp_version}
Source4: %{mpfr_version}
Source5: %{mpc_version}
Source6: %{isl_version}

Patch0: gcc-%{version}-mint-%{releasedate}.patch
Patch1: gmp-universal.patch
Patch2: gmp-6.2.1-CVE-2021-43618.patch
Patch3: gmp-6.2.1-arm64-invert_limb.patch

BuildRequires:  cross-mint-binutils
BuildRequires:  cross-mint-mintlib-headers
BuildRequires:  cross-mint-fdlibm-headers
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  xz
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  perl
BuildRequires:  zlib-devel
%if %{gcc_major_ver} >= 10
BuildRequires:  libzstd-devel
%endif
%if %{build_ada}
BuildRequires:  gcc%{gcc_major_ver}-ada
%endif

%if "%{buildtype}" != "cross"
BuildRequires:  gmp >= 6.0.0
BuildRequires:  mpfr >= 3.0.0
BuildRequires:  mpc >= 1.0.0
BuildRequires:  isl >= 0.18
%endif

%if "%{buildtype}" == "cross"
%if %{build_32bit}
%define _target_cpu i686
%define _host_cpu i686
%define _arch i686
BuildRequires:  gcc-c++-32bit
BuildRequires:  %{crossmint}binutils-32bit
Provides:       %{crossmint}%{pkgname}-32bit = %{version}-%{release}
%else
BuildRequires:  gcc-c++
%endif
%else
BuildRequires:  cross-mint-%{pkgname} = %{version}
BuildRequires:  cross-mint-mintlib
BuildRequires:  cross-mint-fdlibm

%define _target_platform %{_rpmint_target_platform}
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

%description
The GNU Compiler Collection includes front ends for C, C++,
Objective-C, Fortran, and Go, as well as libraries for these
languages (libstdc++, libgcj,...).

%package c++
Summary:        The GNU C++ Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/C and C++
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-c++ = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}libstdc++-devel = %{version}-%{release}
Provides:       %{crossmint}c++ = %{version}-%{release}
Provides:       %{crossmint}gcc-c++ = %{version}-%{release}
%if %{build_32bit}
Provides:       %{crossmint}gcc-c++-32bit = %{version}-%{release}
%endif
%else
%if %{build_cp}
BuildRequires:  cross-mint-%{pkgname}-c++ = %{version}
%endif
Provides:       libstdc++-devel = %{version}-%{release}
Provides:       c++ = %{version}-%{release}
Provides:       c++-compiler
%endif

%description c++
This package contains the GNU compiler for C++.

%package objc
Summary:        GNU Objective C Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-objc = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}libobjc = %{version}-%{release}
Provides:       %{crossmint}gcc-objc = %{version}-%{release}
%else
%if %{build_objc}
BuildRequires:  cross-mint-%{pkgname}-objc = %{version}
%endif
Provides:       libobjc = %{version}-%{release}
Provides:       gcc-objc = %{version}-%{release}
%endif

%description objc
This package contains the GNU Objective C compiler. Objective C is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package obj-c++
Summary:        GNU Objective C++ Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{name}-c++ = %{version}-%{release}
Requires:       %{name}-obj-c++ = %{version}-%{release}
Requires:       %{name}-objc = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}gcc-obj-c++ = %{version}-%{release}
%else
%if %{build_objcp}
BuildRequires:  cross-mint-%{pkgname}-obj-c++ = %{version}
%endif
Provides:       gcc-obj-c++ = %{version}-%{release}
%endif

%description obj-c++
This package contains the GNU Objective C++ compiler. Objective C++ is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package ada
Summary:        GNU Ada Compiler Based on GCC (GNAT)
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-ada = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}libada = %{version}-%{release}
Provides:       %{crossmint}gcc-ada = %{version}-%{release}
%else
%if %{build_ada}
BuildRequires:  cross-mint-%{pkgname}-ada = %{version}
%endif
Provides:       libada = %{version}-%{release}
Provides:       gcc-ada = %{version}-%{release}
%endif

%description ada
This package contains an Ada compiler and associated development
tools based on the GNU GCC technology.

%package fortran
Summary:        The GNU Fortran Compiler and Support Files
License:        GPL-3.0-or-later
Group:          Development/Languages/Fortran
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-fortran = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}libgfortran = %{version}-%{release}
Provides:       %{crossmint}gcc-fortran = %{version}-%{release}
%else
%if %{build_fortran}
BuildRequires:  cross-mint-%{pkgname}-fortran = %{version}
%endif
Provides:       libgfortran = %{version}-%{release}
Provides:       gcc-fortran = %{version}-%{release}
%endif

%description fortran
This is the Fortran compiler of the GNU Compiler Collection (GCC).

%package go
Summary:        GNU Go Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-go = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}libgo = %{version}-%{release}
Provides:       %{crossmint}gcc-go = %{version}-%{release}
%else
%if %{build_go}
BuildRequires:  cross-mint-%{pkgname}-go = %{version}
%endif
Provides:       libgo = %{version}-%{release}
Provides:       gcc-go = %{version}-%{release}
%endif

%description go
This package contains a Go compiler and associated development
files based on the GNU GCC technology.

%package d
Summary:        GNU D Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-d = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       %{crossmint}libgdruntime = %{version}-%{release}
Provides:       %{crossmint}libgphobos = %{version}-%{release}
Provides:       %{crossmint}gcc-d = %{version}-%{release}
%else
%if %{build_d}
BuildRequires:  cross-mint-%{pkgname}-d = %{version}
%endif
Provides:       cross-mint-libgdruntime = %{version}-%{release}
Provides:       cross-mint-libgphobos = %{version}-%{release}
Provides:       gcc-d = %{version}-%{release}
%endif

%description d
This package contains a D compiler and associated development
files based on the GNU GCC technology.

%package doc
Summary:        The system GNU Compiler documentation
License:        GFDL-1.2
Group:          Development/Languages/C and C++
BuildArch:      noarch

%description doc
The system GNU Compiler documentation.

# ##################################
# P R E P
# ##################################
%prep
%setup -q -n gcc-%{version}
%patch0 -p1

srcdir="${RPM_BUILD_DIR}/gcc-%{version}"

%if "%{buildtype}" == "cross"
# dont run this on Darwin, we want universal binaries there,
# which cant be built by the gcc configure scripts,
# and are done by gmp-for-gcc.sh instead
case `uname -s` in
	Darwin*) ;;
	*)
	for archive in %{gmp_version} %{mpfr_version} %{mpc_version} %{isl_version}; do
		basearchive=${archive##*/}
		package="${basearchive%.tar*}"
		if ! test -f "${RPM_SOURCE_DIR}/${basearchive}"; then
			echo "fetching ${archive}"
			wget -nv "${archive}" -O "${RPM_SOURCE_DIR}/${basearchive}"
		fi
		tar -C "${srcdir}" -xf "${RPM_SOURCE_DIR}/${basearchive}"
		basepackage="${package%%-*}"
		ln -sf "${package}" "${srcdir}/${basepackage}"
		if test "$basepackage" = gmp; then
(
cd $package
%patch1 -p1
%patch2 -p1
# following patch was taken from SuSE, but failes to compile with clang
# %patch3 -p1
)
		fi
	done
	;;
	esac
%endif

# ##################################
# B U I L D
# ##################################
%build

srcdir="${RPM_BUILD_DIR}/gcc-%{version}"

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
TARGET_EXEEXT=
PREFIX=%{_prefix}

case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	CYGWIN*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	Darwin*) host=macos; TAR_OPTS= ;;
	*) host=linux64
%if %{build_32bit}
	   host=linux32
%endif
	   ;;
esac
LN_S="ln -s"
case $host in
	cygwin* | mingw* | msys*) BUILD_EXEEXT=.exe ;;
esac
case $host in
	mingw* | msys*) LN_S="cp -p" ;;
esac
%if %{build_32bit}
%define build_libdir %{_prefix}/lib
%else
%if "%{buildtype}" == "cross"
%define build_libdir %{_libdir}
%else
%define build_libdir %{_rpmint_target_prefix}/lib
%endif
%endif
BUILD_LIBDIR=%{build_libdir}

BASE_VER=$(cat gcc/BASE-VER)
if test "$BASE_VER" != "%{version}"; then
	echo "version mismatch: this script is for gcc %{version}, but gcc source is version $BASE_VER" >&2
	exit 1
fi
%if %{gcc_major_ver} >= 6
%define gcc_dir_version %{gcc_major_ver}
%else
%define gcc_dir_version %version
%endif
gcc_dir_version=%{gcc_dir_version}
%define gccsubdir %{build_libdir}/gcc/%{_rpmint_target}/%{gcc_dir_version}
%define gxxinclude %{_rpmint_target_prefix}/include/c++/%{gcc_dir_version}

#
# try config.guess from automake first to get the
# canonical build system name.
# On some distros it is patched to have the
# vendor name included.
#
%define BUILD %(for a in "" -1.16 -1.15 -1.14 -1.13 -1.12 -1.11 -1.10; do \
	BUILD=`/usr/share/automake${a}/config.guess 2>/dev/null`; \
	test "$BUILD" != "" && break; \
	test "$host" = "macos" && BUILD=`/opt/local/share/automake${a}/config.guess 2>/dev/null`; \
	test "$BUILD" != "" && break; \
done; \
test "$BUILD" = "" && BUILD=`${srcdir}/config.guess`; \
case $BUILD in \
	(x86_64-pc-mingw32) BUILD=x86_64-pc-mingw32 ;; \
	(i686-pc-mingw32) BUILD=i686-pc-msys ;; \
esac; \
echo $BUILD
)
BUILD=%{BUILD}

languages=c
%if %{build_cp}
languages=$languages,c++
%endif
%if %{build_objc}
languages=$languages,objc
%endif
%if %{build_fortran}
languages=$languages,fortran
%endif
%if %{build_objcp}
languages=$languages,obj-c++
%endif
%if %{build_ada}
languages=$languages,ada
%endif
%if %{build_go}
languages=$languages,go
%endif
%if %{build_d}
languages=$languages,d
%endif


%define enable_plugin 0
%define enable_lto %(case "%{_rpmint_target}" in (*-*-*elf* | *-*-linux*) echo 1;; (*) echo 0;; esac)
%if %{enable_lto}
%if "%{buildtype}" == "cross"
%define enable_plugin %(case "%{BUILD}" in (*-*-linux*) echo 1;; (*) echo 0;; esac)
%endif
languages="$languages,lto"
%endif

CFLAGS_FOR_BUILD="-O2 -fomit-frame-pointer"
CFLAGS_FOR_TARGET="-O2 -fomit-frame-pointer"
LDFLAGS_FOR_BUILD="-s"
CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
CXXFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"
STACKSIZE=
CPU_CFLAGS=
multilibdir=
with_cpu=
%if "%{buildtype}" != "cross"
CPU=%{buildtype}
if grep -q 'MULTILIB_DIRNAMES = m68000' "gcc/config/m68k/t-mint"; then
CPU_LIBDIR_000=/m68000
CPU_LIBDIR_020=/m68020-60
CPU_LIBDIR_v4e=/m5475
else
CPU_LIBDIR_000=
CPU_LIBDIR_020=
CPU_LIBDIR_v4e=
fi
eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
eval multilibdir=\${CPU_LIBDIR_$CPU}
eval with_cpu=\${WITH_CPU_$CPU}
CFLAGS_FOR_BUILD+=" ${CPU_CFLAGS}"
LDFLAGS_FOR_BUILD+=" ${CPU_CFLAGS}"
CXXFLAGS_FOR_BUILD+=" ${CPU_CFLAGS}"
STACKSIZE="-Wl,-stack,512k"
%endif

mpfr_config=

unset GLIBC_SO
without_zstd=

case $host in
	macos*)
		GCC=/usr/bin/clang
		GXX=/usr/bin/clang++
		MACOSX_DEPLOYMENT_TARGET=10.9
		ARCHS="-arch x86_64"
		case `$GCC --print-target-triple 2>/dev/null` in
		arm64* | aarch64*)
			BUILD_ARM64=yes
			;;
		esac
		if test `uname -r | cut -d . -f 1` -ge 20; then
			BUILD_ARM64=yes
		fi
		if test "$BUILD_ARM64" = yes; then
			ARCHS="${ARCHS} -arch arm64"
			MACOSX_DEPLOYMENT_TARGET=11
		fi
		export MACOSX_DEPLOYMENT_TARGET
		CFLAGS_FOR_BUILD="-pipe -O2 ${ARCHS}"
		CXXFLAGS_FOR_BUILD="-pipe -O2 -stdlib=libc++ ${ARCHS}"
		LDFLAGS_FOR_BUILD="-Wl,-headerpad_max_install_names ${ARCHS}"
		mpfr_config="--with-mpc=${CROSSTOOL_DIR}"
		# zstd gives link errors on github runners
		without_zstd=--without-zstd
		;;
	linux64)
%if "%{buildtype}" == "cross"
		CFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD -include $srcdir/gcc/libcwrap.h"
		CXXFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD"
		export GLIBC_SO="$srcdir/gcc/glibc.so"
%endif
		;;
esac

%if %{build_ada}
# Using the host gnatmake like
#   CC="gcc%%{hostsuffix}" GNATBIND="gnatbind%%{hostsuffix}"
#   GNATMAKE="gnatmake%%{hostsuffix}"
# doesn't work due to PR33857, so an un-suffixed gnatmake has to be
# available
	adahostsuffix=-%{gcc_major_ver}
	GCC=gcc${adahostsuffix}
	GXX=g++${adahostsuffix}
	if test ! -x /usr/bin/gnatmake${adahostsuffix}; then
		echo "need gnatmake${adahostsuffix} to build ada" >&2
		exit 1
	fi
	mkdir -p host-tools/bin
	$LN_S -f /usr/bin/gnatmake${adahostsuffix} host-tools/bin/gnatmake
	$LN_S -f /usr/bin/gnatlink${adahostsuffix} host-tools/bin/gnatlink
	$LN_S -f /usr/bin/gnatbind${adahostsuffix} host-tools/bin/gnatbind
	$LN_S -f /usr/bin/gnatls${adahostsuffix} host-tools/bin/gnatls
	$LN_S -f /usr/bin/gcc${adahostsuffix} host-tools/bin/gcc
	if test $host = linux64; then
		$LN_S -f /usr/lib64 host-tools/lib64
	else
		$LN_S -f /usr/lib host-tools/lib
	fi
	export PATH="`pwd`/host-tools/bin:$PATH"
%endif

%if %{build_32bit}
GCC="${GCC} -m32"
GXX="${GXX} -m32"
%endif

export CC="${GCC}"
export CXX="${GXX}"
GNATMAKE="gnatmake${adahostsuffix}"
GNATBIND="gnatbind${adahostsuffix}"
GNATLINK="gnatlink${adahostsuffix}"


fail()
{
	component="$1"
	echo "configuring $component failed"
	exit 1
}


%if "%{buildtype}" != "cross"
export AS_FOR_TARGET=%{_rpmint_target}-as
export RANLIB_FOR_TARGET=%{_rpmint_target}-ranlib
export STRIP_FOR_TARGET=%{_rpmint_target}-strip
export CC_FOR_TARGET="${TARGET}-gcc-%{version}"
export GCC_FOR_TARGET="${TARGET}-gcc-%{version}"
export CXX_FOR_TARGET="${TARGET}-g++-%{version}"
export GFORTRAN_FOR_TARGET="${TARGET}-gfortran-%{version}"
export GOC_FOR_TARGET="${TARGET}-goc-%{version}"
%endif

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir build-dir
cd build-dir
GCC_WRAPPER="$PWD/gcc-wrapper.sh"
GXX_WRAPPER="$PWD/gxx-wrapper.sh"

%if "%{buildtype}" != "cross"
cat <<'EOF' > "${GCC_WRAPPER}"
#!/bin/sh

#
# Wrapper to invoke the cross-compiler to generate code for the
# intended architecture. We cannot use CFLAGS_FOR_TARGET, because
# that would only be used for the just-built xgcc, which is already
# a binary for the target in our case. We also cannot just add the
# flags to $CC, because that clashes when compiling multilibs.
# So what we do is to add the flags to $CC, use this
# script as the compiler, and keep only the last cpu-specific flags
#
cpu_flags=
args=
for i in "$@"; do
    case "$i" in
		-m68*) cpu_flags=$1 ;;
		-mcpu=*) cpu_flags=$1 ;;
        *)
        	i="${i//\\/\\\\}"
		    args="$args \"${i//\"/\\\"}\""
        	;;
    esac
done
EOF

cp "${GCC_WRAPPER}" "${GXX_WRAPPER}"
cat <<EOF >> "${GCC_WRAPPER}"
eval exec "${TARGET}-gcc-%{version}" \$cpu_flags \$args
EOF
cat <<EOF >> "${GXX_WRAPPER}"
eval exec "${TARGET}-g++-%{version}" \$cpu_flags \$args
EOF

chmod 755 "${GCC_WRAPPER}"
chmod 755 "${GXX_WRAPPER}"

export CC="${GCC_WRAPPER} $CPU_CFLAGS"
export CXX="${GXX_WRAPPER} $CPU_CFLAGS"

export LDFLAGS="$STACKSIZE"
export CFLAGS="-O2 -fomit-frame-pointer"
export CXXFLAGS="-O2 -fomit-frame-pointer"

%endif

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
%if "%{buildtype}" == "cross"
	CFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD" \
	CFLAGS="$CFLAGS_FOR_BUILD" \
	CXXFLAGS_FOR_BUILD="$CXXFLAGS_FOR_BUILD" \
	CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
	BOOT_CFLAGS="$CFLAGS_FOR_BUILD" \
	CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET" \
	CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET" \
	LDFLAGS_FOR_BUILD="$LDFLAGS_FOR_BUILD" \
	LDFLAGS="$LDFLAGS_FOR_BUILD ${STACKSIZE}" \
	GNATMAKE_FOR_HOST="${GNATMAKE}" \
	GNATBIND_FOR_HOST="${GNATBIND}" \
	GNATLINK_FOR_HOST="${GNATLINK}" \
%endif
	--with-pkgversion="MiNT %{releasedate}" \
	--disable-libvtv \
	--disable-libmpx \
	--disable-libcc1 \
%if %{gcc_major_ver} >= 7
	--disable-werror \
	--disable-win32-registry \
%endif
%if "%{buildtype}" == "cross"
	--with-gxx-include-dir=%{_rpmint_sysroot}%{gxxinclude} \
%else
	--with-gxx-include-dir=%{gxxinclude} \
%endif
	--with-default-libstdcxx-abi=gcc4-compatible \
%if %{gcc_major_ver} >= 6
	--with-gcc-major-version-only \
%endif
	--with-gcc --with-gnu-as --with-gnu-ld \
	--with-system-zlib \
	--without-static-standard-libraries \
	--without-stage1-ldflags \
	--disable-libgomp \
	--without-newlib \
	--disable-libstdcxx-pch \
	--disable-threads \
%if %{enable_lto}
	--enable-lto \
%else
	--disable-lto \
%endif
	--enable-ssp \
	--enable-libssp \
%if %{enable_plugin}
	--enable-plugin \
%else
	--disable-plugin \
%endif
	--disable-decimal-float \
	--disable-nls \
	$mpfr_config \
%if "%{buildtype}" == "cross"
	--with-libiconv-prefix="${PREFIX}" \
	--with-libintl-prefix="${PREFIX}" \
	--with-sysroot="${PREFIX}/${TARGET}/sys-root" \
%else
	--with-cpu=$with_cpu \
%if %{gcc_major_ver} >= 10
	--with-build-sysroot="%{_rpmint_target_prefix}/${TARGET}/sys-root" \
%else
	--with-sysroot="%{_rpmint_target_prefix}/${TARGET}/sys-root" \
%endif
%endif
	--enable-languages="$languages" || fail "gcc"

%if "%{buildtype}" != "cross"
make configure-gcc
# there seems to be a problem with thin archives
#	sed -i 's/^S\["thin_archive_support"\]="\([^"]*\)"$/S\["thin_archive_support"\]="no"/' gcc/config.status
# c++ complains about an unknown option?
sed -i -e 's/-Wno-error=format-diag//' gcc/config.status
	./config.status
%endif

make %{?_smp_mflags} all-gcc
make %{?_smp_mflags} all-target-libgcc
make %{?_smp_mflags}

# ##################################
# I N S T A L L
# ##################################
%install

%rpmint_cflags

gcc_major_version=%{gcc_major_ver}
gcc_dir_version=%{gcc_dir_version}
BASE_VER=%{version}
BUILD_LIBDIR=%{build_libdir}

cd build-dir

%if "%{buildtype}" != "cross"
eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
eval multilibdir=\${CPU_LIBDIR_$CPU}
%endif

PREFIX=%{_prefix}
case "$host" in
	mingw*) if test "${PREFIX}" = /usr; then PREFIX=${MINGW_PREFIX}; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
	macos*) if test "${PREFIX}" = /usr; then PREFIX=/opt/cross-mint; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
esac

%if "%{buildtype}" == "cross"
	libdir="$BUILD_LIBDIR"
	libexecdir="$BUILD_LIBDIR"
%else
	libdir="${PREFIX}/lib$multilibdir"
	libexecdir="${PREFIX}/lib$multilibdir"
%endif

make DESTDIR="${RPM_BUILD_ROOT}" prefix="${PREFIX}" libdir="$libdir" libexecdir="$libexecdir" bindir="${PREFIX}/bin" install

mkdir -p "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"

# ranlib is always used for target libraries
ranlib_for_target=%{_rpmint_target}-ranlib
# strip is sometimes used for host executables,
# sometimes for target libraries
strip_for_host="strip -p"
strip_for_target="%{_rpmint_target}-strip -p"
%if "%{buildtype}" != "cross"
strip_for_host="${strip_for_target}"
%endif

tools="c++ cpp g++ gcc gcov gfortran gdc"
%if "%{buildtype}" == "cross"
cd "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"
for i in $tools; do
	if test -x ../../bin/${TARGET}-$i; then
		rm -f ${i} ${i}${BUILD_EXEEXT}
		$LN_S ../../bin/${TARGET}-$i${BUILD_EXEEXT} $i
	fi
done
%else
BUILD_EXEEXT=${TARGET_EXEEXT}
for i in $tools gcc-ar gcc-nm gcc-ranlib; do
	cd "${RPM_BUILD_ROOT}${PREFIX}/bin"
	test -f "$i" || continue
	rm -f ${TARGET}-${i} ${TARGET}-${i}${TARGET_EXEEXT}
	mv $i ${TARGET}-$i
	$LN_S ${TARGET}-$i $i
	cd "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"
	rm -f ${i} ${i}${TARGET_EXEEXT}
	$LN_S ../../bin/$i${TARGET_EXEEXT} $i
done
%endif

cd "${RPM_BUILD_ROOT}${PREFIX}/bin"
${strip_for_host} *

	if test -x ${TARGET}-g++ && test ! -h ${TARGET}-g++; then
		rm -f ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}
		rm -f ${TARGET}-g++-${gcc_dir_version}${BUILD_EXEEXT} ${TARGET}-g++-${gcc_dir_version}
		mv ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++${BUILD_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${gcc_major_version}${BUILD_EXEEXT}
%if "%{buildtype}" != "cross"
		rm -f g++-${BASE_VER}${TARGET_EXEEXT} g++-${BASE_VER}
		rm -f g++-${gcc_dir_version}${TARGET_EXEEXT} g++-${gcc_dir_version}${TARGET_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${TARGET_EXEEXT} g++-${BASE_VER}${TARGET_EXEEXT}
		$LN_S ${TARGET}-g++-${gcc_dir_version}${TARGET_EXEEXT} g++-${gcc_major_version}${TARGET_EXEEXT}
%endif
	fi
	if test -x ${TARGET}-c++ && test ! -h ${TARGET}-c++; then
		rm -f ${TARGET}-c++${BUILD_EXEEXT} ${TARGET}-c++
		$LN_S ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-c++${BUILD_EXEEXT}
	fi
	for tool in gcc gfortran gdc gccgo go gofmt \
                    gnat gnatbind gnatchop gnatclean gnatkr gnatlink gnatls gnatmake gnatname gnatprep gnatxref; do
		if test -x ${TARGET}-${tool} && test ! -h ${TARGET}-${tool}; then
			rm -f ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}-${BASE_VER}
			rm -f ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}
			mv ${TARGET}-${tool}${BUILD_EXEEXT} ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}${BUILD_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT}
%if "%{buildtype}" != "cross"
			rm -f ${tool}-${BASE_VER}${BUILD_EXEEXT} ${tool}-${BASE_VER}
			rm -f ${tool}-${gcc_major_version}${BUILD_EXEEXT} ${tool}-${gcc_major_version}${BUILD_EXEEXT}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${tool}-${BASE_VER}${BUILD_EXEEXT}
			$LN_S ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${tool}-${gcc_major_version}${BUILD_EXEEXT}
%endif
		fi
	done
	if test -x ${TARGET}-cpp && test ! -h ${TARGET}-cpp; then
		rm -f ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-cpp-${BASE_VER}
		mv ${TARGET}-cpp${BUILD_EXEEXT} ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-cpp-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-cpp${BUILD_EXEEXT}
	fi

cd "${RPM_BUILD_ROOT}"

# that directory only contains the gdb pretty printers;
# on the host we don't want them because they would conflict
# with the system ones; on the target we don't need them
# because gdb does not work
rm -rf ${PREFIX#/}/share/gcc-%{gcc_dir_version}
if test -d ${PREFIX#/}/${TARGET}/lib; then find ${PREFIX#/}/${TARGET}/lib -name "libstdc++*.py" -delete; fi
if test -d ${PREFIX#/}/lib; then find ${PREFIX#/}/lib -name "libstdc++*.py" -delete; fi


rm -f ${PREFIX#/}/share/info/dir
rm -f ${PREFIX#/}/share/info/libquadmath*
%if "%{buildtype}" == "cross"
# on the host these may conflict with the system ones
rm -rf ${PREFIX#/}/share/info
rm -rf ${PREFIX#/}/share/man
%else
rm -f ${PREFIX#/}/share/info/dir
for f in ${PREFIX#/}/share/man/*/* ${PREFIX#/}/share/info/*; do
	case $f in
	*.gz) ;;
	*) rm -f ${f}.gz; gzip -9 $f ;;
	esac
done
%endif
rm -rf ${PREFIX#/}/share/gcc*/python
rmdir ${PREFIX#/}/share || :

	rm -f */*/libiberty.a
	find . -type f -name "*.la" -delete -printf "rm %p\n"

#
# move compiler dependant libraries to the gcc subdirectory
#
%if "%{buildtype}" == "cross"
	pushd ${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/lib
%else
	pushd ${RPM_BUILD_ROOT}${PREFIX}/lib
%endif
	libs=`find . -name "lib*.a" ! -path "*/gcc/*"`
	tar -c $libs | tar -x -C ${RPM_BUILD_ROOT}%{gccsubdir}
	rm -f $libs
	for i in libgfortran.spec libgomp.spec libitm.spec libsanitizer.spec libmpx.spec libgphobos.spec; do
		test -f $i && mv $i ${RPM_BUILD_ROOT}%{gccsubdir}
		find . -name "$i" -delete
	done
	rmdir m*/*/*/* || :
	rmdir m*/*/* || :
	rmdir m*/* || :
	rmdir m* || :
	popd

	case $host in
		cygwin*) LTO_PLUGIN=cyglto_plugin-0.dll; MY_LTO_PLUGIN=cyglto_plugin_mintelf-${gcc_dir_version}.dll ;;
		mingw* | msys*) LTO_PLUGIN=liblto_plugin-0.dll; MY_LTO_PLUGIN=liblto_plugin_mintelf-${gcc_dir_version}.dll ;;
		macos*) LTO_PLUGIN=liblto_plugin.dylib; MY_LTO_PLUGIN=liblto_plugin_mintelf-${gcc_dir_version}.dylib ;;
		*) LTO_PLUGIN=liblto_plugin.so.0.0.0; MY_LTO_PLUGIN=liblto_plugin_mintelf.so.${gcc_dir_version} ;;
	esac
%define lto_plugin liblto_plugin.so.0.0.0

	# remove fixincl; it is not needed for cross-compiler and may introduce unneeded dependencies
	rm -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/install-tools/fixincl
	for f in ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/{cc1,cc1plus,cc1obj,cc1objplus,f951,d21,collect2,lto-wrapper,lto1,gnat1,gnat1why,gnat1sciln,go1,brig1,g++-mapper-server}${BUILD_EXEEXT} \
		${BUILD_LIBDIR#/}/gcc/${TARGET}/*/${LTO_PLUGIN} \
		${BUILD_LIBDIR#/}/gcc/${TARGET}/*/plugin/gengtype${BUILD_EXEEXT} \
		${BUILD_LIBDIR#/}/gcc/${TARGET}/*/install-tools/fixincl${BUILD_EXEEXT}; do
		test -f "$f" && ${strip_for_host} "$f"
	done
	rmdir ${PREFIX#/}/include || :
	
	if test -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN}; then
		mkdir -p ${PREFIX#/}/lib/bfd-plugins
		cd ${PREFIX#/}/lib/bfd-plugins
		rm -f ${MY_LTO_PLUGIN}
		$LN_S ../../${BUILD_LIBDIR##*/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN} ${MY_LTO_PLUGIN}
		cd "${INSTALL_DIR}"
	fi
	
	find ${PREFIX#/} -name "*.a" -exec ${strip_for_target} -S -x '{}' \;
	find ${PREFIX#/} -name "*.a" -exec ${ranlib_for_target} '{}' \;
	
	cd ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/include-fixed && {
		for i in `find . -type f`; do
			case $i in
			./README | ./limits.h | ./syslimits.h) ;;
			*) echo "removing fixed include file $i"; rm -f $i ;;
			esac
		done
		for i in `find . -type l`; do
			rm -fv $i
		done
		for i in `find . -depth -type d`; do
			test "$i" = "." || rmdir "$i"
		done
	}


# ##################################
# C L E A N
# ##################################
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-gcc*
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-cpp*
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-gcov*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gcc*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gcov*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/cpp*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gcc*
%{_rpmint_target_prefix}/bin/cpp*
%{_rpmint_target_prefix}/bin/gcov*
%endif
%{gccsubdir}/cc1
%{gccsubdir}/collect2
%{gccsubdir}/lto-wrapper
%{gccsubdir}/install-tools
%{gccsubdir}/include
%{gccsubdir}/include-fixed
%{gccsubdir}/libgcc*
%{gccsubdir}/*/libgcc*
%{gccsubdir}/*/*/libgcc*
%if %{build_fastcall}
%{gccsubdir}/*/*/*/libgcc*
%endif
%{gccsubdir}/libgcov*
%{gccsubdir}/*/libgcov*
%{gccsubdir}/*/*/libgcov*
%if %{build_fastcall}
%{gccsubdir}/*/*/*/libgcov*
%endif
%{gccsubdir}/libssp*
%{gccsubdir}/*/libssp*
%if %{gcc_major_ver} < 6
%{gccsubdir}/libmudflap*
%{gccsubdir}/*/libmudflap*
%endif
%if %{enable_lto}
%{gccsubdir}/lto1
%endif
%if %{enable_plugin}
%{gccsubdir}/liblto_plugin*
%{gccsubdir}/plugin
%{_prefix}/lib/bfd-plugins
%endif

%if "%{buildtype}" != "cross"
%files doc
%defattr(-,root,root)
%{_rpmint_target_prefix}/share/man/*/*
%{_rpmint_target_prefix}/share/info/*

%post doc
%rpmint_install_info %{pkgname}*
%rpmint_install_info cpp*
%if %{build_fortran}
%rpmint_install_info gfortran*
%endif
%if %{build_ada}
%rpmint_install_info gnat*
%endif

%preun doc
%rpmint_uninstall_info %{pkgname}*
%rpmint_uninstall_info cpp*
%if %{build_fortran}
%rpmint_uninstall_info gfortran*
%endif
%if %{build_ada}
%rpmint_uninstall_info gnat*
%endif

%endif

%if %{build_cp}
%files c++
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-c++*
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-g++*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/c++*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/g++*
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/c++
%else
%{_rpmint_target_prefix}/bin/c++*
%{_rpmint_target_prefix}/bin/g++*
%{_rpmint_target_prefix}/include/c++
%endif
%{gccsubdir}/cc1plus
%{gccsubdir}/libstdc++*
%{gccsubdir}/*/libstdc++*
%{gccsubdir}/libsupc++*
%{gccsubdir}/*/libsupc++*
%if %{gcc_major_ver} >= 11
%{gccsubdir}/g++-mapper-server
%endif
%endif

%if %{build_objc}
%files objc
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_includedir}/objc
%else
%{_rpmint_target_prefix}/include/objc
%endif
%{gccsubdir}/cc1obj
%{gccsubdir}/libobjc*
%{gccsubdir}/*/libobjc*
%endif

%if %{build_objcp}
%files obj-c++
%defattr(-,root,root)
%{gccsubdir}/cc1objplus
%endif

%if %{build_fortran}
%files fortran
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-gfortran*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gfortran*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gfortran*
%endif
%{gccsubdir}/f951
%{gccsubdir}/finclude
%{gccsubdir}/*/finclude
%{gccsubdir}/libgfortran*
%{gccsubdir}/*/libgfortran*
%if %{gcc_major_ver} >= 6
%{gccsubdir}/libcaf*
%{gccsubdir}/*/libcaf*
%endif
%endif

%if %{build_ada}
%files ada
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-gnat*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gnat*
%endif
%{gccsubdir}/gnat1
%{gccsubdir}/adalib
%{gccsubdir}/*/adalib
%{gccsubdir}/adainclude
%{gccsubdir}/*/adainclude
%if %{gcc_major_ver} >= 10
%{gccsubdir}/ada_target_properties
%{gccsubdir}/*/ada_target_properties
%endif
%endif

%if %{build_go}
%files go
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-go*
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-gccgo*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/go*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gccgo*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/go*
%{_rpmint_target_prefix}/bin/gccgo*
%endif
%{gccsubdir}/go1
%{gccsubdir}/cgo
%{gccsubdir}/libgo*
%{gccsubdir}/*/libgo*
%{build_libdir}/go/%{gcc_dir_version}
%endif

%if %{build_d}
%files d
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target}-gdc*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gdc*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gdc*
%endif
%{gccsubdir}/d21
%{gccsubdir}/d
%{gccsubdir}/libgphobos*
%{gccsubdir}/*/libphobos*
%{gccsubdir}/libgdruntime*
%{gccsubdir}/*/libgdruntime*
%endif


%changelog
* Tue Feb 14 2023 Thorsten Otto <admin@tho-otto.de>
- Some cleanup to properly use install section 

* Fri Aug 21 2020 Thorsten Otto <admin@tho-otto.de>
- first RPMint spec file
