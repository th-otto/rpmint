%define gcc_major_ver 2
%define pkgname gcc%{gcc_major_ver}

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

%if "%{buildtype}" == "cross"
%define cross_pkgname  cross-mint-%{pkgname}
%else
%define cross_pkgname  %{pkgname}
%endif

Summary       : Various compilers (C, C++, Objective-C, Chill, ...)
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 2.95.3
Release       : 7
%define releasedate 20230312
License       : GPL-2.0-or-later
Group         : Development/Languages

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : http://gcc.gnu.org/

BuildRequires:  cross-mint-binutils
BuildRequires:  cross-mint-mintlib-headers
BuildRequires:  cross-mint-fdlibm-headers
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  flex

Prefix        : %{_prefix}
Docdir        : %{_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}.tar.gz
Source1: gcc-2.95.3-README.MiNT
Patch1:  gcc-2.95.3-mint-20230311.patch

%if "%{buildtype}" == "cross"
# can only be built as 32bit version
%define _target_cpu i686
%define _host_cpu i686
%define _arch i686
BuildRequires:  gcc-c++
BuildRequires:  cross-mint-binutils
Provides:       cross-mint-%{pkgname} = %{version}-%{release}
%else
BuildRequires:  cross-mint-mintlib-gcc2
BuildRequires:  cross-mint-pml-gcc2 >= 2.03
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

%define TARGET %{_rpmint_target}
%define gcc_dir_version %version
%define gccsubdir %{_prefix}/lib/gcc-lib/%{TARGET}/%{version}
%if "%{buildtype}" == "cross"
# for consistency with newer gcc
%define gxxinclude %{_rpmint_target_prefix}/include/c++/%{gcc_dir_version}
%else
# traditionally, this were installed in a different place than later gcc versions
%define gxxinclude %{_rpmint_target_prefix}/include/g++-3
%endif


%description
The gcc package contains the GNU Compiler Collection: cc and gcc. You'll need
this package in order to compile C code.

%package c++
Summary       : C++ support for gcc
License:        GPL-2.0-or-later
Group         : Development/Languages
Requires      : %{pkgname} = %{version}-%{release}
Requires:       %{name}-c++ = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libstdc++-devel = %{version}-%{release}
Provides:       cross-mint-c++ = %{version}-%{release}
Provides:       cross-mint-gcc-c++ = %{version}-%{release}
%else
BuildRequires:  cross-mint-%{pkgname}-c++ = %{version}
Provides:       libstdc++-devel = %{version}-%{release}
Provides:       c++ = %{version}-%{release}
Provides:       c++-compiler
%endif

%description c++
This package adds C++ support to the GNU C compiler. It includes support
for most of the current C++ specification, including templates and
exception handling. It does include the static standard C++
library and C++ header files.

%package objc
License:        GPL-2.0-or-later
Summary       : Objective C support for gcc
Group         : Development/Languages
Requires      : %{pkgname} = %{version}
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-objc = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libobjc = %{version}-%{release}
Provides:       cross-mint-gcc-objc = %{version}-%{release}
%else
BuildRequires:  cross-mint-%{pkgname}-objc = %{version}
Provides:       libobjc = %{version}-%{release}
Provides:       gcc-objc = %{version}-%{release}
%endif

%description objc
gcc-objc provides Objective C support for the GNU C compiler (gcc).
Mainly used on systems running NeXTSTEP, Objective C is an
object-oriented derivative of the C language.

Install gcc-objc if you are going to do Objective C development and
you would like to use the gcc compiler.  You'll also need gcc.

Note: libobjc is currently not available as multilib

%package fortran
Summary       : Fortran 77 support for gcc
License:        GPL-2.0-or-later
Group         : Development/Languages
Requires      : %{pkgname} = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libgfortran = %{version}-%{release}
Provides:       cross-mint-gcc-fortran = %{version}-%{release}
%else
BuildRequires:  cross-mint-%{pkgname}-fortran = %{version}
Provides:       libgfortran = %{version}-%{release}
Provides:       gcc-fortran = %{version}-%{release}
%endif

%description fortran
The gcc-g77 package provides support for compiling Fortran 77
programs with the GNU gcc compiler.

