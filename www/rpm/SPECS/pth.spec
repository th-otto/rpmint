%define pkgname pth

%rpmint_header

Summary:        GNU Pth threads library
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version:        2.0.7
Release:        1
License:        LGPL-2.1-or-later
Group:          Development/Libraries/C and C++

Packager:       Thorsten Otto <admin@tho-otto.de>
URL:            https://www.gnu.org/software/pth/

Prefix:         %{_prefix}
Docdir:         %{_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0: https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Patch0:  patches/%{pkgname}/pth-2.0.7-m68k-atari-mint.patch
Patch1:  patches/%{pkgname}/pth-link-warning.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  make
%if "%{buildtype}" == "cross"
Provides:       cross-mint-pthread-devel
%else
Provides:       pthread-devel
%endif

%rpmint_build_arch

%description
based library for Unix platforms which provides non-preemptive
priority-based scheduling for multiple threads of execution (aka
``multithreading'') inside event-driven applications. All threads run
in the same address space of the server application, but each thread
has it&apos;s own individual program-counter, run-time stack, signal mask
and errno variable.

The thread scheduling itself is done in a cooperative way, i.e., the
threads are managed by a priority- and event-based non-preemptive
scheduler. The intention is that this way one can achieve better
portability and run-time performance than with preemptive scheduling.
The event facility allows threads to wait until various types of events
occur, including pending I/O on filedescriptors, asynchronous signals,
elapsed timers, pending I/O on message ports, thread and process
termination, and even customized callback functions. 

Original MiNT-Patch by Patrice Mandin & medmed.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

autoconf
rm -rf autom4te.cache

cp %{S:1} config.sub

%build

%rpmint_cflags

COMMON_CFLAGS="-O2 -fomit-frame-pointer ${CFLAGS_AMIGAOS}"
CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
    --enable-pthread
    --config-cache
"

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_check_stackgrowth=down
ac_cv_check_sjlj=sjljmint
ac_cv_check_mcsc=no
ac_cv_func_sigstack=no
ac_cv_func_sigaltstack=no
ac_cv_func_makecontext=no
EOF
}

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	create_config_cache

	CC="%{_rpmint_target}-gcc" \
	AR="${ar}" \
	RANLIB=${ranlib} \
	NM=%{_rpmint_target}-nm \
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	rm -f %{buildroot}%{_rpmint_mandir}/man1/pth-config*
	rm -f %{buildroot}%{_rpmint_mandir}/man1/pthread-config*
	rmdir %{buildroot}%{_rpmint_mandir}/man1 || :

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias
	rm -f %{buildroot}%{_rpmint_bindir}/pthread-config
	rm -f %{buildroot}%{_rpmint_bindir}/pth-config
	rmdir %{buildroot}%{_rpmint_bindir} || :

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
%{_isysroot}%{_rpmint_target_prefix}/include
%{_isysroot}%{_rpmint_target_prefix}/lib
%{_isysroot}%{_rpmint_target_prefix}/share



%changelog
* Sun Apr 02 2023 Thorsten Otto <admin@tho-otto.de>
- Add link warnings

* Tue Mar 07 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
