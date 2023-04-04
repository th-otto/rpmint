%define pkgname bash

%define baseversion 4.4
%define patchlevel .23

%rpmint_header

Summary:        The GNU Bourne-Again Shell
Name:           %{crossmint}%{pkgname}
Version:        %{baseversion}%{patchlevel}
Release:        1
License:        GPL-3.0-or-later
Group:          System/Shells

URL:            http://www.gnu.org/software/bash/bash.html
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        https://ftp.gnu.org/gnu/%{pkgname}/%{pkgname}-%{baseversion}.tar.gz
Source1:        patches/automake/mintelf-config.sub
Source2:        patches/bash/bash-dot.bashrc
Source3:        patches/bash/bash-dot.profile

Patch0:         patches/bash/bash-4.4-patches/bash44-001
Patch1:         patches/bash/bash-4.4-patches/bash44-002
Patch2:         patches/bash/bash-4.4-patches/bash44-003
Patch3:         patches/bash/bash-4.4-patches/bash44-004
Patch4:         patches/bash/bash-4.4-patches/bash44-005
Patch5:         patches/bash/bash-4.4-patches/bash44-006
Patch6:         patches/bash/bash-4.4-patches/bash44-007
Patch7:         patches/bash/bash-4.4-patches/bash44-008
Patch8:         patches/bash/bash-4.4-patches/bash44-009
Patch9:         patches/bash/bash-4.4-patches/bash44-010
Patch10:        patches/bash/bash-4.4-patches/bash44-011
Patch11:        patches/bash/bash-4.4-patches/bash44-012
Patch12:        patches/bash/bash-4.4-patches/bash44-013
Patch13:        patches/bash/bash-4.4-patches/bash44-014
Patch14:        patches/bash/bash-4.4-patches/bash44-015
Patch15:        patches/bash/bash-4.4-patches/bash44-016
Patch16:        patches/bash/bash-4.4-patches/bash44-017
Patch17:        patches/bash/bash-4.4-patches/bash44-018
Patch18:        patches/bash/bash-4.4-patches/bash44-019
Patch19:        patches/bash/bash-4.4-patches/bash44-020
Patch20:        patches/bash/bash-4.4-patches/bash44-021
Patch21:        patches/bash/bash-4.4-patches/bash44-022
Patch22:        patches/bash/bash-%{baseversion}.dif
Patch23:        patches/bash/bash-2.03-manual.patch
Patch24:        patches/bash/bash-4.0-security.patch
Patch25:        patches/bash/bash-4.3-2.4.4.patch
Patch26:        patches/bash/bash-3.0-evalexp.patch
Patch27:        patches/bash/bash-3.0-warn-locale.patch
Patch28:        patches/bash/bash-4.3-decl.patch
Patch29:        patches/bash/bash-4.3-include-unistd.dif
Patch30:        patches/bash/bash-3.2-printf.patch
Patch31:        patches/bash/bash-4.3-loadables.dif
Patch32:        patches/bash/bash-4.1-completion.dif
Patch33:        patches/bash/bash-4.0-setlocale.dif
Patch34:        patches/bash/bash-4.3-winch.dif
Patch35:        patches/bash/bash-4.1-bash.bashrc.dif
Patch36:        patches/bash/bash-man2html-no-timestamp.patch
Patch37:        patches/bash/bash-4.3-perl522.patch
Patch38:        patches/bash/bash-4.3-extra-import-func.patch
Patch39:        patches/bash/bash-4.4-paths.patch
Patch40:        patches/bash/bash-4.4-profile.patch
Patch41:        patches/bash/bash-4.4-mint.patch
Patch42:        patches/bash/bash-cross-comp.patch

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  %{crossmint}ncurses
BuildRequires:  %{crossmint}libreadline7

%rpmint_build_arch

%description
Bash is an sh-compatible command interpreter that executes commands
read from standard input or from a file.  Bash incorporates useful
features from the Korn and C shells (ksh and csh).  Bash is intended to
be a conformant implementation of the IEEE Posix Shell and Tools
specification (IEEE Working Group 1003.2).

