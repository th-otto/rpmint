Summary: The GNU line editor.
Name: ed
Version: 0.2
Release: 1
Copyright: GPL
Group: Applications/Text
Source: ftp://prep.ai.mit.edu/pub/gnu/ed-0.2.tar.gz
Prereq: /sbin/install-info
Buildroot: /var/tmp/%{name}-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Summary(de): Der GNU Zeileneditor.


%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it much.

%description -l de
Ed ist ein zeilen-orientierter Texteditor und wird benÅtzt, um Textdateien
zu erzeugen, anzuzeigen und zu Ñndern (sowohl interaktiv als auch per 
Shellskripts). Im Normalfall wird man statt ed heute eher "seitenweise" 
Editoren wie emacs oder vi verwenden.

Ed war der ursprÅngliche UNIX Editor, und wird mîglicherweise von manchen 
Programmen benÅtzt. Im allgemeinen aber mÅssen Sie es nicht installieren und werden 
werden es vermutlich auch nicht oft verwenden.

%prep
%setup -q

%build
%configure --prefix=/usr --exec-prefix=/
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s

%install
make CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s prefix=$RPM_BUILD_ROOT/usr \
     exec_prefix=$RPM_BUILD_ROOT install
gzip -fn $RPM_BUILD_ROOT/usr/info/ed.info
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/r%{name}.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/%{name}.1

strip $RPM_BUILD_ROOT/bin/ed

%post
/sbin/install-info /usr/info/ed.info.gz /usr/info/dir --entry="* ed: (ed).                  The GNU Line Editor."

%preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete /usr/info/ed.info.gz /usr/info/dir --entry="* ed: (ed).                  The GNU Line Editor."
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc NEWS POSIX README THANKS
/bin/ed
/bin/red
/usr/info/ed.info.gz
/usr/man/man1/ed.1.gz
/usr/man/man1/red.1.gz

%changelog
* Sat Sep 08 1999 Edgar Aichinger <eaiching@t0.or.at>
- First Release for SpareMiNT 
- added Vendor, Packager, german Summary/Description
- compressed manpage

* Tue Mar 23 1999 Jeff Johnson <jbj@redhat.com>
- fix %post syntax error (#1689).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 11)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Dec 18 1998 Preston Brown <pbrown@redhat.com>
- bumped spec number for initial rh 6.0 build

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added install-info support
- added BuildRoot
- correct URL in Source line

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
