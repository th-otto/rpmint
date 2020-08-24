%define gcc_major_ver 4
%define pkgname gcc%{gcc_major_ver}

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%if "%{?build_32bit}" == ""
%define build_32bit 0
%endif

%define build_cp 1
%define build_fortran 1
%define build_objc 0
%define build_objcp 0
%define build_go 0
%define build_ada 0
%define build_d 0

%if %{build_objcp}
%define build_cp 1
%define build_objc 1
%endif

%if "%{buildtype}" == "cross"
%define cross_pkgname  cross-mint-%{pkgname}
%else
%define cross_pkgname  %{pkgname}
%endif

Summary:        The system GNU C Compiler
Name:           %{cross_pkgname}
Version:        4.6.4
Release:        1
%define releasedate 20200502
License:        GPL-3.0+
Group:          Development/Languages/C and C++
%if "%{buildtype}" != "cross"
Provides:       c_compiler
%endif
%if "%{buildtype}" == "cross"
Provides:       cross-mint-gcc
%endif

Packager:       Thorsten Otto <admin@tho-otto.de>
Vendor:         RPMint
URL:            http://gcc.gnu.org/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.bz2
Source1: gcc-download-prerequisites
Patch0: gcc-%{version}-mint-%{releasedate}.patch
Patch1: gcc-%{version}-fastcall.patch

BuildRequires:  gcc-c++
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
%if %{build_ada}
BuildRequires:  gcc-ada
%endif

%if "%{buildtype}" != "cross"
BuildRequires:  cross-mint-gcc
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
The system GNU C Compiler.

%package c++
Summary:        The GNU C++ Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/C and C++
Requires:       %{cross_pkgname} = %{version}-%{release}
Requires:       %{cross_pkgname}-c++ = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libstdc++-devel = %{version}-%{release}
%else
Provides:       libstdc++-devel = %{version}-%{release}
%endif

%description c++
This package contains the GNU compiler for C++.

%package objc
Summary:        GNU Objective C Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{cross_pkgname} = %{version}-%{release}
Requires:       %{cross_pkgname}-objc = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libobjc = %{version}-%{release}
%else
Provides:       libobjc = %{version}-%{release}
%endif

%description objc
This package contains the GNU Objective C compiler. Objective C is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package obj-c++
Summary:        GNU Objective C++ Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{cross_pkgname}-c++ = %{version}-%{release}
Requires:       %{cross_pkgname}-obj-c++ = %{version}-%{release}
Requires:       %{cross_pkgname}-objc = %{version}-%{release}

%description obj-c++
This package contains the GNU Objective C++ compiler. Objective C++ is an
object oriented language, created by Next Inc. and used in their
Nextstep OS. The source code is available in the gcc package.

%package ada
Summary:        GNU Ada Compiler Based on GCC (GNAT)
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{cross_pkgname} = %{version}-%{release}
Requires:       %{cross_pkgname}-ada = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libada = %{version}-%{release}
%else
Provides:       libada = %{version}-%{release}
%endif

%description ada
This package contains an Ada compiler and associated development
tools based on the GNU GCC technology.

%package fortran
Summary:        The GNU Fortran Compiler and Support Files
License:        GPL-3.0-or-later
Group:          Development/Languages/Fortran
Requires:       %{cross_pkgname} = %{version}-%{release}
Requires:       %{cross_pkgname}-fortran = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libgfortran = %{version}-%{release}
%else
Provides:       libgfortran = %{version}-%{release}
%endif

%description fortran
This is the Fortran compiler of the GNU Compiler Collection (GCC).

%package go
Summary:        GNU Go Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{cross_pkgname} = %{version}-%{release}
Requires:       %{cross_pkgname}-go = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libgo = %{version}-%{release}
%else
Provides:       libgo = %{version}-%{release}
%endif

%description go
This package contains a Go compiler and associated development
files based on the GNU GCC technology.

%package d
Summary:        GNU D Compiler
License:        GPL-3.0-or-later
Group:          Development/Languages/Other
Requires:       %{cross_pkgname} = %{version}-%{release}
Requires:       %{cross_pkgname}-d = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libgdruntime = %{version}-%{release}
Provides:       cross-mint-libgphobos = %{version}-%{release}
%else
Provides:       cross-mint-libgdruntime = %{version}-%{release}
Provides:       cross-mint-libgphobos = %{version}-%{release}
%endif

