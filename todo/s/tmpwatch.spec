Summary: A utility for removing files based on when they were last accessed.
Name: tmpwatch
%define version 1.7
Version: %{version}
Release: 2
Source: tmpwatch-%{version}.tar.gz
Patch: tmpwatch-stripman.patch
Copyright: GPL
Group: System Environment/Base
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
BuildRoot: /var/tmp/tmpwatch-root
Summary(de): Hilfsmittel um Dateien auf Basis der letzten Zugriffszeit zu löschen.

%description
The tmpwatch utility recursively searches through specified directories
and removes files which have not been accessed in a specified period of
time.  Tmpwatch is normally used to clean up directories which are used
for temporarily holding files (for example, /tmp).  Tmpwatch ignores
symlinks, won't switch filesystems and only removes empty directories
and regular files.

%description -l de
Das Hilfsmittel tmpwatch durchsucht die angegebenen Verzeichnisse rekursiv
und entfernt Dateien, auf die seit einer festlegbaren Zeit nicht mehr
zugegriffen wurde.  Tmpwatch wird in der Regel benutzt, um Verzeichnisse,
die temporäre Dateien enthalten (beispielsweise /tmp) zu säubern.  Tmpwatch
ignoriert symbolische Links, wechselt keine Dateisystem und entfernt nur
leere Verzeichnisse und reguläre Dateien.

%prep
%setup -q
%patch -p1 -b .stripman

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install
gzip -9nf $RPM_BUILD_ROOT/usr/man/man8/tmpwatch.8

mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
cat >$RPM_BUILD_ROOT/etc/cron.daily/tmpwatch <<FOOT_OF_PRIDE
#! /bin/sh
# /etc/cron.daily/tmpwatch: Clean tmp dirs.
/usr/sbin/tmpwatch 240 /tmp /var/tmp /var/catman/cat?
FOOT_OF_PRIDE
chmod +x $RPM_BUILD_ROOT/etc/cron.daily/tmpwatch

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/sbin/tmpwatch
/usr/man/man8/tmpwatch.8.gz
%config /etc/cron.daily/tmpwatch

%changelog
* Wed Aug 25 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Added German translation.
- Modified to meet Sparemint standards.
