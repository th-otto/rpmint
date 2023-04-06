%define pkgname coreutils

%rpmint_header

Summary:        GNU Core Utilities
Name:           %{crossmint}%{pkgname}
Version:        8.32
Release:        1
License:        GPL-3.0-or-later
Group:          System/Base

Packager:       %{packager}
URL:            http://www.gnu.org/software/coreutils/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.xz
Source1: patches/automake/mintelf-config.sub
Source2: patches/%{pkgname}/%{pkgname}-DIR_COLORS

Patch0:  patches/coreutils/coreutils-i18n.patch
Patch1:  patches/coreutils/coreutils-sysinfo.patch
Patch2:  patches/coreutils/coreutils-invalid-ids.patch
Patch3:  patches/coreutils/coreutils-getaddrinfo.patch
Patch4:  patches/coreutils/coreutils-misc.patch
Patch5:  patches/coreutils/coreutils-skip-some-sort-tests-on-ppc.patch
Patch6:  patches/coreutils/coreutils-skip-gnulib-test-tls.patch
Patch7:  patches/coreutils/coreutils-tests-shorten-extreme-factor-tests.patch
Patch8:  patches/coreutils/coreutils-disable_tests.patch
Patch9:  patches/coreutils/coreutils-test_without_valgrind.patch
Patch10: patches/coreutils/coreutils-ls-restore-8.31-behavior-on-removed-dirs.patch
Patch11: patches/coreutils/coreutils-gnulib-disable-test-float.patch
Patch12: patches/coreutils/sh-utils-2.0-getgid.patch
Patch13: patches/coreutils/sh-utils-2.0-mint.patch
Patch14: patches/coreutils/coreutils-mint-physmem.patch
Patch15: patches/coreutils/coreutils-dummy-man-patch
Patch16: patches/coreutils/coreutils-mint-mountlist.patch
Patch17: patches/coreutils/coreutils-mint-procfile.patch
Patch18: patches/coreutils/coreutils-mint-thread.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
%if "%{buildtype}" != "cross"
Obsoletes:      sh-utils < 3.0
Obsoletes:      textutils < 3.0
Obsoletes:      fileutils < 5.0
Obsoletes:      mktemp < 2.0
%endif
Provides:       %{crossmint}mktemp = %{version}

%rpmint_build_arch

%description
These are the GNU core utilities.  This package is the union of
the GNU fileutils, sh-utils, and textutils packages.

  [ arch b2sum base32 base64 basename cat chcon chgrp chmod chown chroot cksum
  comm cp csplit cut date dd df dir dircolors dirname du echo env expand expr
  factor false fmt fold groups head hostid id install join
  link ln logname ls md5sum mkdir mkfifo mknod mktemp mv nice nl nohup
  nproc numfmt od paste pathchk pinky pr printenv printf ptx pwd readlink
  realpath rm rmdir runcon seq sha1sum sha224sum sha256sum sha384sum sha512sum
  shred shuf sleep sort split stat stdbuf stty sum sync tac tail tee test
  timeout touch tr true truncate tsort tty uname unexpand uniq unlink
  uptime users vdir wc who whoami yes ]

This package does not provide man pages, since those are generated automatically
by running the tools and parsing the --help message, which does not work when
cross-compiling. However that also means that those man pages do not
provide any useful information beyond what is available by just running
<tool> --help.

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
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

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
	--enable-install-program=arch,kill
	--localstatedir=/var/run
	DEFAULT_POSIX2_VERSION=200112
	alternative=199209
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
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/find'$multilibexecdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	mkdir -p %{buildroot}%{_rpmint_sysroot}/bin
	cd %{buildroot}%{_rpmint_sysroot}/bin
	for i in arch kill basename cat chgrp chmod chown cp date dd df echo \
	  false ln ls mkdir mknod mktemp mv pwd rm rmdir sleep sort stat \
	  stty sync touch true uname readlink md5sum
	do
	  rm -f $i
	  $LN_S ../%{_rpmint_target_prefix}/bin/$i $i
	done

	# don't supply chroot under MiNT
	cd ../%{_rpmint_target_prefix}/bin
	rm -f chroot

	# rename hostname so it don't conflict with the hostname rpm
	test ! -x hostname || mv hostname hostname.gnu
	
	# don't ship su; it's in shadow-utils
	rm -f su

	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/profile.d
	install -m 644 %{S:2} %{buildroot}%{_rpmint_sysroot}/etc/DIR_COLORS

	# remove man-pages; they are generated by running the tools
	rm -rf %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man

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
%license COPYING
%doc ABOUT-NLS AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%config %{_isysroot}/etc/DIR_COLORS
%{_isysroot}/etc/profile.d
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Wed Apr 05 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 8.32
- replaces sh-utils, textutils and fileutils

* Fri Jun 27 2003 Frank Naumann <fnaumann@freemint.de>
- special physmem detection for FreeMiNT/TOS; don't
  default to 64 MB memory

* Fri Sep 28 2001 Frank Naumann <fnaumann@freemint.de>
- added missing df tool
- compiled against MiNTLib 0.57.1

* Wed Sep 19 2001 Frank Naumann <fnaumann@freemint.de>
- recompiled against bugfixed MiNTLib without PATHMAX problems

* Mon Sep 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0.11

* Thu Sep 13 2001 Frank Naumann <fnaumann@freemint.de>
- updated to textutils 4.1

* Mon Nov 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against bugfixed MiNTLib 0.55 that solve wrong
  error code emulation (rm problems)

* Sun Jul 16 2000 Marc-Anton Kehr <m.kehr@ndh.net>
- rebuild against MiNTLib 0.55, this fixes some problems

* Mon Apr 10 2000 Guido Flohr <guido@freemint.de>
- upgrade to 2.0
- install sort and cat in /bin, not in/usr/bin
- built against MiNTLib 0.55.2
- work around a bug in MiNTLib 0.55.2 that defines unix to an empty string
- added credits

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor

* Thu Aug 12 1999 Guido Flohr <guido@freemint.de>
- changed vendor to Sparemint

* Sun Jul 18 1999 Guido Flohr <guido@freemint.de>
- built against MiNTLib 0.52.3a
- increased stack size for sort from 10k to 64k, for wc from default
  to 64k
