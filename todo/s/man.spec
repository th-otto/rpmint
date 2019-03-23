Summary       : A set of documentation tools: man, apropos and whatis.
Name          : man
Version       : 1.5g
Release       : 4
Copyright     : GPL
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Requires      : groff less ncurses

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.win.tue.nl/pub/linux/util/man/man-%{version}.tar.gz
Source1: makewhatis.cronweekly
Source2: makewhatis.crondaily
Source3: man-1.5e-rhpath.patch
Patch0:  man-1.5a-manpath.patch
Patch2:  man-1.5g-buildroot.patch
Patch3:  man-1.5-manconf.patch
Patch4:  man-1.5g-make.patch
Patch5:  man-1.5g-mint.patch


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
%setup -q
%patch0 -p1 -b .manpath
%patch2 -p1 -b .buildroot
%patch3 -p1 
%patch4 -p1 -b .make
%patch5 -p1 -b .mint
rm -f $RPM_BUILD_DIR/man-%{version}/man/en/man.conf.man


%build
./configure -default +fsstnd +sgid
patch -p1 -s < $RPM_SOURCE_DIR/man-1.5e-rhpath.patch || :
make CC="gcc -g $RPM_OPT_FLAGS -D_GNU_SOURCE"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p  ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p  ${RPM_BUILD_ROOT}%{_prefix}/man
mkdir -p  ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p  ${RPM_BUILD_ROOT}/etc/cron.daily
mkdir -p  ${RPM_BUILD_ROOT}/etc/cron.weekly

make install PREFIX=${RPM_BUILD_ROOT}

install -m755 $RPM_SOURCE_DIR/makewhatis.cronweekly ${RPM_BUILD_ROOT}/etc/cron.weekly/makewhatis.cron
install -m755 $RPM_SOURCE_DIR/makewhatis.crondaily ${RPM_BUILD_ROOT}/etc/cron.daily/makewhatis.cron

mkdir -p ${RPM_BUILD_ROOT}/var/catman
mkdir -p ${RPM_BUILD_ROOT}/var/catman/local
mkdir -p ${RPM_BUILD_ROOT}/var/catman/X11
for i in 1 2 3 4 5 6 7 8 9 n; do
	mkdir -p ${RPM_BUILD_ROOT}/var/catman/cat$i
	mkdir -p ${RPM_BUILD_ROOT}/var/catman/local/cat$i
	mkdir -p ${RPM_BUILD_ROOT}/var/catman/X11R6/cat$i
done

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/man
chmod u+w ${RPM_BUILD_ROOT}%{_prefix}/bin/man ||:
stack --fix=40k ${RPM_BUILD_ROOT}%{_prefix}/bin/man ||:

# added man2html stuff
cd man2html
make install PREFIX=${RPM_BUILD_ROOT}

# compress manuals
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/man*/* ||:

# symlinks for manpath
ln -s man ${RPM_BUILD_ROOT}%{_prefix}/bin/manpath
ln -s man.1.gz ${RPM_BUILD_ROOT}%{_prefix}/man/man1/manpath.1.gz


%preun
# Clean up accumulated cat litter.
rm -f /var/catman/cat[123456789n]/*
rm -f /var/catman/local/cat[123456789n]/*
rm -f /var/catman/X11R6/cat[123456789n]/*

%post
rm -f /var/catman/cat[123456789n]/*
rm -f /var/catman/local/cat[123456789n]/*
rm -f /var/catman/X11/cat[123456789n]/*

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%config /etc/cron.weekly/makewhatis.cron
%config /etc/cron.daily/makewhatis.cron
%config /etc/man.config
%attr(2755,root,man) %{_prefix}/bin/man
%{_prefix}/bin/man2html
%{_prefix}/bin/manpath
%{_prefix}/bin/apropos
%{_prefix}/bin/whatis
%{_prefix}/sbin/makewhatis
%{_prefix}/man/man5/man.config.5.gz
%{_prefix}/man/man1/whatis.1.gz
%{_prefix}/man/man1/man.1.gz
%{_prefix}/man/man1/manpath.1.gz
%{_prefix}/man/man1/apropos.1.gz
%{_prefix}/man/man1/man2html.1.gz

%attr(0775,root,man) %dir /var/catman
%attr(0775,root,man) %dir /var/catman/cat[123456789n]
%attr(0775,root,man) %dir /var/catman/local
%attr(0775,root,man) %dir /var/catman/local/cat[123456789n]
%attr(0775,root,man) %dir /var/catman/X11R6
%attr(0775,root,man) %dir /var/catman/X11R6/cat[123456789n]


%changelog
* Thu Nov 08 2001 Frank Naumann <fnaumann@freemint.de>
- recompiled, corrected MAN_PATH to include /usr/share/man
- fixed PATH to cat

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
