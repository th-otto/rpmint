%define pkgname newt

%rpmint_header

Summary:        A development library for text mode user interfaces.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.50
Release:        5
License:        LGPL-2.0-or-later
Group:          Applications/System

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://github.com/strukturag/libde265/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.redhat.com/pub/redhat/code/newt/newt-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/newt-inc.patch
Patch1:  patches/%{pkgname}/newt-mint.patch
Patch2:  patches/%{pkgname}/newt-autoconf.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
%if "%{buildtype}" == "cross"
Requires:       cross-mint-slang
Provides:       cross-mint-newt-devel
%else
Requires:       slang
Provides:       newt-devel
%endif

%rpmint_build_arch

%description
Newt is a programming library for color text mode, widget based user
interfaces.  Newt can be used to add stacked windows, entry widgets,
checkboxes, radio buttons, labels, plain text fields, scrollbars,
etc., to text mode user interfaces.  This package also contains the
shared library needed by programs built with newt, as well as a
/usr/bin/dialog replacement called whiptail.  Newt is based on the
slang library.

The newt-devel package contains the header files and libraries
necessary for developing applications which use newt.  Newt is a
development library for text mode user interfaces.  Newt is based on
the slang library.

Install newt-devel if you want to develop applications which will use
newt.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

#autoconf || exit 1
#autoheader || exit 1
#rm -rf autom4te.cache config.h.in.orig

#cp %{S:1} config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
"

export CC="%{_rpmint_target}-gcc"
export AR="%{_rpmint_target}-ar"
export ARFLAGS=rcs

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CC="$CC" \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/{bin,include,lib}
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/${multilibdir}
	cp newt.h %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/include
	cp libnewt.a %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib${multilibdir}
	cp whiptail %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	%{_rpmint_target}-strip %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/*
	# make DESTDIR=%{buildroot}%{_rpmint_sysroot} INSTALL="install --strip-program=%{_rpmint_target}-strip" install

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
	rm -rf config.cache
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
%doc CHANGES COPYING
%doc tutorial.sgml
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%endif



%changelog
* Sun Mar 19 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Sat Apr 01 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Sun Dec 26 1999 Guido Flohr <guido@freemint.de>
- Don't use color mode on monochrome terminals.

* Sun Dec 19 1999 Guido Flohr <guido@freemint.de>
- First release for Sparemint.
