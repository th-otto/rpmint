%define pkgname sed

%rpmint_header

Summary:        A Stream-Oriented Non-Interactive Text Editor
Name:           %{crossmint}%{pkgname}
Version:        4.9
Release:        1
License:        GPL-3.0-or-later
Group:          System/Base

Packager:       %{packager}
URL:            https://www.gnu.org/software/sed/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/sed/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

Patch0: patches/sed/sed-nothreads.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make

%rpmint_build_arch

%description
Sed takes text input, performs one or more operations on it, and
outputs the modified text. Sed is typically used for extracting parts
of a file using pattern matching or  for substituting multiple
occurrences of a string within a file.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

aclocal -I m4 || exit 1
autoconf || exit 1
autoheader || exit 1
automake --force --copy --add-missing || exit 1
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} build-aux/config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--disable-threads
	--without-included-regex
	--config-cache
"
STACKSIZE="-Wl,-stack,256k"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
EOF
	%rpmint_append_gnulib_cache
}

build_dir=`pwd`

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
	cd "$build_dir"

	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# according to FHS 3.0, sed must be in /bin
	mkdir -p %{buildroot}%{_rpmint_sysroot}/bin
	cd %{buildroot}%{_rpmint_sysroot}/bin
	for i in sed
	do
	  rm -f $i
	  $LN_S ..%{_rpmint_target_prefix}/bin/$i $i
	done

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	cd "$build_dir"
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
%license COPYING*
%doc ABOUT-NLS AUTHORS ChangeLog* BUGS NEWS README THANKS
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Mon Apr 10 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.9

* Fri Aug 20 2010 Keith Scroggins <kws@radix.net>
- Built latest version

* Fri Aug 13 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Removed test (never fails but takes a helluva long time)