%description d
This package contains a D compiler and associated development
files based on the GNU GCC technology.

%package -n gcc-doc
Summary:        The system GNU Compiler documentation
License:        GFDL-1.2
Group:          Development/Languages/C and C++
BuildArch:      noarch

%description -n gcc-doc
The system GNU Compiler documentation.

%prep
%setup -q -n gcc-%{version}
%patch0 -p1
# %patch1 -p1

sh %{SOURCE1} ${RPM_SOURCE_DIR}

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
%if %{build_32bit}
GCC="${GCC} -m32"
GXX="${GXX} -m32"
%endif
BUILD_EXEEXT=
TARGET_EXEEXT=
PREFIX=/usr

case `uname -s` in
	MINGW64*) host=mingw64; MINGW_PREFIX=/mingw64; ;;
	MINGW32*) host=mingw32; MINGW_PREFIX=/mingw32; ;;
	MINGW*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	MSYS*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=mingw32; else host=mingw64; fi; MINGW_PREFIX=/$host ;;
	CYGWIN*) if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then host=cygwin32; else host=cygwin64; fi ;;
	Darwin*) host=macos; STRIP=strip; TAR_OPTS= ;;
	*) host=linux64
%if %{build_32bit}
	   host=linux32
%endif
	   ;;
esac
case $host in
	cygwin* | mingw* | msys*) BUILD_EXEEXT=.exe ;;
esac
case $host in
	mingw* | msys*) LN_S="cp -p" ;;
esac
%if %{build_32bit}
%define build_libdir %{_prefix}/lib
%else
%define build_libdir %{_libdir}
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
test "$BUILD" = "" && BUILD=`$srcdir/config.guess`; \
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


ranlib=ranlib
%define enable_plugins 0
%define enable_lto %(case "%{_rpmint_target}" in (*-*-*elf* | *-*-linux*) echo 1;; (*) echo 0;; esac)
%if %{enable_lto}
%if "%{buildtype}" == "cross"
%define enable_plugins %(case "%{BUILD}" in (*-*-linux*) echo 1;; (*) echo 0;; esac)
%endif
languages="$languages,lto"
# not here; we are just building it
# ranlib=gcc-ranlib
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

ranlib=${TARGET}-${ranlib}
strip="${TARGET}-strip"
as="${TARGET}-as"
STRIP=${STRIP-strip}
%if "%{buildtype}" != "cross"
STRIP=${strip}
export AS_FOR_TARGET="$as"
export RANLIB_FOR_TARGET="$ranlib"
export STRIP_FOR_TARGET="$strip"
export CC_FOR_TARGET="${TARGET}-gcc"
export CXX_FOR_TARGET="${TARGET}-g++"
%endif

[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir build-dir
cd build-dir

%if "%{buildtype}" != "cross"
cat <<'EOF' > "$RPM_BUILD_DIR/gcc-wrapper.sh"
!/bin/sh
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

cp "$RPM_BUILD_DIR/gcc-wrapper.sh" "$RPM_BUILD_DIR/gxx-wrapper.sh"
cat <<EOF >> "$RPM_BUILD_DIR/gcc-wrapper.sh"
eval exec "${TARGET}-gcc" \$cpu_flags \$args
EOF
cat <<EOF >> "$RPM_BUILD_DIR/gxx-wrapper.sh"
eval exec "${TARGET}-g++" \$cpu_flags \$args
EOF

chmod 755 "$RPM_BUILD_DIR/gcc-wrapper.sh"
chmod 755 "$RPM_BUILD_DIR/gxx-wrapper.sh"

export CC="${RPM_BUILD_DIR}/gcc-wrapper.sh $CPU_CFLAGS"
export CXX="$RPM_BUILD_DIR}/gxx-wrapper.sh $CPU_CFLAGS"

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
%if %{enable_plugins}
	--enable-plugin \
%else
	--disable-plugin \
%endif
	--disable-decimal-float \
	--disable-nls \
	--with-libiconv-prefix="${PREFIX}" \
	--with-libintl-prefix="${PREFIX}" \
%if "%{buildtype}" == "cross"
	--with-sysroot="${PREFIX}/${TARGET}/sys-root" \
%else
	--with-cpu=$with_cpu \
	--with-build-sysroot="%{_rpmint_target_prefix}/${TARGET}/sys-root" \
%endif
	--enable-languages="$languages"

make %{?_smp_mflags} all-gcc
make %{?_smp_mflags} all-target-libgcc
make %{?_smp_mflags}

# not quite right, but do the install already here;
# rpmbuild will use a different script during install,
# and our local variables are lost

case $host in
	mingw*) if test "${PREFIX}" = /usr; then PREFIX=${MINGW_PREFIX}; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
	macos*) if test "${PREFIX}" = /usr; then PREFIX=/opt/cross-mint; BUILD_LIBDIR=${PREFIX}/lib; fi ;;
