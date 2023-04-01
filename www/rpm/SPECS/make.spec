%define pkgname make

%if "%{?buildtype}" == ""
%define buildtype cross
%endif
%rpmint_header

Summary:        GNU make
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        4.2.1
Release:        2
License:        GPL-2.0-or-later
Group:          Development/Tools/Building

URL:            http://www.gnu.org/software/make/make.html
Packager:       Thorsten Otto <admin@tho-otto.de>

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        http://ftp.gnu.org/gnu/make/make-%{version}.tar.bz2
Source1:        patches/automake/mintelf-config.sub

Patch0:         patches/%{pkgname}/make-testcases_timeout.diff
Patch1:         patches/%{pkgname}/make-clockskew.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
Prereq		: /sbin/install-info

%rpmint_build_arch

%description
A GNU tool for controlling the generation of executables and other
non-source files of a program from the program's source files.  Make
allows users to build and install packages without any significant
knowledge about the details of the build process.  The details about how
the program should be built are provided for make in the program's
makefile.

The GNU make tool should be installed on your system because it is
commonly used to simplify the process of installing programs.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1

rm -f config/config.sub
cp %{S:1} config/config.sub

%build

create_config_cache()
{
cat <<EOF >config.cache
make_cv_sys_gnu_glob=yes
EOF
	%rpmint_append_gnulib_cache
}


%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--disable-shared
	--disable-load
	--disable-nsec-timestamps
	--config-cache
"
STACKSIZE="-Wl,-stack,160k"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -s ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -fv %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	rm -fv %{buildroot}%{_rpmint_includedir}/gnumake.h

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif

	make distclean
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
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
%doc NEWS README AUTHORS
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Sat Apr 01 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.2.1

* Fri Aug 13 2010 Keith Scroggins <kws@radix.net>
- Updated to 3.82

* Mon May 24 2010 Keith Scroggins <kws@radix.net>
- Fixed to be able to compile for 5475 target.

* Sat Jan 30 2010 Keith Scroggins <kws@radix.net>
- Fixed to be able to compile for different CPU targets.

* Sat May 16 2009 Keith Scroggins <kws@radix.net>
- Updated to latest version (3.81) and setup for Cross Compile

* Thu Feb 16 2006 Mark Duckworth <mduckworth@atari-source.com
- compiled against latest mintlib - attempt to fix malloc bug
- updated to latest version

* Sun Jul 04 2004 Martin Tarenskeen <m.tarenskeen@zonnet.nl>
- compiled against latest mintlib

* Thu Jan 29 2004 Mark Duckworth <mduckworth@atari-source.com>
- compiled against latest mintlib
- updated to latest version

* Tue Mar 20 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 3.79.1

* Mon Apr 10 2000 Guido Flohr <guido@freemint.de>
- added credits, bug reports section

* Tue Apr 4 2000 Guido Flohr <guido@freemint.de>
- update to 3.78.1
- install manpages in /usr/share/man
- give up mbaserel package
- fixed typo in German description
- rebuilt against MiNTLib 0.55

* Sun Aug 22 1999 Guido Flohr <guido@freemint.de>
- version compiled with -mbaserel goes into different package smail-mbaserel.

* Sat Jul 31 1999 Guido Flohr <guido@freemint.de>
- updated German translation.
- built against shared-text library (-mbaserel).
- g'zipped manpage.
