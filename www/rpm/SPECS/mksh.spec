%define pkgname mksh

%rpmint_header

%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        57
Release:        1
Summary:        MirBSD Korn Shell
License:        MirOS AND ISC
Group:          System/Shells
Url:            http://www.mirbsd.org/mksh.htm
Source:         https://www.mirbsd.org/MirOS/dist/mir/mksh/%{pkgname}-R%{version}.tar.xz
Patch0:         mksh-vendor-mkshrc.patch
Patch1:         mksh-Allow-files-without-the-executable-bit.patch
BuildRequires:  sed
BuildRequires:  update-alternatives
Provides:       pdksh = %{version}
Obsoletes:      pdksh < %{version}
Provides:       ksh = %{version}
Obsoletes:      ksh < %{version}
Provides:       /bin/ksh
Requires(post): update-alternatives
Requires(preun): update-alternatives
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%rpmint_build_arch

%description
The MirBSD Korn Shell is an actively developed free implementation of the Korn
Shell programming language and a successor to the Public Domain Korn Shell
(pdksh).

%prep
%setup -q -n %{pkgname}-R%{version}
%patch0 -p1
%patch1 -p1

%build

%rpmint_cflags

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--disable-shared
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

#
# sys_errlist and sys_siglist *are* deprecated
# Be aware of the _SYS_SIGLIST and _SYS_ERRLIST macros as well
#
HAVE_SYS_SIGLIST=0
HAVE_SYS_ERRLIST=0
HAVE__SYS_SIGLIST=0
HAVE__SYS_ERRLIST=0
export HAVE_SYS_SIGLIST HAVE_SYS_ERRLIST HAVE__SYS_SIGLIST HAVE__SYS_ERRLIST

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

	export TARGET_OS=FreeMiNT
	export CC=%{_rpmint_target}-gcc
	export CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS"
	export LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS -s ${STACKSIZE}"
	export CPPFLAGS='-DMKSH_VENDOR_MKSHRC_PATH=\"/etc/mkshrc\" -DMKSH_SMALL'
	CPPFLAGS="$CPPFLAGS -DKSH_VERSIONNAME_VENDOR_EXT=\\\"\ +%{vendor}\\\""

	sh ./Build.sh -r
	# build lksh to automatically enable -o posix if called as sh
	CPPFLAGS="$CPPFLAGS -DMKSH_BINSHPOSIX"
	sh ./Build.sh -L -r

	for shell in mksh lksh; do
	    install -D -p -m 755 ${shell} %{buildroot}%{_rpmint_sysroot}/bin/${shell}
	    install -D -p -m 644 ${shell}.1 %{buildroot}%{_rpmint_mandir}/man1/${shell}.1
	    mkdir -p %{buildroot}%{_rpmint_bindir}
	    ln -sf ../../bin/${shell} %{buildroot}%{_rpmint_bindir}
	done
	# compatibility symlinks for pdksh, lksh replaces pdksh
	ln -s lksh %{buildroot}%{_rpmint_sysroot}/bin/pdksh
	ln -s lksh %{buildroot}%{_rpmint_bindir}/pdksh
	ln -s lksh.1%{ext_man} %{buildroot}%{_rpmint_mandir}/man1/pdksh.1%{ext_man}
	mkdir -p %{buildroot}%{_rpmint_sysconfdir}
	
	install -D -p -m 644 dot.mkshrc %{buildroot}%{_rpmint_docdir}/packages/%{pkgname}/dot.mkshrc

	# compress manpages
	%rpmint_gzip_docs

	%if "%{buildtype}" != "cross"
	mkdir -p %{buildroot}/etc
	ln -sf bash.bashrc %{buildroot}/etc/mkshrc
	%rpmint_make_bin_archive $CPU
	%else
	rm -f %{buildroot}/etc/mkshrc
	rmdir %{buildroot}/etc || :
	%endif
done

%install

# symlinks for update-alternatives
%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
install -d -m 755 %{buildroot}%{_sysconfdir}/alternatives
mkdir -p %{buildroot}/etc/alternatives
touch %{buildroot}/etc//alternatives/ksh \
    %{buildroot}/etc/alternatives/usr-bin-ksh \
    %{buildroot}/etc/alternatives/ksh.1%{ext_man}
ln -sf /etc/alternatives/ksh %{buildroot}/bin/ksh
ln -sf /etc/alternatives/usr-bin-ksh %{buildroot}/%{_bindir}/ksh
ln -sf /etc/alternatives/ksh.1%{ext_man} %{buildroot}/%{_mandir}/man1/ksh.1%{ext_man}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if "%{buildtype}" != "cross"
%post
%{_sbindir}/update-alternatives \
  --install /bin/ksh ksh %{_bindir}/lksh 15 \
  --slave %{_rpmint_target_prefix}/bin/ksh usr-bin-ksh %{_rpmint_target_prefix}/bin/lksh \
  --slave %{_rpmint_target_prefix}/share/man/man1/ksh.1%{?ext_man} ksh.1%{?ext_man} %{_rpmint_target_prefix}/share/man/man1/lksh.1%{?ext_man}

%preun
if test $1 -eq 0 ; then
    %{_sbindir}/update-alternatives --remove ksh /bin/lksh
fi

%postun
test -x %{_bindir}/mksh && awk '
($1 != "/bin/mksh") && ($1 != "%{_bindir}/mksh") {
    line[n++] = $0
}
END {
    for (i = 0; i < n; i++) {
        print line[i] >"%{_sysconfdir}/shells"
    }
}' '%{_sysconfdir}/shells' || true
%endif

%files
%defattr(-,root,root)
%if "%{buildtype}" == "cross"
%{_rpmint_sysroot}/bin
%{_rpmint_bindir}
%{_rpmint_datadir}
%else
/etc/mkshrc
/bin
%{_rpmint_target_prefix}/bin
%{_rpmint_target_prefix}/share
%ghost /etc/alternatives/ksh
%ghost /etc/alternatives/usr-bin-ksh
%ghost /etc/alternatives/ksh.1%{?ext_man}
%endif

%changelog
* Sun Mar 5 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