You should install gcc-g77 if you are going to do Fortran development
and you would like to use the gcc compiler.  You will also need gcc.

%package chill
Summary       : CHILL support for gcc
License:        GPL-2.0-or-later
Group         : Development/Languages
Requires      : %{pkgname} = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-libchill = %{version}-%{release}
Provides:       cross-mint-gcc-chill = %{version}-%{release}
%else
BuildRequires:  cross-mint-%{pkgname}-chill = %{version}
Provides:       libchill = %{version}-%{release}
Provides:       gcc-chill = %{version}-%{release}
%endif

%description chill
This package adds support for compiling CHILL programs with the GNU
compiler.

Chill is the "CCITT High-Level Language", where CCITT is the old
name for what is now ITU, the International Telecommunications Union.
It is a language in the Modula2 family, and targets many of the
same applications as Ada (especially large embedded systems).
Chill was never used much in the United States, but is still
being used in Europe, Brazil, Korea, and other places.

%package java
Summary       : Java support for gcc
License:        GPL-2.0-or-later
Group         : Development/Languages
Requires      : %{pkgname} = %{version}-%{release}
%if "%{buildtype}" == "cross"
Provides:       cross-mint-gcc-java = %{version}-%{release}
%else
BuildRequires:  cross-mint-%{pkgname}-java = %{version}
Provides:       gcc-java = %{version}-%{release}
%endif

%description java
This package adds experimental support for compiling Java(tm) programs and
bytecode into native code. To use this you will also need the gcc-libgcj
package.
Note: gcc-libgcj is currently not available for m68k-atari-mint!


%package doc
Summary:        The system GNU Compiler documentation
License:        GFDL-1.2
Group:          Development/Languages/C and C++
BuildArch:      noarch

%description doc
The system GNU Compiler documentation.

## ##################################
# P R E P
# ##################################
%prep
%setup -q -n gcc-%{version}
%patch1 -p1

cp %{SOURCE1} gcc/README.MiNT


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
	(m68k-unknown-mint*) BUILD=m68k-atari-mint ;; \
esac; \
echo $BUILD
)
BUILD=%{BUILD}

# when checked out from git, we cannot be sure
# about the timestamps of the configure scripts.
# Make sure autoconf won't run, since newer versions
# of autoconf will produce broken scripts
# from those ancient configure.in scripts
find $srcdir -name configure | xargs touch

# Dito for some other generated files
touch "$srcdir/gcc/c-gperf.h"


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

rm -rf build-dir
mkdir build-dir
cd build-dir

#
# the hosts compiler
#
export CC=${CC-gcc}
export CXX=${CXX-g++}
BUILD_EXEEXT=
TARGET_EXEEXT=
PREFIX=%{_prefix}

case `uname -s` in
	Linux*)
		host=linux64
		BUILD=x86_64-pc-linux
		if echo "" | ${GCC} -dM -E - 2>/dev/null | grep -q i386; then
			host=linux32
		fi
		;;
	*)
		echo "Build on $host not supported!" >&2
		exit 1
		;;
esac

# On 64-bit architecture GNU Assembler crashes writing out an object, due to
# (probably) miscalculated structure sizes.  There could be some other bugs
# lurking there in 64-bit mode, but I have little incentive chasing them.
# Also, the build system of gcc-2 does not recognize any 64bit host architecture at all.
# Just compile everything in 32-bit mode and forget about the issues.
case `uname -m` in
  x86_64)
    ARCH=" -m32"
    BUILD=i686-${BUILD#*-}
    test "$host" = linux64 && host=linux32
    ;;
esac
CC="$CC$ARCH"
CXX="$CXX$ARCH"


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
		-m5200) cpu_flags=$1 ;;
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

export CFLAGS="-O2 -fomit-frame-pointer"
export CXXFLAGS="-O -fomit-frame-pointer"

%endif

%if "%{buildtype}" == "cross"
%define build_libdir %{_prefix/lib}
%else
%define build_libdir %{_rpmint_target_prefix}/lib
%endif
BUILD_LIBDIR=%{build_libdir}