Note: /bin/sh is now a bash compiled
with minimal configuration (ie. no line editing features)

%package doc
Group         : Documentation
Summary       : Documentation for the GNU Bourne Again shell (bash).

%description doc
This is a separate documentation package for the GNU Bourne
Again shell.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{baseversion}
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
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1

autoconf
rm -rf autom4te.cache config.h.in.orig

rm -f support/config.sub
cp %{S:1} support/config.sub


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -DIMPORT_FUNCTIONS_DEF=0"
STACKSIZE="-Wl,-stack,256k"

SYSMALLOC="--without-gnu-malloc --without-bash-malloc"
READLINE="--with-installed-readline"

COMMON_CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--with-curses
	--with-afs
	$SYSMALLOC
	$READLINE
	--enable-separate-helpfiles=%{_rpmint_target_prefix}/share/%{pkgname}/helpfiles
	--disable-strict-posix-default
	--config-cache
"

CONFIGURE_FLAGS="$COMMON_CONFIGURE_FLAGS
	--enable-job-control
	--enable-alias
	--enable-readline
	--enable-history
	--enable-bang-history
	--enable-directory-stack
	--enable-process-substitution
	--enable-prompt-string-decoding
	--enable-select
	--enable-help-builtin
	--enable-array-variables
	--enable-brace-expansion
	--enable-command-timing
	--enable-disabled-builtins
"

MINSH_CONFIGURE_FLAGS="$COMMON_CONFIGURE_FLAGS
	--enable-minimal-config
	--enable-arith-for-command
	--disable-readline
	--without-installed-readline
	--disable-history
	--enable-array-variables
	--enable-brace-expansion
	--enable-casemod-attributes
	--enable-casemod-expansion
	--enable-cond-command
	--enable-cond-regexp
	--enable-directory-stack
	--enable-dparen-arithmetic
	--enable-extended-glob
"

# set to true if /bin/sh should be a minimal shell
minsh=true


create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
ac_cv_func_chown_works=yes
ac_cv_func_strcoll_works=yes
ac_cv_func_working_mktime=yes
bash_cv_func_sigsetjmp=present
bash_cv_getcwd_malloc=yes
bash_cv_job_control_missing=present
bash_cv_sys_named_pipes=present
bash_cv_sys_siglist=yes
bash_cv_under_sys_siglist=yes
bash_cv_unusable_rtsigs=no
bash_cv_wcontinued_broken=yes
bash_cv_wexitstatus_offset=8
gt_cv_int_divbyzero_sigfpe=yes
EOF
	%rpmint_append_gnulib_cache
}


disable_iconv()
{
	# even if we have iconv, we don't want to use it,
	# because mintlib does not support locales, and it
	# just bloats the binary
	sed -i 's/^D\["HAVE_ICONV"\]="[ ]*[01]"$/D\["HAVE_ICONV="\]=" 0"/
s/^S\["LIBICONV"\]="\([^"]*\)"$/S\["LIBICONV"\]=""/
s/^S\["LTLIBICONV"\]="\([^"]*\)"$/S\["LTLIBICONV"\]=""/' config.status
	./config.status
}


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
	
	build_dir=`pwd`

	if $minsh; then
		CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
		LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
		"./configure" ${MINSH_CONFIGURE_FLAGS} \
		--libdir='${exec_prefix}/lib'$multilibdir \
		--libexecdir='${exec_prefix}/libexec/bash'$multilibexecdir
		: hack_lto_cflags
		disable_iconv

		make %{?_smp_mflags} Program=sh sh
		make clean
	fi

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE}" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir \
	--libexecdir='${exec_prefix}/libexec/bash'$multilibexecdir

	sed -i 's/^install:.*/install:/' examples/loadables/Makefile
	disable_iconv

	make %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	# If /bin/sh is not the POSIX compatible shell command itself, it must be a hard or symbolic link to the
	# real shell command.
	mkdir -p %{buildroot}%{_rpmint_sysroot}/bin

	mv %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/bash %{buildroot}%{_rpmint_sysroot}/bin
	
	if $minsh; then
		cd %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
		install ${build_dir}/sh %{buildroot}%{_rpmint_sysroot}/bin/sh
		rm -fv sh
		$LN_S ../../bin/sh sh
	else
		cd %{buildroot}%{_rpmint_sysroot}/bin
		rm -fv sh
		$LN_S bash sh
		cd %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
		rm -fv sh
		$LN_S ../../bin/bash sh
	fi
	cd %{buildroot}%{_rpmint_sysroot}/bin
	rm -fv rbash
	$LN_S bash rbash
	cd %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	rm -fv rbash
	$LN_S ../../bin/bash rbash

	cd "$build_dir"
	make clean >/dev/null

	rm -f %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib$multilibdir/charset.alias	

	mkdir -p %{buildroot}%{_rpmint_sysroot}/etc/skel
	install -m 644 %{S:2}   %{buildroot}%{_rpmint_sysroot}/etc/skel/.bashrc
	install -m 644 %{S:3}   %{buildroot}%{_rpmint_sysroot}/etc/skel/.profile
	touch -t 199605181720.50 %{buildroot}%{_rpmint_sysroot}/etc/skel/.bash_history
	chmod 600 %{buildroot}%{_rpmint_sysroot}/etc/skel/.bash_history
	chmod 755 %{buildroot}%{_rpmint_bindir}/bashbug
    
	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%rpmint_install_info %{pkgname}
