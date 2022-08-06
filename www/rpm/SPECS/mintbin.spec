%define pkgname mintbin

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Supplementary tools to the GNU binutils for MiNT
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.3
Release:        20200828
License:        GPL-2.0-or-later
Group:          Development/Languages/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/freemint/mintbin

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        mintbin-%{version}.tar.xz


%if "%{buildtype}" == "cross"
BuildRequires:  binutils
BuildRequires:  gcc
%else

BuildRequires:  cross-mint-binutils
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
MiNTBin has been written by Guido Flohr. It is a set of tools for
manipulating the MiNT executables generated by ld. They are a
complement to the binutils. The main tools are stack for setting the
stack size of an executable, and flags for setting the header flags. 

%prep
%setup -q -n %{pkgname}-%{version}


%build

%rpmint_cflags
unset PKG_CONFIG_LIBDIR
unset PKG_CONFIG_PATH

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

tools="arconv cnm csize cstrip flags mintbin stack symex"

CONFIGURE_FLAGS="--disable-nls"

%if "%{buildtype}" == "cross"

GCC=${GCC-gcc}
export CC="${GCC}"

CONFIGURE_FLAGS+=" --target=%{_rpmint_target_platform} --prefix=%{_prefix}"

CFLAGS="$COMMON_CFLAGS" \
LDFLAGS="$COMMON_CFLAGS" \
./configure ${CONFIGURE_FLAGS}

make %{?_smp_mflags}
make DESTDIR=%{buildroot} install
strip %{buildroot}%{_bindir}/*
%rpmint_gzip_docs
pushd %{buildroot}%{_prefix}/%{_rpmint_target_platform}/bin
for i in $tools; do
	if test -x $i; then
		rm -f ${i} ${i}${BUILD_EXEEXT}
		$LN_S ../../bin/%{_rpmint_target_platform}-$i${BUILD_EXEEXT} $i
	fi
done
popd

%else

CONFIGURE_FLAGS+=" --host=%{_rpmint_target_platform} --prefix=%{_rpmint_target_prefix} --disable-nls"

for CPU in %{buildtype}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS}

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot} install
	# seems to be bug in Makefile
	rm -f %{buildroot}%{_rpmint_target_prefix}/bin/-*

	pushd %{buildroot}%{_rpmint_target_prefix}/bin
	for i in $tools; do
		if test -x $i; then
			rm -f %{_rpmint_target_platform}-${i}
			$LN_S $i %{_rpmint_target_platform}-${i}
		fi
	done
	popd

	# compress manpages
	%rpmint_gzip_docs

	"%{_rpmint_target_strip}" %{buildroot}%{_rpmint_target_prefix}/bin/*

	make distclean
done

%endif


%install

# already done in loop above
# make install DESTDIR=%{buildroot}%{_rpmint_sysroot}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_bindir}/*
%{_prefix}/%{_rpmint_target_platform}/bin/*
%{_prefix}/%{_rpmint_target_platform}/include
%{_infodir}
%else
%{_rpmint_target_prefix}/bin/*
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/share/info
%endif

%post
%if "%{buildtype}" == "cross"
%install_info --info-dir=%{_infodir} %{_infodir}/%{pkgname}.info%{ext_info}
%else
%install_info --info-dir=%{_rpmint_target_prefix}/share/info %{_rpmint_target_prefix}/share/info/%{pkgname}.info%{ext_info}
%endif

%preun
%if "%{buildtype}" == "cross"
%install_info_delete --info-dir=%{_infodir} %{_infodir}/%{pkgname}.info%{ext_info}
%else
%install_info_delete --info-dir=%{_rpmint_target_prefix}/share/info %{_rpmint_target_prefix}/share/info/%{pkgname}.info%{ext_info}
%endif


%changelog
* Fri Aug 28 2020 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file