#
# create symlinks to mintlib headers,
# otherwise gcc configure script will copy them.
# (yuks, this really works on the absolute path)
#
#rm -f ${PREFIX}/${TARGET}/sys-include
#ln -s sys-root/usr/include ${PREFIX}/${TARGET}/sys-include
#if test "${PREFIX}" != /usr; then
#	ln -sf %{_rpmint_sysroot} ${PREFIX}/${TARGET}/sys-root
#	rm -f ${PREFIX}/${TARGET}/lib
#fi

#
# Setting AR_FOR_TARGET already here does not work,
# it is overwritten in the Makefiles.
# Provide symlinks instead
ranlib=`which ${TARGET}-ranlib 2>/dev/null`
strip=`which "${TARGET}-strip" 2>/dev/null`
as=`which "${TARGET}-as" 2>/dev/null`
ld=`which "${TARGET}-ld" 2>/dev/null`
nm=`which "${TARGET}-nm" 2>/dev/null`
ar=`which "${TARGET}-ar" 2>/dev/null`
if test "$ranlib" = "" -o ! -x "$ranlib" -o ! -x "$as" -o ! -x "$strip"; then
	echo "cross-binutil tools for ${TARGET} not found" >&2
	exit 1
fi
mkdir -p binutils
ln -sf "$ar" binutils/ar
ln -sf "$nm" binutils/nm
ln -sf "$nm" binutils/nm-new
ln -sf "$ld" binutils/ld
ln -sf "$ranlib" binutils/ranlib


# 
# C++ with simple optimization, C++ Optimizer seems to be buggy
# 
CC="$CC" \
CXX="$CXX" \
CFLAGS_FOR_BUILD="$CFLAGS_FOR_BUILD" \
CFLAGS="$CFLAGS_FOR_BUILD" \
CXXFLAGS_FOR_BUILD="$CXXFLAGS_FOR_BUILD" \
CXXFLAGS="$CXXFLAGS_FOR_BUILD" \
BOOT_CFLAGS="$CFLAGS_FOR_BUILD" \
CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET" \
CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET" \
LDFLAGS_FOR_BUILD="$LDFLAGS_FOR_BUILD" \
LDFLAGS="$LDFLAGS_FOR_BUILD" \
../configure \
	--target="${TARGET}" \
%if "%{buildtype}" != "cross"
	--host="${TARGET}" \
%else
	--host="${BUILD}" \
%endif
	--build="${BUILD}" \
	--prefix="${PREFIX}" \
	--libdir='${prefix}/lib' \
	--bindir='${prefix}/bin' \
	--libexecdir='${libdir}' \
	--infodir='${prefix}/share/info' \
	--mandir='${prefix}/share/man' \
%if "%{buildtype}" == "cross"
	--with-gxx-include-dir=%{_rpmint_sysroot}%{gxxinclude} \
%else
	--with-gxx-include-dir=%{gxxinclude} \
%endif
	--with-gcc \
	--with-gnu-ld \
	--with-gnu-as \
	--disable-threads \
	--disable-nls \
	--program-suffix=-%{version} \
	--without-newlib \
	--enable-version-specific-runtime-libs \
	|| exit 1

# as I have already installed the gcc 2.95.2 and compiled
# it several times there is no reason to bootstrap the
# compiler again and again
# it save lot of time to skip stage1 and stage2 and go
# directly to stage3
#make bootstrap ||:
make %{?_smp_mflags} || :
# seems we have to run it again to produce the target libraries
make %{?_smp_mflags} || :
make || exit 1

# run the tests - not possible yet
# make -k check || true


# ##################################
# I N S T A L L
# ##################################
%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%rpmint_cflags
PREFIX=%{_prefix}

gcc_major_version=%{gcc_major_ver}
gcc_dir_version=%{gcc_dir_version}
BASE_VER=%{version}
BUILD_LIBDIR=%{build_libdir}	

cd build-dir

# gxx_include_dir is evaled and does not contain '$(prefix)' anymore in Makefiles :(
%if "%{buildtype}" == "cross"
gxx_include_dir="${RPM_BUILD_ROOT}%{_rpmint_sysroot}%{gxxinclude}"
%else
gxx_include_dir="${RPM_BUILD_ROOT}%{gxxinclude}"
%endif
make prefix="${RPM_BUILD_ROOT}${PREFIX}" gxx_include_dir="${gxx_include_dir}" install

