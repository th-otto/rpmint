%define pkgname groff

%rpmint_header

Summary:        GNU troff Document Formatting System
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%define gxditview cross-mint-gxditview
%define perl cross-mint-%{pkgname}-perl
%else
Name:           %{pkgname}
%define gxditview gxditview
%define perl %{pkgname}-perl
%endif
Version:        1.22.4
Release:        4
License:        GPL-3.0-or-later
Group:          Applications/Publishing

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            http://www.gnu.org/software/groff/groff.html

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
%define _licensedir %{_isysroot}%{_rpmint_target_prefix}/share/licenses
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        ftp://ftp.gnu.org/gnu/groff/%{pkgname}-%{version}.tar.gz
Source1:        patches/automake/mintelf-config.sub
Source2:        groff-troff-to-ps.fpi
Source3:        patches/groff/groff-zzz-groff.csh
Source4:        patches/groff/groff-zzz-groff.sh
Patch0:         patches/groff/groff-1.20.1-destbufferoverflow.patch
Patch1:         patches/groff/groff-1.20.1-nroff-empty-LANGUAGE.patch
Patch2:         patches/groff/groff-1.20.1-deunicode.patch
Patch3:         patches/groff/groff-1.21-CVE-2009-5044.patch
Patch4:         patches/groff/groff-1.21-CVE-2009-5081.patch
Patch5:         patches/groff/groff-0001-locale-support-in-papersize-definition.patch
Patch6:         patches/groff/groff-0002-documentation-for-the-locale-keyword.patch
Patch7:         patches/groff/groff-0004-don-t-use-usr-bin-env-in-shebang.patch
Patch8:         patches/groff/groff-force-locale-usage.patch
Patch9:         patches/groff/groff-gnulib.patch
Patch10:        patches/groff/groff-xditview.patch
# Patches from debian
Patch11:        patches/groff/groff-bash-scripts.patch
Patch12:        patches/groff/groff-1.23-forward-compatibility.patch
Patch13:        patches/groff/groff-sort-perl-hash-keys.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-gcc-c++
%else
BuildRequires:  gcc-c++
%endif

%rpmint_build_arch

%description
Groff is a document formatting system.  Groff takes standard text and
formatting commands as input and produces formatted output.  The
created documents can be shown on a display or printed on a printer. 
Groff's formatting commands allow you to specify font type and size, bold
type, italic type, the number and size of columns on a page, and more.

You should install groff if you want to use it as a document formatting
system.  Groff can also be used to format man pages. If you are going
to use groff with the X Window System, you'll also need to install the
groff-gxditview package.

%package -n %{perl}
Summary: Parts of the groff formatting system that require Perl.
Group: Applications/Publishing

%description -n %{perl}
groff-perl contains the parts of the groff text processor
package that require Perl. These include the afmtodit
font processor used to create PostScript font files, the
grog utility that can be used to automatically determine
groff command-line options, and the troff-to-ps print filter.

%package -n %{gxditview}
Summary:        Ditroff Output Displayer for Groff
Group:          Productivity/Publishing/Troff
%if "%{buildtype}" == "cross"
BuildRequires:  cross-mint-XFree86-devel
%else
BuildRequires:  XFree86-devel
%endif
Requires:       %{name} = %{version}
Provides:       gxdview = %{version}-%{release}

%description -n %{gxditview}
This version of xditview is called gxditview and has some extensions
used by the groff command.  gxditview is used by groff if called with
the -X option.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

# remove hardcoded docdir
sed -i \
    -e '/^docdir=/d' \
    Makefile.am

autoreconf -fiv

cp "%{S:1}" config.sub


%build
%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -fno-strict-aliasing"

# libdir redefined as it is just bunch of scripts
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--libdir=%{_rpmint_target_prefix}/libexec
	--with-appresdir=%{_rpmint_target_prefix}/share/X11/app-defaults
	--with-grofferdir=%{_rpmint_target_prefix}/libexec/groff/groffer
	--disable-nls
"
STACKSIZE="-Wl,-stack,160k"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_func_strnlen_working=yes
EOF
	%rpmint_append_gnulib_cache
}

srcdir=`pwd`
export GROFF_COMMAND_PREFIX=
export GROFF_TMAC_PATH=$srcdir/tmac:$srcdir/src/roff/troff
	
