%define pkgname bison

%rpmint_header

Summary:        The GNU Parser Generator
Name:           %{crossmint}%{pkgname}
Version:        3.6.4
Release:        1
License:        GPL-3.0-or-later
Group:          Development/Languages/C and C++

Packager:       %{packager}
URL:            http://www.gnu.org/software/bison/bison.html

Prereq         : info

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  flex
BuildRequires:  make
Requires:       %{crossmint}m4

%rpmint_build_arch

%description
Bison is a general-purpose parser generator that converts an annotated
context-free grammar into a deterministic LR or generalized LR (GLR)
parser employing LALR(1) parser tables. As an experimental feature,
Bison can also generate IELR(1) or canonical LR(1) parser tables. Once
you are proficient with Bison, you can use it to develop a wide range
of language parsers, from those used in simple desk calculators to
complex programming languages. 

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

aclocal
autoconf
autoheader
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--config-cache
"
STACKSIZE=-Wl,-stack,128k

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
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	: make -C doc refcard.ps
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install
	
	# install via macro later
	rm -fv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}/COPYING

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

	make -i clean
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


%post
%rpmint_install_info %{pkgname}

%preun
%rpmint_uninstall_info %{pkgname}


%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS NEWS README THANKS TODO
%{_isysroot}%{_rpmint_target_prefix}/bin
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/aclocal/*
%{_isysroot}%{_rpmint_target_prefix}/share/bison/*
%{_isysroot}%{_rpmint_target_prefix}/share/doc/packages/bison/examples
%{_isysroot}%{_rpmint_target_prefix}/share/locale/*/*/*



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 3.6.4

* Mon Aug 02 2004 Frank Naumann <fnaumann@freemint.de>
- fixed g++ bug in skeleton

* Thu Feb 20 2003 Frank Naumann <fnaumann@freemint.de>
- updated to 1.875

* Fri Mar 22 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 1.34

* Mon Sep 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.29

* Thu Dec 14 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against MiNTLib 0.56

* Thu Apr 06 2000 Frank Naumann <fnaumann@freemint.de>
- update to 1.28
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