esac

make DESTDIR="${RPM_BUILD_ROOT}" install

mkdir -p "${RPM_BUILD_ROOT}${PREFIX}/${TARGET}/bin"

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
%endif

cd "${RPM_BUILD_ROOT}${PREFIX}/bin"
${STRIP} *

	if test -x ${TARGET}-g++ && test ! -h ${TARGET}-g++; then
		rm -f ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}
		rm -f ${TARGET}-g++-${gcc_dir_version}${BUILD_EXEEXT} ${TARGET}-g++-${gcc_dir_version}
		mv ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++${BUILD_EXEEXT}
		if test ${BASE_VER} != ${gcc_dir_version}; then
		$LN_S ${TARGET}-g++-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-g++-${gcc_dir_version}${BUILD_EXEEXT}
		fi
	fi
	if test -x ${TARGET}-c++ && test ! -h ${TARGET}-c++; then
		rm -f ${TARGET}-c++${BUILD_EXEEXT} ${TARGET}-c++
		$LN_S ${TARGET}-g++${BUILD_EXEEXT} ${TARGET}-c++${BUILD_EXEEXT}
	fi
	if test -x ${TARGET}-gcc && test ! -h ${TARGET}-gcc; then
		rm -f ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-gcc-${BASE_VER}
		mv ${TARGET}-gcc${BUILD_EXEEXT} ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT}
		$LN_S ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-gcc${BUILD_EXEEXT}
	fi
	if test ${BASE_VER} != ${gcc_dir_version} && test -x ${TARGET}-gcc-${gcc_dir_version} && test ! -h ${TARGET}-gcc-${gcc_dir_version}; then
		rm -f ${TARGET}-gcc-${gcc_dir_version}${BUILD_EXEEXT} ${TARGET}-gcc-${gcc_dir_version}
		$LN_S ${TARGET}-gcc-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-gcc-${gcc_dir_version}${BUILD_EXEEXT}
	fi
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
%if "%{buildtype}" == "cross"
# on the host these may conflict with the system ones
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
	find . -name "lib*.a" | tar -c --files-from=- | tar -x -C ${RPM_BUILD_ROOT}%{gccsubdir}
	for i in libgfortran.spec libgomp.spec libitm.spec libsanitizer.spec libmpx.spec; do
		test -f $i && mv $i ${RPM_BUILD_ROOT}%{gccsubdir}
		find . -name "$i" -delete
	done
	find . -name "lib*.a" -delete
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

	for f in ${BUILD_LIBDIR#/}/gcc/${TARGET}/*/{cc1,cc1plus,cc1obj,cc1objplus,f951,d21,collect2,lto-wrapper,lto1,gnat1,gnat1why,gnat1sciln,go1,brig1}${BUILD_EXEEXT} \
		${BUILD_LIBDIR#/}/gcc/${TARGET}/*/${LTO_PLUGIN} \
		${BUILD_LIBDIR#/}/gcc/${TARGET}/*/plugin/gengtype${BUILD_EXEEXT} \
		${BUILD_LIBDIR#/}/gcc/${TARGET}/*/install-tools/fixincl${BUILD_EXEEXT}; do
		test -f "$f" && ${STRIP} "$f"
	done
	rmdir ${PREFIX#/}/include || :
	
	if test -f ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN}; then
		mkdir -p ${PREFIX#/}/lib/bfd-plugins
		cd ${PREFIX#/}/lib/bfd-plugins
		rm -f ${MY_LTO_PLUGIN}
		$LN_S ../../${BUILD_LIBDIR##*/}/gcc/${TARGET}/${gcc_dir_version}/${LTO_PLUGIN} ${MY_LTO_PLUGIN}
		cd "${INSTALL_DIR}"
	fi
	
	find ${PREFIX#/} -name "*.a" -exec "${strip}" -S -x '{}' \;
	find ${PREFIX#/} -name "*.a" -exec "${ranlib}" '{}' \;
	
	cd ${BUILD_LIBDIR#/}/gcc/${TARGET}/${gcc_dir_version}/include-fixed && {
		for i in `find . -type f`; do
			case $i in
			./README | ./limits.h | ./syslimits.h) ;;
			*) echo "removing fixed include file $i"; rm -f $i ;;
			esac
		done
		for i in `find . -depth -type d`; do
			test "$i" = "." || rmdir "$i"
		done
	}


%install

%rpmint_cflags

# already done above
# make install DESTDIR=${RPM_BUILD_ROOT}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-gcc*
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-cpp*
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-gcov*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gcc*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gcov*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/cpp*
%if "%{buildtype}" == "cross"
%else
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
%{gccsubdir}/*/*/*/libgcc*
%{gccsubdir}/libgcov*
%{gccsubdir}/*/libgcov*
%{gccsubdir}/*/*/libgcov*
%{gccsubdir}/*/*/*/libgcov*
%{gccsubdir}/libssp*
%{gccsubdir}/*/libssp*
%{gccsubdir}/*/*/libssp*
%{gccsubdir}/*/*/*/libssp*
%{gccsubdir}/libmudflap*
%{gccsubdir}/*/libmudflap*
%{gccsubdir}/*/*/libmudflap*
%{gccsubdir}/*/*/*/libmudflap*
%if %{enable_lto}
%{gccsubdir}/lto1
%endif
%if %{enable_plugins}
%{gccsubdir}/liblto_plugin*
%{gccsubdir}/plugin
%{_prefix}/lib/bfd-plugins
%endif

%if "%{buildtype}" != "cross"
%files doc
%defattr(-,root,root)
%{_rpmint_target_prefix}/share/man/*/*
%{_rpmint_target_prefix}/share/info/*
%endif

%if %{build_cp}
%files c++
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-c++*
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-g++*
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
%{gccsubdir}/*/*/libstdc++*
%{gccsubdir}/*/*/*/libstdc++*
%{gccsubdir}/libsupc++*
%{gccsubdir}/*/libsupc++*
%{gccsubdir}/*/*/libsupc++*
%{gccsubdir}/*/*/*/libsupc++*
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
%{gccsubdir}/*/*/libobjc*
%{gccsubdir}/*/*/*/libobjc*
%endif

%if %{build_objcp}
%files obj-c++
%defattr(-,root,root)
%{gccsubdir}/cc1objplus
%endif

%if %{build_fortran}
%files fortran
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-gfortran*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gfortran*
%{gccsubdir}/f951
%{gccsubdir}/libgfortran*
%{gccsubdir}/*/libgfortran*
%{gccsubdir}/*/*/libgfortran*
%{gccsubdir}/*/*/*/libgfortran*
%if %{gcc_major_ver} >= 6
%{gccsubdir}/libcaf*
%{gccsubdir}/*/libcaf*
%{gccsubdir}/*/*/libcaf*
%{gccsubdir}/*/*/*/libcaf*
%endif
%endif

%if %{build_ada}
%files ada
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-gnat*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/gnat*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gnat*
%endif
%{gccsubdir}/gnat1
%{gccsubdir}/adalib
%{gccsubdir}/adainclude
%endif

%if %{build_go}
%files go
%defattr(-,root,root)
%{_rpmint_target_prefix}/bin/%{_rpmint_target_platform}-go*
%{_rpmint_target_prefix}/%{_rpmint_target}/bin/go*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/go*
%endif
%{gccsubdir}/go1
%{gccsubdir}/cgo
%{gccsubdir}/libgo*
%{gccsubdir}/*/libgo*
%{gccsubdir}/*/*/libgo*
%{gccsubdir}/*/*/*/libgo*
%{build_libdir}/go/%{gcc_dir_version}
%endif


%changelog
* Fri Aug 21 2020 Thorsten Otto <admin@tho-otto.de>
- first RPMint spec file for gcc 4.6.4
