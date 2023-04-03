%define pkgname minicom

%rpmint_header

Summary: A text-based modem control and terminal emulation program.
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version: 2.00.0
Release: 1

Packager: Thorsten Otto <admin@tho-otto.de>

License: GPL-2.0-or-later
Group: Applications/Communications
Source0: https://www.ibiblio.org/pub/linux/apps/serialcomm/dialout/%{pkgname}-%{version}.src.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0: minicom-2.00.0-mint.patch
Patch1: minicom-2.00.0-gettext.patch

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
Buildroot: /var/tmp/%{name}-root

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
BuildRequires:  gettext-tools

%rpmint_build_arch

%description
Minicom is a simple text-based modem control and terminal emulation
program somewhat similar to MSDOS Telix.  Minicom includes a dialing
directory, full ANSI and VT100 emulation, an (external) scripting
language, and other features.

Minicom should be installed if you need a simple modem control program
or terminal emulator.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

%patch0 -p1
%patch1 -p1

rm -f aclocal.m4
rm -rf aux
mkdir build-aux
cp /usr/share/gettext/config.rpath build-aux

aclocal
autoconf
autoheader
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--enable-dfl-port=/dev/ttyS1
	--enable-dfl_baud=57600
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
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
%doc doc
#%%config %%{_isysroot}/etc/minicom.users
%attr(2755,root,uucp) %{_isysroot}%{_rpmint_target_prefix}/bin/minicom
%{_isysroot}%{_rpmint_target_prefix}/bin/xminicom
%{_isysroot}%{_rpmint_target_prefix}/bin/runscript
%{_isysroot}%{_rpmint_target_prefix}/bin/ascii-xfr
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/locale/*/*/*

%changelog
* Wed Mar 29 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 2.00.0

* Sat Mar 2 2002 Jan Krupka <jkrupka@volny.cz>
- first release for Sparemint
