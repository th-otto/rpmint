Summary: An easy to use, modeless text editor.
Name: joe
Version: 2.8
Release: 1
Copyright: GPL
Group: Applications/Editors
Source: ftp://ftp.std.com/src/editors/joe2.8.tar.Z
Patch0: joe2.8-config.patch
Patch1: joe2.8-time.patch
Patch2: joe2.8-axphack.patch
Patch3: joe2.8-make.patch
Patch4: joe2.8-locale.patch
Patch5: joe-2.8-port.patch
Patch6: joe-2.8-mips.patch
Patch7: joe-2.8-mint.patch
Buildroot: /var/tmp/joe-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Ein leicht bedienbarer Texteditor ohne Modi.

%description
Joe is an easy to use, modeless text editor which would be very
appropriate for novices.  Joe uses the same WordStar keybindings used in
Borland's development environment.

You should install joe if you've used it before and you liked it, or if
you're still deciding what text editor you'd like to use, or if you have a
fondness for WordStar.  If you're just starting out, you should probably
install joe because it is very easy to use.

%description -l de
Joe ist ein leicht bedienbarer Texteditor ohne Modi, der für Beginner
angemessen erscheint.  Joe benützt dieselben WordStar-Tastaturkürzel
wie auch die Entwicklungsumgebung von Borland.

Sie sollten joe installieren,wen Sie ihn schon verwendet und gemocht haben,
oder wenn Sie sich noch für keinen anderen Texteditor entschieden haben,
oder eine Vorliebe für WordStar haben.  Wenn Sie gerade erst beginnen,
sollten Sie joe installieren, weil er sehr leicht zu benützen ist.

%prep
%setup -q -n joe
%patch0 -p1 -b .config
%patch1 -p1 -b .time

%ifarch axp
%patch2 -p1 -b .axp
%endif

%patch3 -p1 -b .make
%patch4 -p1 -b .locale

%patch5 -p1 -b .port

%ifarch mipsel mipseb
%patch6 -p1 -b .mips
%endif
%patch7 -p1 -b .mint


%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DUSE_LOCALE"

%install
rm -rf $RPM_BUILD_ROOT
make install TOPDIR=$RPM_BUILD_ROOT
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1
strip joe

%files
/usr/bin/*
%dir /usr/lib/joe 
%config /usr/lib/joe/*
/usr/man/man1/joe.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Sep 09 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- added Vendor, Packager, german Summary/Description
- compressed manpage
- #ifdef'd SV_INTERRUPT (tty.c)

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- added locale patch from  Petr Kolar <PETR.KOLAR@vslib.cz>
  (yeah, finally!)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 17)

* Wed Jan 20 1999 Alex deVries <puffin@redhat.com>
- added mipseb support

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Sep 15 1998 Cristian Gafton <gafton@redhat.com>
- built with Alan's -port patch

* Fri May 08 1998 Cristian Gafton <gafton@redhat.com>
- enable -asis in the config files so international keyboards will be better
  supported

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- /usr/lib/joe/* are config files

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- manhattan build

* Thu Dec 11 1997 Cristian Gafton <gafton@redhat.com>
- fixed termcap problems for terms other than 80x25
- added support for buildroot and BuildRoot

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

