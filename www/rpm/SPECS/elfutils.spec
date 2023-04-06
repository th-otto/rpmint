%define pkgname elfutils

%rpmint_header

Summary:        Higher-level library to access ELF files
Name:           %{crossmint}%{pkgname}
Version:        0.170
Release:        1
License:        GPL-2.0-or-later OR LGPL-3.0-or-later
Group:          Development/Tools/Building

Packager:       %{packager}
URL:            https://sourceware.org/elfutils/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://sourceware.org/pub/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.bz2
Source1: patches/automake/mintelf-config.sub

Patch0: patches/elfutils/elfutils-disable-tests-with-ptrace.patch
Patch3: patches/elfutils/elfutils-no-threads.patch
Patch4: patches/elfutils/elfutils-mint.patch
Patch5: patches/elfutils/elfutils-lto-warnings.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  %{crossmint}gcc-c++
BuildRequires:  %{crossmint}libbz2-devel
BuildRequires:  %{crossmint}libzstd-devel
BuildRequires:  %{crossmint}xz-devel
BuildRequires:  %{crossmint}zlib-devel
BuildRequires:  %{crossmint}zstd
Provides:       %{crossmint}libelf-devel
Provides:       %{crossmint}libdw-devel
Provides:       %{crossmint}libasm-devel
Provides:       %{crossmint}libebl-devel

%rpmint_build_arch

%description
elfutils is a collection of utilities and libraries to read, create
and modify ELF binary files, find and handle DWARF debug data,
symbols, thread state and stacktraces for processes and core files.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Change DATE/TIME macros to use last change time of ChangeLog
modified=$(head -1 ChangeLog | cut -d" " -f1)
DATE=$(date -d "${modified}" "+%Y-%m-%d")
TIME=$(date -d "${modified}" "+%R")
find . -type f -regex ".*\.c\|.*\.cpp\|.*\.h" -exec sed -i "s/__DATE__/\"${DATE}\"/g;s/__TIME__/\"${TIME}\"/g" {} +
# Set modversion used to verify dynamically loaded ebl backend matches to
# similarly predictable value [upstream default is hostname + date]
MODVERSION="%{vendor} ${DATE} ${TIME}"
sed --in-place "s/^MODVERSION=.*\$/MODVERSION=\"${MODVERSION}\"/" configure.ac

autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--disable-nls
	--disable-shared
	--program-prefix=eu-
	--config-cache
"

for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	rm -f config.cache
	if test "$LTO_CFLAGS" != ""; then
		echo 'ac_cv_stack_usage=no' >> config.cache
		echo 'ac_cv_null_dereference=no' >> config.cache
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

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
%license COPYING
%doc AUTHORS ChangeLog NEWS NOTES README THANKS TODO
%{_isysroot}/%{_rpmint_target_prefix}/bin/*
%{_isysroot}/%{_rpmint_target_prefix}/include/*
%{_isysroot}/%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}/%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}/%{_rpmint_target_prefix}/lib/pkgconfig/*.pc
%if "%{buildtype}" == "cross"
%{_rpmint_cross_pkgconfigdir}
%endif


%changelog
* Thu Apr 06 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
