# Conditional build (replace "#" with "%" to enable):
#
#define _with_ncurses		 1 # use ncurses
%define _with_included_slang	 1 # use included S-Lang library
#define _with_charset		 1 # enable code for charset conversion
#define _with_samba		 1 # enable SMB/CIFS virtual file system
#define _with_ext2undel		 1 # compile with ext2 undelete code
%define _without_x		 1 # avoid dependency on X11 libraries

# Note that this is NOT a relocatable package
%define ver     4.6.0
%define rpmver   4.6.0
%define  RELEASE 2
%define  rel     %{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}

Summary:   Midnight Commander visual shell
Name:      mc
Version:   %rpmver
Release:   %rel
Vendor:	   Sparemint
Packager:  Adam Klobukowski <atari@gabo.pl>
Distribution: SpareMiNT
Epoch:     1
Copyright: GPL
Group:     Applications/File
Source0:   ftp://ftp.ibiblio.org/pub/Linux/utils/file/managers/mc/mc-%{ver}.tar.gz
URL:       http://www.ibiblio.org/mc/
BuildRoot: /var/tmp/mc-%{PACKAGE_VERSION}-root
Prereq:    /sbin/chkconfig
BuildRequires: glib
%{!?_with_included_slang:%{!?_with_ncurses:BuildRequires: slang-devel}}
%{?_with_ncurses:BuildRequires: ncurses-devel}

Patch: amc.patch

%description
GNU Midnight Commander is a visual file manager.  It's a feature rich
full-screen text mode application that allows you to copy, move and
delete files and whole directory trees, search for files and run
commands in the subshell.  Internal viewer and editor are included.
Mouse is supported under X Window System and on Linux console.  VFS
(Virtual Filesystem) allows you to view archives and files on remote
servers.

%prep
%setup -q -n mc-%{ver}
%patch -p1

%build

CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" ./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
%{?_with_ncurses: --with-screen=ncurses} \
%{?_with_included_slang: --with-screen=mcslang} \
%{?_with_charset: --enable-charset} \
%{?_with_samba: --with-samba} \
%{?_with_ext2undel: --with-ext2undel} \
%{?_without_x: --without-x}

make

%install
echo $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/profile.d
cp -f $RPM_BUILD_ROOT%{_prefix}/share/mc/bin/mc.csh \
	$RPM_BUILD_ROOT/etc/profile.d
cp -f $RPM_BUILD_ROOT%{_prefix}/share/mc/bin/mc.sh \
	$RPM_BUILD_ROOT/etc/profile.d


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

