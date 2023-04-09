%define pkgname man

%rpmint_header

Summary       : A set of documentation tools: man, apropos and whatis
Name          : %{crossmint}%{pkgname}
Version       : 1.5g
Release       : 4
License       : GPL-2.0-or-later
Group         : System/Base

Packager      : %{packager}
URL:            https://savannah.nongnu.org/projects/man-db

BuildRequires:  groff
Requires      : groff
Requires      : less
Requires      : ncurses

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
Buildroot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.win.tue.nl/pub/linux/util/man/man-%{version}.tar.gz
Source1: man-makewhatis.cronweekly
Source2: man-makewhatis.crondaily

Patch0:  man-1.5a-manpath.patch
Patch2:  man-1.5g-buildroot.patch
Patch3:  man-1.5-manconf.patch
Patch4:  man-1.5g-make.patch
Patch5:  man-1.5g-mint.patch

%rpmint_build_arch


%description
The man package includes three tools for finding information and/or
documentation about your Linux system:  man, apropos and whatis.  The man
system formats and displays on-line manual pages about commands or
functions on your system.  Apropos searches the whatis database
(containing short descriptions of system commands) for a string.  Whatis
searches its own database for a complete word.

The man package should be installed on your system because it is the
primary way for finding documentation.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1 
%patch4 -p1
%patch5 -p1
rm -f man/en/man.conf.man


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS="-O2 -fomit-frame-pointer -D_GNU_SOURCE -DNONLS"

CONFIGURE_FLAGS="-default +fsstnd +sgid"

./configure ${CONFIGURE_FLAGS}
sed -i 's/-Tlatin1/-Tascii/' conf_script
sed -i 's@usr/lib@etc@' conf_script
sed -i 's@/man\.conf@/man.config@' conf_script

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
	cd "$MINT_BUILD_DIR"

	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	make CC="${TARGET}-gcc $CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" || exit 1

	mkdir -p  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin
	mkdir -p  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man
	mkdir -p  %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/sbin
	mkdir -p  %{buildroot}%{_rpmint_sysroot}/etc/cron.daily
	mkdir -p  %{buildroot}%{_rpmint_sysroot}/etc/cron.weekly
	
	make install PREFIX=%{buildroot}%{_rpmint_sysroot}
	
	install -m 755 %{S:1} %{buildroot}%{_rpmint_sysroot}/etc/cron.weekly/makewhatis.cron
	install -m 755 %{S:2} %{buildroot}%{_rpmint_sysroot}/etc/cron.daily/makewhatis.cron
	
	mkdir -p %{buildroot}%{_rpmint_sysroot}/var/catman
	mkdir -p %{buildroot}%{_rpmint_sysroot}/var/catman/local
	mkdir -p %{buildroot}%{_rpmint_sysroot}/var/catman/X11
	for i in 1 2 3 4 5 6 7 8 9 n; do
		mkdir -p %{buildroot}%{_rpmint_sysroot}/var/catman/cat$i
		mkdir -p %{buildroot}%{_rpmint_sysroot}/var/catman/local/cat$i
		mkdir -p %{buildroot}%{_rpmint_sysroot}/var/catman/X11R6/cat$i
	done
	
	# added man2html stuff
	cd man2html
	make install PREFIX=%{buildroot}%{_rpmint_sysroot}
	cd ..
	
	# symlinks for manpath
	ln -sf man %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/bin/manpath
	ln -sf man.1.gz %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/share/man/man1/manpath.1.gz

	make clean >/dev/null

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif
done



%install
%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif


%preun
# Clean up accumulated cat litter.
rm -f %{_isysroot}/var/catman/cat[123456789n]/*
rm -f %{_isysroot}/var/catman/local/cat[123456789n]/*
rm -f %{_isysroot}/var/catman/X11R6/cat[123456789n]/*

%post
rm -f %{_isysroot}/var/catman/cat[123456789n]/*
rm -f %{_isysroot}/var/catman/local/cat[123456789n]/*
rm -f %{_isysroot}/var/catman/X11/cat[123456789n]/*

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%license COPYING
%doc LSM README* TODO
%config %{_isysroot}/etc/cron.weekly/makewhatis.cron
%config %{_isysroot}/etc/cron.daily/makewhatis.cron
%config %{_isysroot}/etc/man.config
%attr(2755,root,man) %{_isysroot}%{_rpmint_target_prefix}/bin/man
%{_isysroot}%{_rpmint_target_prefix}/bin/man2html
%{_isysroot}%{_rpmint_target_prefix}/bin/manpath
%{_isysroot}%{_rpmint_target_prefix}/bin/apropos
%{_isysroot}%{_rpmint_target_prefix}/bin/whatis
%{_isysroot}%{_rpmint_target_prefix}/sbin/makewhatis
%{_isysroot}%{_rpmint_target_prefix}/share/man/man5/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man1/*
%{_isysroot}%{_rpmint_target_prefix}/share/man/man8/*

%attr(0775,root,man) %dir %{_isysroot}/var/catman
%attr(0775,root,man) %dir %{_isysroot}/var/catman/cat[123456789n]
%attr(0775,root,man) %dir %{_isysroot}/var/catman/local
%attr(0775,root,man) %dir %{_isysroot}/var/catman/local/cat[123456789n]
%attr(0775,root,man) %dir %{_isysroot}/var/catman/X11R6
%attr(0775,root,man) %dir %{_isysroot}/var/catman/X11R6/cat[123456789n]


%changelog
* Sun Apr 09 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Thu Nov 08 2001 Frank Naumann <fnaumann@freemint.de>
- recompiled, corrected MAN_PATH to include /usr/share/man
- fixed PATH to cat

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
