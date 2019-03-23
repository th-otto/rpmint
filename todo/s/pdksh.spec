Summary: A public domain clone of the Korn shell (ksh).
Name: pdksh
Version: 5.2.13
Release: 1
Copyright: Public Domain
Group: System Environment/Shells
Source: ftp.cs.mun.ca:/pub/pdksh/%{name}-%{version}.tar.gz
Patch0: pdksh-5.2.13-compat21.patch
Patch1: pdksh-noeisdir.patch
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
# Just in case ...
# Conflicts: pdksh-mbaserel
BuildRoot: /var/tmp/%{name}-root
Summary(de): Ein Public-Domain-Klon der Korn-Shell (ksh).

%description
The pdksh package contains PD-ksh, a clone of the Korn shell (ksh).
The ksh shell is a command interpreter intended for both interactive
and shell script use.  Ksh's command language is a superset of the
sh shell language.

The pdksh has been barely tested under MiNT.  It is provided here on
special request. ;-)

Install the pdksh package if you want to use a version of the ksh
shell.

%description -l de
Das Paket pdksh enth„lt die PD-ksh, ein Klon der Korn-Shell (ksh).
Die ksh-Shell ist ein Kommandozeilen-Interpreter, der sowohl fr
interaktive als auch fr Shell-Skript-Benutzung gedacht ist.  Die
Kommando Sprache der ksh ist eine Obermente der Shell-Sprache sh.

Das Paket pdksh sollte installiert werden, wenn eine Version der
Korn-Shell (ksh) erforderlich ist.

%prep
%setup -q
#%patch0 -p1 -b .compat21
%patch1 -p1 -b .noeisdir

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS=-s ./configure --prefix=/usr

make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,usr/bin,usr/man/man1}

/usr/bin/install -s -c -m755 ksh $RPM_BUILD_ROOT/bin/ksh
stack --fix=64k $RPM_BUILD_ROOT/bin/ksh
/usr/bin/install -c -m644 ksh.1 $RPM_BUILD_ROOT/usr/man/man1/ksh.1
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/ksh.1
# /bin/ksh and /usr/bin/ksh may be the same file.  It doesn't
# look like a good idea to force a link.  Better do that in
# other sections.
# ln -sf /bin/ksh $RPM_BUILD_ROOT/usr/bin/ksh
ln -sf /bin/ksh $RPM_BUILD_ROOT/usr/bin/pdksh
ln -sf ksh.1.gz $RPM_BUILD_ROOT/usr/man/man1/pdksh.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	echo "/bin/ksh" > /etc/shells
else
	if ! grep '^/bin/ksh$' /etc/shells > /dev/null; then
		echo "/bin/ksh" >> /etc/shells
	fi
fi
ln -sf /bin/ksh /usr/bin/ksh 2>/dev/null || :

%postun
if [ ! -f /bin/ksh ]; then
	grep -v /bin/ksh /etc/shells > /etc/shells.new
	mv /etc/shells.new /etc/shells
fi
if [ -h /usr/bin/pdksh ]; then
	rm -f /usr/bin/pdksh
fi

%verifyscript

echo -n "Looking for ksh in /etc/shells... "
if ! grep '^/bin/ksh$' /etc/shells > /dev/null; then
    echo "missing"
    echo "ksh missing from /etc/shells" >&2
else
    echo "found"
fi
echo -n "Looking for symbolic link /usr/bin/pdksh ... "
if [ -h /usr/bin/pdksh ]; then
	echo "found"
else
	echo "missing"
fi

%files
%defattr(-,root,root)
%doc README NOTES PROJECTS NEWS BUG-REPORTS
/bin/ksh
/usr/bin/pdksh
/usr/man/man1/ksh.1.gz
/usr/man/man1/pdksh.1.gz
