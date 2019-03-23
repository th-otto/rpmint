Summary: A utility which displays a tree view of the contents of directories.
Name: tree
Version: 1.2
Release: 2
Group: Applications/File
Copyright: GPL
Source: ftp://sunsite.unc.edu/pub/Linux/Incoming/tree-1.2.tgz
Patch0: tree-mint.patch
Prefix: /usr
BuildRoot: /var/tmp/tree-root
Packager: Edgar Aichinger <eaiching@t0.or.at>
Vendor: Sparemint
Requires: /bin/bash
Summary(de): Ein Utility zur Darstellung einer Baum-Ansicht von Verzeichnis-Inhalten.

%description
The tree utility recursively displays the contents of directories in a
tree-like format.  Tree is basically a UNIX port of the tree DOS
utility.

Install tree if you think it would be useful to view the contents of
specified directories in a tree-like format.

%description -l de
Das Hilfsprogramm tree stellt die Inhalte von Verzeichnissen rekursiv in
einem baum-Ñhnlichen Format dar.  Tree ist ein UNIX-Port des Programmes 
tree aus der DOS-Welt.

Installieren Sie tree wenn Sie es fÅr hilfreich erachten, den Inhalt von
bestimmten Verzeichnissen in einem baum-artigen Format anzusehen.

%prep
%setup -q
%patch0 -p1 -b .mint

%build
rm -f tree
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1}

make	BINDIR=$RPM_BUILD_ROOT/usr/bin \
	MANDIR=$RPM_BUILD_ROOT/usr/man/man1 \
	install
strip $RPM_BUILD_ROOT/usr/bin/tree
gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/tree.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/tree
/usr/man/man1/tree.1.gz
%doc README

%changelog
* Wed Sep 01 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpage

* Sat Aug 28 1999 Edgar Aichinger <eaiching@t0.or.at>
- added german translations, Packager, Vendor, Requires to spec-file
- #include <limits.h> instead of <linux/limits.h>
- added pseudo opcode for S_IFSOCK to make compile