#
# we need an executable for the host
#
HOST_BUILD_DIR="$srcdir/build-host"
mkdir -p "$HOST_BUILD_DIR"
cd "${HOST_BUILD_DIR}"
CFLAGS="-O2" $srcdir/configure
make %{?_smp_mflags}

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
	cd "$srcdir"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	CXXFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS}

	make %{?_smp_mflags} \
		GROFF_BIN_DIR="${HOST_BUILD_DIR}" \
		GROFF_BIN_PATH="${HOST_BUILD_DIR}" \
		GROFFBIN="${HOST_BUILD_DIR}/groff"

	make DESTDIR=%{buildroot}%{_rpmint_sysroot} \
		GROFF_BIN_DIR="${HOST_BUILD_DIR}" \
		GROFF_BIN_PATH="${HOST_BUILD_DIR}" \
		GROFFBIN="${HOST_BUILD_DIR}/groff" \
		install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/libexec/charset.alias

	%{_rpmint_target}-stack --fix=384k %{buildroot}%{_rpmint_bindir}/grops

	# compat symlinks
	ln -sf tbl		%{buildroot}%{_rpmint_bindir}/gtbl
	ln -sf eqn		%{buildroot}%{_rpmint_bindir}/geqn

	mkdir -p %{buildroot}%{_rpmint_libdir}/rhs/rhs-printfilters
	install -m 755 %{S:2} %{buildroot}%{_rpmint_libdir}/rhs/rhs-printfilters/troff-to-ps.fpi

	mkdir -p %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin
	mv %{buildroot}%{_rpmint_bindir}/{gxditview,xtotroff} %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin

	# install profiles to disable the use of ANSI colour sequences by default:
	install -d -m 755 %{buildroot}%{_isysroot}/etc/profile.d/
	install -m 644 %{S:3} %{buildroot}%{_isysroot}/etc/profile.d/zzz-groff.csh
	install -m 644 %{S:4} %{buildroot}%{_isysroot}/etc/profile.d/zzz-groff.sh
	
	# fix a symlink
	ln -s -f ../examples/mom/mom-pdf.pdf %{buildroot}%{_rpmint_docdir}/packages/%{pkgname}/pdf/mom-pdf.pdf

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
		rm -f %{buildroot}%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/*
	fi
	%rpmint_make_bin_archive $CPU
	%else
	%{_rpmint_target_strip} %{buildroot}%{_rpmint_bindir}/* || :
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

%files
%defattr(-,root,root)
%license COPYING FDL LICENSES
%doc BUG-REPORT ChangeLog* MANIFEST MORE.STUFF NEWS PROBLEMS PROJECTS README
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%exclude %{_isysroot}%{_rpmint_target_prefix}/bin/grog
%exclude %{_isysroot}%{_rpmint_target_prefix}/bin/afmtodit
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/%{pkgname}
%{_isysroot}%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
%exclude %{_isysroot}%{_rpmint_target_prefix}/share/man/man1/afmtodit.*
%exclude %{_isysroot}%{_rpmint_target_prefix}/share/man/man1/grog.*
%exclude %{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gxditview.*
%exclude %{_isysroot}%{_rpmint_target_prefix}/share/man/man1/xtotroff.*
%{_isysroot}%{_rpmint_target_prefix}/libexec/groff
%config %{_isysroot}/etc/profile.d/zzz-%{pkgname}.*sh

%files -n %{perl}
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/bin/grog
%{_isysroot}%{_rpmint_target_prefix}/bin/afmtodit
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/afmtodit.*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/grog.*
%{_isysroot}%{_rpmint_target_prefix}/lib/rhs/*/*

%files -n %{gxditview}
%defattr(-,root,root)
#%%doc src/devices/xditview/ChangeLog
#%%doc src/devices/xditview/README
#%%doc src/devices/xditview/TODO
%{_isysroot}%{_rpmint_target_prefix}/X11R6/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/gxditview.*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/xtotroff.*
%{_isysroot}%{_rpmint_target_prefix}/share/X11/app-defaults/*


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%changelog
* Sat Apr 01 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 1.22.4
- add X11 tools

* Wed May 10 2000 Frank Naumann <fnaumann@freemint.de>
- recompiled against new MiNTLib
- increased stack sizes

* Mon Jan 31 2000 Frank Naumann <fnaumann@freemint.de>
- first SpareMiNT release
