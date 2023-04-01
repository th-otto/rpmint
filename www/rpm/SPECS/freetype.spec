%define pkgname freetype

%if "%{?buildtype}" == ""
%define buildtype cross
%endif

%rpmint_header

Summary       : A free and portable TrueType font rendering engine
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 1.4
Release       : 2
License       : GPL-2.0-or-later
Group         : System Environment/Libraries

%if "%{buildtype}" == "cross"
Provides      : cross-mint-freetype-devel = %{version}
%else
Provides      : freetype-devel = %{version}
%endif

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : http://www.freetype.org/

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: freetype-%{version}.tar.gz
Source1: freetype-ttmkfdir2.tar.gz
Source2: patches/automake/mintelf-config.sub
Patch3:  patches/{%pkgname}/freetype-ttmkfdir-libtool.patch
Patch4:  patches/{%pkgname}/freetype-ttmkfdir-foundrynames.patch
Patch5:  patches/{%pkgname}/freetype-ttmkfdir.patch
Patch6:  patches/{%pkgname}/freetype-config.patch

%rpmint_build_arch


%description
The FreeType engine is a free and portable TrueType font rendering
engine. It has been developed to provide TrueType support to a great
variety of platforms and environments.

Note that FreeType is a *library*. It is not a font server for your
favorite platform, even though it was designed to be used in many of
them. Note also that it is *not* a complete text-rendering library.
Its purpose is simply to open and manage font files, as well as load,
hint and render individual glyphs efficiently. You can also see it as
a "TrueType driver" for a higher-level library, though rendering text
with it is extremely easy, as demo-ed by the test programs.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -b 1 -a 1 -n %{pkgname}-%{version}
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

rm -f config.cache ltconfig ltmain.sh
libtoolize -i
rm -f config.sub
cp %{S:2} config.sub

aclocal
autoconf

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-debug \
	--disable-shared
	--enable-static \
	--disable-nls \
"

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir || exit 1

	make
	make install prefix=%{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}

	# binaries are obsoleted by freetype2
	rm -f %{buildroot}%{_rpmint_bindir}/* ||:

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" == "$CPU"; then
		make -C ttmkfdir2 CC=%{_rpmint_target}-gcc CXX=%{_rpmint_target}-g++ DEBUG="$COMMON_CFLAGS ${CPU_CFLAGS}"
		install -m 755 ttmkfdir2/ttmkfdir %{buildroot}%{_rpmint_bindir}
		make -C ttmkfdir2 clean
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
%if "%{buildtype}" != "cross"
%{_isysroot}%{_rpmint_target_prefix}/bin
%endif
%{_isysroot}%{_rpmint_target_prefix}/include/freetype
%{_isysroot}%{_rpmint_target_prefix}/lib


%changelog
* Thu Mar 23 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Only build libttf, for xpdf

* Tue Jul 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0.4, dropped old 1.x libs

* Fri Mar 16 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0 and 1.4

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- correct Packager and Vendor
- added Summary(de)