%doc FAQ COPYING NEWS README README.AMC
%{_prefix}/bin/mc
%{_prefix}/bin/mcedit
%{_prefix}/bin/mcview
%{_prefix}/bin/mcmfmt
#{_prefix}/lib/mc/cons.saver
%{_mandir}/man1/*
%{_mandir}/*/man1/*

%config /etc/profile.d/*
%{_prefix}/share/mc/cedit.menu
%{_prefix}/share/mc/edit.indent.rc
%{_prefix}/share/mc/edit.spell.rc
%{_prefix}/share/mc/bin/*
%{_prefix}/share/mc/extfs/*
%{_prefix}/share/mc/mc.ext
%{_prefix}/share/mc/mc.lib
%{_prefix}/share/mc/mc.menu
%{?_with_charset:%config %{_prefix}/share/mc/mc.charsets}

%{_prefix}/share/mc/mc.hint*
%{_prefix}/share/mc/mc.hlp*
%{_prefix}/share/mc/syntax/*
%{_prefix}/share/mc/term/*
%{_prefix}/share/locale/*/LC_MESSAGES/*

%dir %{_prefix}/lib/mc
%dir %{_prefix}/share/mc
%dir %{_prefix}/share/mc/extfs
%dir %{_prefix}/share/mc/syntax
%dir %{_prefix}/share/mc/term

%changelog
* Sun Oct 14 2003 Adam Klobukowski <atari@gabo.pl>
- Added Advenced Midnight Commander patch

* Tue Dec 24 2002 Pavel Roskin <proski@gnu.org>
- Work around bug in rpm 4.1 that expands defines in comments.
- Handle --without-x.

* Mon Nov 04 2002 Andrew V. Samoilov <sav@bcs.zp.ua>
- Handle --with ext2undel.

* Fri Nov 01 2002 Pavel Roskin <proski@gnu.org>
- Add wrappers to support setting last directory on exit.  Keep all
  scripts in their original directory, just copy them.

* Tue Oct 22 2002 Pavel Roskin <proski@gnu.org>
- Don't use the included S-Lang, there is a workaround for Red Hat 8.0
  S-Lang, and binary compatibility with Red Hat 7.x doesn't work anyway.

* Tue Oct 08 2002 Pavel Roskin <proski@gnu.org>
- Use the included S-Lang again, since we include a better version now.
  This should avoid incompatibility with Red Hat 7.x.
- Add _with_glib2 option.

* Mon Oct 07 2002 Pavel Roskin <proski@gnu.org>
- Remove installed mc.sh and mc.csh from %{_prefix}/share/mc/bin to
  suppress a warning about installed but unpackaged files.

* Mon Sep 30 2002 Andrew V. Samoilov <sav@bcs.zp.ua>
- Don't require slang-devel if _with_ncurses.
- Handle --with samba.

* Sun Sep 29 2002 Pavel Roskin <proski@gnu.org>
- Use --with-screen instead of --with-ncurses and --with-included-slang.

* Mon Sep 23 2002 Andrew V. Samoilov <sav@bcs.zp.ua>
- Restore %config for %{_prefix}/share/mc/mc.charsets.
- Restore %{_prefix}/share/mc/edit.spell.rc.

* Sat Sep 21 2002 Pavel Roskin <proski@gnu.org>
- Use FHS-compliant paths.
- Drop %config from files under /usr/share - users are not supposed to
  edit them.  Local copies under ~/.mc should be used for that.

* Wed Aug 21 2002 Pavel Roskin <proski@gnu.org>
- Change description, update URLs, allow dash in the version.

* Tue Aug 20 2002 Pavel Roskin <proski@gnu.org>
- Support conditional builds.

* Tue Aug 20 2002 Andrew V. Samoilov <sav@bcs.zp.ua>
- Add /usr/lib/mc/mc.charsets.
- Add %{_mandir}/*/man1/*.

* Fri Aug 16 2002 Pavel Roskin <proski@gnu.org>
- Remove mc.global.

* Mon Jan 21 2002 Pavel Roskin <proski@gnu.org>
- Remove --with-gnome and --with-included-slang from configure options.
- Add BuildPrereq.

* Fri Aug 24 2001 Pavel Roskin <proski@gnu.org>
- Remove gmc.  Reunite mc and mc-common.

* Sun Aug 05 2001 Pavel Roskin <proski@gnu.org>
- Set epoch.

* Sun Jul 15 2001 Pavel Roskin <proski@gnu.org>
- Remove /usr/lib/mc/layout.

* Sat Jun 09 2001 Pavel Roskin <proski@gnu.org>
- Use %{_prefix} and %{_mandir}. Specify --mandir to configure.

* Fri May 25 2001 Pavel Roskin <proski@gnu.org>
- Change groups. Don't include locale directories. More config files.

* Sun May 20 2001 Pavel Roskin <proski@gnu.org>
- Don't require stylesheets, since HTML files are now in the tarball.

* Thu Apr 19 2001 Pavel Roskin <proski@gnu.org>
- Remove package mcserv. Drop dependency on PAM.

* Mon Feb 26 2001 Pavel Roskin <proski@gnu.org>
- Remove mc-gnome.ext.

* Thu Jan 11 2001 Pavel Roskin <proski@gnu.org>
- Include mcview.

* Mon Oct 23 2000 Pavel Roskin <proski@gnu.org>
- Allow mcserv.8 to be gzipped.

* Sat Sep 30 2000 Pavel Roskin <proski@gnu.org>
- New package mc-common.
- Use DESTDIR instead of misusing prefix.
- Don't install old icons - they don't exist

* Sat Sep 23 2000 Pavel Roskin <proski@gnu.org>
- Include translations with mc, not gmc
- chkconfig --del in %preun, not %postun
- --without-debug not needed
- /etc/X11/wmconfig not needed
- /etc/pam.d/mcserv shouldn't be executable
- New files in %{prefix}/lib/mc/ - translated hints, editor files

* Thu Sep 09 1999 Elliot Lee <sopwith@redhat.com>
- Include .idl files in the package.

* Sat Sep 04 1999 Gregory McLean <gregm@comstar.net>
- Added a build prereq so that rpms get built with documentation ;)

* Mon Jul 12 1999 Kjartan Maraas  <kmaraas@online.no>
- added help and locale files to %files

* Tue Jun 22 1999 Vladimir Kondratiev <vkondra@iil.intel.com>
- added syntax files to %files

* Wed May 26 1999 Cody Russell <bratsche@dfw.net>
- chmod cons.saver at $RPM_BUILD_ROOT%{prefix}/lib rather than at
  $RPM_BUILD_ROOT/usr/lib. We can now install to somewhere other than /usr.

* Sun Apr 18 1999 Gregory McLean <gregm@comstar.net>
- Updated the specfile, removed some kludges.

* Thu Aug 20 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against gnome-libs 0.27 and gtk+-1.1

* Thu Jul 09 1998 Michael Fulbright <msf@redhat.com>
- made cons.saver not setuid

* Sun Apr 19 1998 Marc Ewing <marc@redhat.com>
- removed tkmc

* Wed Apr 8 1998 Marc Ewing <marc@redhat.com>
- add /usr/lib/mc/layout to gmc

* Tue Dec 23 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
- added --without-debug to configure,
- modification in %build and %install and cosmetic modification in packages
  headers,
- added %%{PACKAGE_VERSION} macro to Buildroot,
- removed "rm -rf $RPM_BUILD_ROOT" from %prep.
- removed Packager field.

* Thu Dec 18 1997 Michele Marziani <marziani@fe.infn.it>
- Merged spec file with that from RedHat-5.0 distribution
  (now a Hurricane-based distribution is needed)
- Added patch for RPM script (didn't always work with rpm-2.4.10)
- Corrected patch for mcserv init file (chkconfig init levels)
- Added more documentation files on termcap, terminfo, xterm

* Thu Oct 30 1997 Michael K. Johnson <johnsonm@redhat.com>

- Added dependency on portmap

* Wed Oct 29 1997 Michael K. Johnson <johnsonm@redhat.com>

- fixed spec file.
- Updated to 4.1.8

* Sun Oct 26 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>

- updated to 4.1.6
- added %attr macros in %files,
- a few simplification in %install,
- removed glibc patch,
- fixed installing /etc/X11/wmconfig/tkmc.

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>

- updated to 4.1.5
- added wmconfig

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>

- chkconfig is for mcserv package, not mc one

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>

- patched init script for chkconfig
- don't turn on the service by default

* Fri Oct 10 1997 Michael K. Johnson <johnsonm@redhat.com>

- Converted to new PAM conventions.
- Updated to 4.1.3
- No longer needs glibc patch.

* Thu May 22 1997 Michele Marziani <marziani@fe.infn.it>

- added support for mc alias in /etc/profile.d/mc.csh (for csh and tcsh)
- lowered number of SysV init scripts in /etc/rc.d/rc[0,1,6].d
  (mcserv needs to be killed before inet)
- removed all references to $RPM_SOURCE_DIR
- restored $RPM_OPT_FLAGS when compiling
- minor cleanup of spec file: redundant directives and comments removed

* Sun May 18 1997 Michele Marziani <marziani@fe.infn.it>

- removed all references to non-existent mc.rpmfs
- added mcedit.1 to the %files section
- reverted to un-gzipped man pages (RedHat style)
- removed double install line for mcserv.pamd

* Tue May 13 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>

- added new rpmfs script,
- removed mcfn_install from mc (adding mc() to bash enviroment is in
  /etc/profile.d/mc.sh),
- /etc/profile.d/mc.sh changed to %config,
- removed /usr/lib/mc/bin/create_vcs,
- removed /usr/lib/mc/term.

* Wed May 9 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>

- changed source url,
- fixed link mcedit to mc,

* Tue May 7 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>

- new version 3.5.27,
- %dir /usr/lib/mc/icons and icons removed from tkmc,
- added commented xmc part.

* Tue Apr 22 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>

- FIX spec:
   - added URL field,
   - in mc added missing /usr/lib/mc/mc.ext, /usr/lib/mc/mc.hint,
     /usr/lib/mc/mc.hlp, /usr/lib/mc/mc.lib, /usr/lib/mc/mc.menu.

* Fri Apr 18 1997 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>

- added making packages: tkmc, mcserv (xmc not work yet),
- gziped man pages,
- added /etc/pamd.d/mcserv PAM config file.
- added instaling icons,
- added /etc/profile.d/mc.sh,
- in %doc added NEWS README,
- removed /usr/lib/mc/FAQ,
- added mcserv.init script for mcserv (start/stop on level 86).