%if "%{buildtype}" != "cross"
if [ ! -f /etc/shells ]; then
        echo "/bin/sh" > /etc/shells
        echo "/bin/bash" >> /etc/shells
        echo "/bin/rbash" >> /etc/shells
else
        if ! grep '^/bin/bash$' /etc/shells > /dev/null; then
                echo "/bin/bash" >> /etc/shells
                echo "/bin/rbash" >> /etc/shells
		chmod 644 /etc/shells
        fi
fi
%endif

%preun
%rpmint_uninstall_info %{pkgname}
%if "%{buildtype}" != "cross"
if [ "$1" = 0 ]; then
        grep -v '^/bin/bash' /etc/shells | grep -v '^/bin/rbash' > /etc/shells.new
        mv /etc/shells.new /etc/shells
	chmod 644 /etc/shells
fi
%endif

%files
%defattr(-,root,root)
%license COPYING
%doc ABOUT-NLS AUTHORS CHANGES COMPAT NEWS NOTES POSIX RBASH README Y2K
%doc doc/FAQ doc/INTRO doc/article.ms
%config %{_isysroot}/etc/skel/.bashrc
%config %{_isysroot}/etc/skel/.profile
%config %{_isysroot}/etc/skel/.bash_history
%{_isysroot}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/*
%{_isysroot}%{_rpmint_target_prefix}/share/info/*
%{_isysroot}%{_rpmint_target_prefix}/share/%{pkgname}/*


%files doc
%defattr(-,root,root)
%doc doc/*.ps doc/*.0 doc/*.html doc/article.txt
%doc examples


%changelog
* Tue Apr 04 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 4.4.23

* Mon Jan 26 2004 Mark Duckworth <mduckworth@atari-source.com>
- Originally packaged by Guido Flohr
- Rebuilt against latest mintlib, no other changes whatsoever
- incremented release

* Wed Apr 03 2002 Frank Naumann <fnaumann@freemint.de>
- recompiled against newest MiNTLib from CVS

* Tue Mar 05 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 2.05a

* Thu Sep 27 2001 Frank Naumann <fnaumann@freemint.de>
- removed /etc/bashrc and /etc/profile, belongs to new base
  package

* Mon Sep 17 2001 Frank Naumann <fnaumann@freemint.de>
- fixed new bug in read builtin method

* Thu Sep 13 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.05

* Fri Nov 24 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55

* Sun Aug 22 1999 Guido Flohr <guido@freemint.de> 
- Job control works now.
- Fixed the reason for the ugly termios hack.
- Don't compile with mbaserel, which will go into separate bash-mbaserel.

* Sat Jul 31 1999 Guido Flohr <guido@freemint.de> 
- Updated German translations.
- Built against shared-text library (-mbaserel).
- Included Y2k in docs.
- Gzipped manpages.
