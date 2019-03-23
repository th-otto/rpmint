Summary: The elm mail user agent.
Name: elm
Version: 2.5.0
Release: 0.2pre8
Copyright: distributable
Group: Applications/Internet
Url: http://www.myxa.com/elm.html
Source0: ftp://dsinc.myxa.com/pub/elm/elm2.5.0pre8.tar.gz
Source1: elm.wmconfig
Patch0: elm-2.5.0pre8-config.patch
Patch1: elm-2.5.0pre8-compat21.patch
Patch2: elm-mint.patch
Summary(de): Das E-Mail-Programm elm
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
BuildRoot: /var/tmp/%{name}-root

%description
Elm is a popular terminal mode email user agent.  Elm includes all
standard mailhandling features, including MIME support via metamail.

Elm is still used by some people, but is no longer in development.  If
you've used Elm before and you're devoted to it, you should install the
elm package.  If you would like to use metamail's MIME support, you'll
also need to install the metamail package.

%description -l de
Elm ist ein populäres terminal-basiertes E-Mail-Programm.  Elm hat
alle Standard-Mailbehandlungs-Fähigkeiten, einschließlich
MIME-Unterstützung über metamail.

Elm wird noch immer von einigen Leuten benutzt, wird aber nicht weiter
entwickelt.  Wenn Sie Elm schon früher benutzt haben, und Sie es
mögen, sollten Sie Elm installieren.  Falls Sie auch Metamails
MIME-Unterstützung haben möchten, sollten Sie auch das Metamail-Paket
installieren.

%prep
%setup -q -n elm2.5.0pre8

%patch0 -p1 -b .p11
%patch1 -p1 -b .p17
%patch2 -p1 -b .mint

%build
touch .CHECK Makefile */Makefile
mkdir -p bin
make OPTIMIZE="$RPM_OPT_FLAGS" LIBS="-lport -ltermcap -lsocket" RANLIB="ranlib"
strip bin/* || :

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,lib/elm,man/man1}

make	DESTBIN=$RPM_BUILD_ROOT/usr/bin \
	BIN=$RPM_BUILD_ROOT/usr/bin \
	DESTLIB=$RPM_BUILD_ROOT/usr/lib/elm \
	LIB=$RPM_BUILD_ROOT/usr/lib/elm \
	MAN=$RPM_BUILD_ROOT/usr/man/man1 \
	install

( cd $RPM_BUILD_ROOT
  mkdir -p ./etc/X11/wmconfig
  install -m 644 $RPM_SOURCE_DIR/elm.wmconfig ./etc/X11/wmconfig/elm
)

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*
stack --fix=64k $RPM_BUILD_ROOT/usr/bin/* || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(missingok) /etc/X11/wmconfig/elm
/usr/bin/elm
/usr/bin/answer
/usr/bin/checkalias
/usr/bin/elmalias
/usr/bin/fastmail
/usr/bin/frm
/usr/bin/listalias
/usr/bin/messages
/usr/bin/newalias
/usr/bin/newmail
/usr/bin/printmail
/usr/bin/readmsg
/usr/lib/elm
/usr/bin/wnewmail
/usr/bin/nfrm
/usr/man/man1/answer.1.gz
/usr/man/man1/checkalias.1.gz
/usr/man/man1/elm.1.gz
/usr/man/man1/elmalias.1.gz
/usr/man/man1/fastmail.1.gz
/usr/man/man1/frm.1.gz
/usr/man/man1/listalias.1.gz
/usr/man/man1/messages.1.gz
/usr/man/man1/newalias.1.gz
/usr/man/man1/newmail.1.gz
/usr/man/man1/printmail.1.gz
/usr/man/man1/readmsg.1.gz
/usr/man/man1/wnewmail.1.gz

%changelog
* Sat Sep 11 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial revision.
