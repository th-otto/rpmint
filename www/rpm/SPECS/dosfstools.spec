%define pkgname dosfstools

%rpmint_header

Summary:        Utilities for Making and Checking FAT File Systems
Name:           %{crossmint}%{pkgname}
Version:        4.1+git
Release:        1
License:        GPL-3.0-or-later
Group:          System/Filesystems

Packager:       %{packager}
URL:            https://github.com/dosfstools/dosfstools
VCS:            https://github.com/th-otto/dosfstools

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: %{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub

# archive above is from git repo and already has all
# mint specific patches applied

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make

%rpmint_build_arch

%description
The dosfstools package includes the mkdosfs and dosfsck utilities, which
respectively make and check MS-DOS FAT file systems on hard drives or on
floppies.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}

aclocal
autoconf
automake --force --copy --add-missing
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--docdir=%{_rpmint_target_prefix}/share/doc/packages/%{pkgname}
	--sbindir=/sbin
	--enable-compat-symlinks
	--enable-atari-check
	--without-udev
"
STACKSIZE="-Wl,-stack,128k"

export LIBICONV=-liconv

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
%doc ChangeLog NEWS README doc/*
%{_isysroot}/sbin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*


%changelog
* Thu Apr 06 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.1

* Tue Sep 30 2003 Frank Naumann <fnaumann@freemint.de>
- updated to 2.10
- much better memory management (around 33% reduced memory consumption)

* Thu Feb 15 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
