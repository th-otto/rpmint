Summary: The /bin/mail program, which is used to send mail via shell scripts.
Name: mailx
Version: 8.1.1
Release: 1
Copyright: BSD
Group: Applications/Internet
Source: ftp://ftp.debian.org/pub/debian/hamm/source/mail/mailx-8.1.1.tar.gz
Patch0: mailx-8.1.1.debian.patch
Patch1: mailx-8.1.1.security.patch
Patch2: mailx-8.1.1.nolock.patch
Patch3: mailx-8.1.1.debian2.patch
Patch4: mailx-mint.patch
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Summary(de): Das /bin/mail-Programm, zur Mail-Versendung aus Shell-Skripts.
BuildRoot: /var/tmp/%{name}-root

%description
The mailx package installs the /bin/mail program, which is used to send
quick email messages (i.e., without opening up a full-featured mail user
agent). Mail is often used in shell scripts.

You should install mailx because of its quick email sending ability, which
many shell scripts rely on.

%description -l de
Das Mailx-Paket installiert das /bin/mail-Programm, das benutzt wird,
um schnelle Email-Nachrichten (also, ohne einen E-Mail-Client mit
allen Schikanen zu ”ffnen).  Mail wird oft in Shell-Skripts verwendet.

Mailx sollte aufgrund seiner F„higkeiten, schnell eine E-Mail zu 
versenden, installiert werden, was von vielen Shell-Skripts ausgenutzt
wird.

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .mint

%build
make CFLAGS="$RPM_OPT_FLAGS" LIBS=-lport

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,etc,usr/bin,usr/lib,usr/man/man1}

make DESTDIR=$RPM_BUILD_ROOT install
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

( cd $RPM_BUILD_ROOT
  mv ./usr/bin/mail ./bin/mail
  chmod g-s ./bin/mail
  ln -sf ../../bin/mail ./usr/bin/Mail
  ln -sf mail.1.gz ./usr/man/man1/Mail.1.gz
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,mail)	/bin/mail
/usr/bin/Mail
/usr/lib/mail.help
/usr/lib/mail.tildehelp
%config /etc/mail.rc
/usr/man/man1/mail.1.gz
/usr/man/man1/Mail.1.gz

%changelog
* Tue Sep 09 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Initial revision.