# ranlib is always used for target libraries
ranlib=%{_rpmint_target}-ranlib
# strip is sometimes used for host executables,
# sometimes for target libraries
strip_for_host="strip -p"
strip_for_target="%{_rpmint_target}-strip -p"
%if "%{buildtype}" != "cross"
strip_for_host="${strip_for_target}"
%endif

gcc_dir_version=%{version}
gccsubdir=%{gccsubdir}
gccsubdir=${gccsubdir#/}

cd "${RPM_BUILD_ROOT}"

#
# Remove info pages. They are same as man pages, and we would have to rename them,
# but that also requires fixing the links in them
#
# rm -rf ${PREFIX#/}/share/info

#
# zip man pages
%if "%{buildtype}" == "cross"
test -f ${PREFIX#/}/share/man/man1/${TARGET}-cccp.1 && mv ${PREFIX#/}/share/man/man1/${TARGET}-cccp.1 ${PREFIX#/}/share/man/man1/${TARGET}-cpp.1 
%else
test -f ${PREFIX#/}/share/man/man1/cccp.1 && mv ${PREFIX#/}/share/man/man1/cccp.1 ${PREFIX#/}/share/man/man1/cpp.1 
%endif
for i in ${PREFIX#/}/share/man/man1/*.1; do
	b=${i##*/}
	b=${b%*.1}
	case $b in 
	${TARGET}-*) ;;
	*) b=${TARGET}-${b} ;;
	esac
	mv $i ${PREFIX#/}/share/man/man1/${b}-%{version}.1
done
for i in ${PREFIX#/}/share/info/*.info*; do
	b=${i##*/}
	e=${b#*.info*}
	b=${b%*.info*}
	case $b in
	${TARGET}-*) ;;
	*) b=${TARGET}-${b} ;;
	esac
	mv $i ${PREFIX#/}/share/info/${b}-%{version}${e}
done
gzip -9nf ${PREFIX#/}/share/man/*/* ${PREFIX#/}/share/info/*

gcc_major_version=$(echo %{version} | cut -d '.' -f 1)

#
# when cross-compiling, some executables are installed without the target prefix.
# All of them are installed without the program suffix. Fix it.
#
cd "${PREFIX#/}/bin"
${strip_for_host} * || :
for i in cpp gcjh gcov jcf-dump jv-scan c++ c++filt chill g++ g77 gcc gcj protoize unprotoize; do
	if test -f $i; then
		rm -f ${TARGET}-$i-%{version}
		mv $i ${TARGET}-$i-%{version}
	fi
	if test -f ${TARGET}-$i; then
		rm -f ${TARGET}-$i-%{version}
		mv ${TARGET}-$i ${TARGET}-$i-%{version}
	fi
done

LN_S="ln -s"

# only links to major version here; gcc-2 is not the default compiler anymore
for tool in gcc g++ cpp; do
	if test ${BASE_VER} != ${gcc_major_version}; then
		rm -f ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}
		$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT}
	fi
done


# java & chill are not supported in later versions, and are therefore still default
for tool in gcj gcjh jcf-dump jv-scan chill; do
	if test -x ${TARGET}-$tool-${BASE_VER}; then
		rm -f ${TARGET}-${tool}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}
		$LN_S ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-${tool}${BUILD_EXEEXT}
		if test ${BASE_VER} != ${gcc_major_version}; then
			rm -f ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}
			$LN_S ${TARGET}-${tool}-${BASE_VER}${BUILD_EXEEXT} ${TARGET}-${tool}-${gcc_major_version}${BUILD_EXEEXT}
		fi
	fi
done

%if "%{buildtype}" != "cross"
for tool in gcc cpp g++ gcov gcj gcjh jcf-dump jv-scan chill; do
	rm -f ${tool}
	$LN_S ${TARGET}-${tool} ${tool}
done
rm -f c++ cc f77
$LN_S g++ c++
$LN_S gcc cc
$LN_S g77 f77
%endif

cd ../..

mkdir -p "${PREFIX#/}/${TARGET}/bin"
cd "${PREFIX#/}/${TARGET}/bin"
for tool in gcc g++ g77 gcov cpp; do
		if test -x ../../bin/${TARGET}-${tool}-%{version}; then
			rm -f ${tool} ${tool}${BUILD_EXEEXT}
			$LN_S ../../bin/${TARGET}-${tool}${BUILD_EXEEXT} ${tool}
		fi
done
cd ../../..

# libiberty is only used by gcc itself, no need to install it
find ${PREFIX#/} -name libiberty.a -delete -printf "rm %p\n"
find ${PREFIX#/} -type f -name "*.la" -delete -printf "rm %p\n"
# seems to be duplicate to m5475
find ${PREFIX#/}/${TARGET} -type d -name m5200 -exec rm -rf '{}' \;
find ${gccsubdir} -type d -name m5200 -exec rm -rf '{}' \;

#
# move compiler dependant libraries to the gcc subdirectory
#
%if "%{buildtype}" == "cross"
dir="${PREFIX#/}/${TARGET}/lib"
%else
dir="${PREFIX#/}/lib"
%endif
libs=`find $dir -name "libstdc*" ! -path "*/gcc-lib/*" | sed -e "s@^$dir/@@"`
for i in $libs; do
    d=${gccsubdir}/${i%%.*}.a
    case $d in
       */libstdc++.a.2*) d=${d%/*}/libstdc++.a ;;
    esac
    rm -f "$d"
    mv "$dir/$i" "$d" || exit 1
done
find ${PREFIX#/}/${TARGET}/lib -depth -type d | xargs rmdir || :
if test -f ${PREFIX#/}/${TARGET}/include/_G_config.h; then
	mv ${PREFIX#/}/${TARGET}/include/_G_config.h ${gxx_include_dir}
fi
rm -f ${PREFIX#/}/${TARGET}/include/assert.h
rm -f ${PREFIX#/}/include/assert.h
rmdir ${PREFIX#/}/${TARGET}/include || :


for f in ${gccsubdir}/{cc1,cc1plus,cc1obj,cc1objplus,cc1chill,cpp0,f771,f951,d21,collect2,lto-wrapper,lto1,gnat1,gnat1why,gnat1sciln,go1,brig1,jc1,jvgenmain,g++-mapper-server}${BUILD_EXEEXT} \
	${gccsubdir#/}/install-tools/fixincl${BUILD_EXEEXT}; do
	test -f "$f" && ${strip_for_host} "$f"
done

find ${PREFIX#/} -name "*.a" -exec ${strip_for_target} -S -x '{}' \;
find ${PREFIX#/} -name "*.a" -exec ${ranlib_for_target} '{}' \;


# ##################################
# C L E A N
# ##################################
%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


# ##################################
# F I L E S
# ##################################
%files
%defattr(-,root,root)
%doc gcc/README* gcc/*ChangeLog* gcc/PROBLEMS gcc/NEWS gcc/SERVICE gcc/BUGS gcc/LANGUAGES
%{_rpmint_target_prefix}/bin/%{TARGET}-gcc*
%{_rpmint_target_prefix}/bin/%{TARGET}-cpp*
%{_rpmint_target_prefix}/bin/%{TARGET}-gcov*
%{_rpmint_target_prefix}/bin/%{TARGET}-protoize*
%{_rpmint_target_prefix}/bin/%{TARGET}-unprotoize*
%{_rpmint_target_prefix}/%{TARGET}/bin/gcc
%{_rpmint_target_prefix}/%{TARGET}/bin/gcov
%{_rpmint_target_prefix}/%{TARGET}/bin/cpp
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gcc*
%{_rpmint_target_prefix}/bin/cpp*
%{_rpmint_target_prefix}/bin/gcov*
%{_rpmint_target_prefix}/bin/cc
%endif
%dir %{gccsubdir}
%dir %{gccsubdir}/include
%dir %{gccsubdir}/m68020-60
%dir %{gccsubdir}/m68020-60/mshort
%dir %{gccsubdir}/m5475
%dir %{gccsubdir}/m5475/mshort
%dir %{gccsubdir}/mshort
%{gccsubdir}/cc1
%{gccsubdir}/collect2
%{gccsubdir}/cpp0
%{gccsubdir}/include/README
%{gccsubdir}/include/float.h
%{gccsubdir}/include/iso646.h
%{gccsubdir}/include/limits.h
%{gccsubdir}/include/proto.h
%{gccsubdir}/include/stdarg.h
%{gccsubdir}/include/stdbool.h
%{gccsubdir}/include/stddef.h
%{gccsubdir}/include/syslimits.h
%{gccsubdir}/include/varargs.h
%{gccsubdir}/include/va-*.h
%{gccsubdir}/libgcc.a
%{gccsubdir}/*/libgcc.a
%{gccsubdir}/*/*/libgcc.a
%{gccsubdir}/SYSCALLS.c.X
%{gccsubdir}/specs

%files c++
%defattr(-,root,root)
%doc gcc/cp/NEWS gcc/cp/ChangeLog*
%{_rpmint_target_prefix}/bin/%{TARGET}-g++*
%{_rpmint_target_prefix}/bin/%{TARGET}-c++*
%{_rpmint_target_prefix}/%{TARGET}/bin/g++
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/g++*
%{_rpmint_target_prefix}/bin/c++*
%{gxxinclude}
%else
%{_rpmint_sysroot}%{gxxinclude}
%endif
%{gccsubdir}/cc1plus
%{gccsubdir}/include/exception
%{gccsubdir}/include/new
%{gccsubdir}/include/new.h
%{gccsubdir}/include/typeinfo
%{gccsubdir}/libstdc++.a*
%{gccsubdir}/*/libstdc++.a*
%{gccsubdir}/*/*/libstdc++.a*

%files objc
%defattr(-,root,root)
%doc gcc/objc/README libobjc/THREADS* libobjc/ChangeLog
%{gccsubdir}/cc1obj
# NOTE: not build with multilib-support
%{gccsubdir}/libobjc.a
%{gccsubdir}/include/objc

%files fortran
%defattr(-,root,root)
%doc gcc/f/README gcc/ChangeLog*
%{_rpmint_target_prefix}/bin/%{TARGET}-g77*
%{_rpmint_target_prefix}/%{TARGET}/bin/g77
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/f77
%endif
%{gccsubdir}/f771
%{gccsubdir}/libg2c.a
%{gccsubdir}/*/libg2c.a
%{gccsubdir}/*/*/libg2c.a
%{gccsubdir}/include/g2c.h

%files chill
%defattr(-,root,root)
%doc gcc/ch/README gcc/ch/chill.brochure gcc/ChangeLog*
%{_rpmint_target_prefix}/bin/%{TARGET}-chill*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/chill
%endif
%{gccsubdir}/cc1chill
%{gccsubdir}/chill*.o
%{gccsubdir}/libchill.a
%{gccsubdir}/*/chill*.o
%{gccsubdir}/*/libchill.a
%{gccsubdir}/*/*/chill*.o
%{gccsubdir}/*/*/libchill.a

%files java
%defattr(-,root,root)
%doc gcc/java/ChangeLog*
%{_rpmint_target_prefix}/bin/%{TARGET}-gcj*
%{_rpmint_target_prefix}/bin/%{TARGET}-jcf-dump*
%{_rpmint_target_prefix}/bin/%{TARGET}-jv-scan*
%if "%{buildtype}" != "cross"
%{_rpmint_target_prefix}/bin/gcj
%{_rpmint_target_prefix}/bin/gcjh
%{_rpmint_target_prefix}/bin/jcf-dump
%{_rpmint_target_prefix}/bin/jv-scan
%endif
%{gccsubdir}/jc1
%{gccsubdir}/jvgenmain


%files doc
%defattr(-,root,root)
%{_rpmint_target_prefix}/share/man/*/*
%{_rpmint_target_prefix}/share/info/*


%changelog
* Sun Mar 12 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Tue Jun 15 2010 Keith Scroggins <kws@radix.net>
- Compiled against latest MiNTLib and renamed package to gcc2 to become the
- legacy compiler for MiNT

* Thu Feb 27 2003 Frank Naumann <fnaumann@freemint.de>
- fixed bug in -pg option for the mint port

* Sat Mar 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.95.3

* Sat Mar 03 2001 Frank Naumann <fnaumann@freemint.de>
- rebuild against MiNTLib 0.56

* Tue Feb 29 2000 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
