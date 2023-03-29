%define pkgname gettext

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        Tools for Native Language Support (NLS)
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        0.19.8.1
Release:        1
License:        GPL-3.0-or-later and LGPL-2.0-or-later
Group:          Development/Tools/Other

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.gnu.org/software/gettext/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/pub/gnu/gettext/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/gettext-gnulib.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  m4
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-gettext-runtime = %{version}
Provides:       cross-mint-gettext-tools = %{version}
Provides:       cross-mint-gettext-devel = %{version}
%else
Provides:       gettext-runtime = %{version}
Provides:       gettext-tools = %{version}
Provides:       gettext-devel = %{version}
%endif

%rpmint_build_arch

%description
This package contains the intl library as well as tools that ease the
creation and maintenance of message catalogs. It allows you to extract
strings from source code. The supplied Emacs mode (po-mode.el) helps
editing these catalogs (called PO files, for portable object) and
adding translations. A special compiler turns these PO files into
binary catalogs.

%prep
%setup -q -n %{pkgname}-%{version}-1
%patch0 -p1

(
 cd m4
 rm -f init.m4 amversion.m4 ar-lib.m4 cond.m4 depend.m4 depout.m4 auxdir.m4 install-sh.m4 lispdir.m4 make.m4 missing.m4 options.m4 prog-cc-c-o.m4 runlog.m4 sanity.m4 silent.m4 strip.m4 substnot.m4 tar.m4
)

./autogen.sh

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer"

WHOLE_LIBINTL=
if test "$LTO_CFLAGS" != ""; then
	WHOLE_LIBINTL=--enable-whole-libintl
fi

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname} \
	--disable-shared
	--disable-threads
	--enable-silent-rules
	--disable-curses
	--enable-relocatable
	--with-included-gettext
	$WHOLE_LIBINTL
	--config-cache
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

create_config_cache()
{
cat <<EOF >config.cache
EOF
	%rpmint_append_gnulib_cache
}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	RANLIB="$ranlib" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

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
%if "%{buildtype}" == "cross"
%{_rpmint_bindir}
%{_rpmint_includedir}
%{_rpmint_libdir}
%{_rpmint_datadir}
%{_rpmint_prefix}/libexec/%{pkgname}
%else
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/include
%{_rpmint_target_prefix}/lib
%{_rpmint_target_prefix}/share
%{_rpmint_target_prefix}/libexec/%{pkgname}
%endif



%changelog
* Tue Mar 7 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
- Update to version 0.19.8.1

* Tue Feb 24 2004 Mark Duckworth <mduckworth@atari-source.com>
- Original packager, guido flohr but because of the changes and upgrades
- bug reports should surely go to me.
- Upgraded to version 0.12.1 compiled against mintlib cvs
- Removed stuff about xgemtext, it doesn't seem to be part of this pkg?

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 11 1999 Guido Flohr <guido@freemint.de>
- Changed vendor to Sparemint.
