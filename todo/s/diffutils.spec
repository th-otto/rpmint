Summary: GNU diff Utilities
Name: diffutils
Version: 2.7
Release: 2
Group: Utilities/Text
Source: ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.gz
Patch0: diffutils-unneeded.patch
Copyright: GPL
Prereq: /sbin/install-info
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Buildroot: /var/tmp/diff-root
Summary(de): GNU-Diff-Utilities 
Summary(fr): Utilitaires diff de GNU
Summary(tr): GNU dosya karþýlaþtýrma araçlarý

%description
The diff utilities can be used to compare files, and generate a record
of the "differences" between files.  This record can be used by the
patch program to bring one file up to date with the other.  All these
utilities (except cmp) only work on text files.

%description -l de
Die Diff-Utilities koennen zum Vergleich von Dateien verwendet werden, und
erzeugen geben die Unterschiede zwischen Dateien aus. Diese Ausgabe kann 
vom Programm »patch« benutzt werden, um Dateien auf dieser Grundlage zu
aktualisieren. All diese Programme (außer cmp) arbeiten nur mit Textdateien.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="$RPM_OPT_FLAGS"
export CFLAGS
./configure --prefix=/usr 
make LDFLAGS=-s PR_PROGRAM=/usr/bin/pr

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/usr install
gzip -9nf $RPM_BUILD_ROOT/usr/info/diff*

cd $RPM_BUILD_ROOT
strip $RPM_BUILD_ROOT/usr/bin/{diff,diff3,sdiff,cmp}

%post
/sbin/install-info /usr/info/diff.info.gz /usr/info/dir --entry="* diff: (diff).                 The GNU diff."

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete /usr/info/diff.info.gz /usr/info/dir --entry="* diff: (diff).                 The GNU diff."
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc NEWS README
/usr/bin/*
/usr/info/diff.info*gz

%changelog
* Wed Aug 11 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Changed vendor to Sparemint.
