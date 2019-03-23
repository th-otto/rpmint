Summary: A utility for creating TTY dialog boxes.
Name: dialog
Version: 0.6
Release: 1
Copyright: GPL
Group: Applications/System
Packager: Frank Naumann <fnaumann@cs.uni-magdeburg.de>
Vendor: Sparemint
Source: ftp.redhat.com:/pub/misc/dialog-0.6.tar.gz
Patch0: dialog-0.6-ncurses.patch
Patch1: dialog-0.6-opt.patch
Patch2: dialog-0.6-loop.patch
Patch3: dialog-0.6-mint.patch
BuildRoot: /var/tmp/dialog-root

%description
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces.  Dialog is called
from within a shell script.  The following dialog boxes are implemented:
yes/no, menu, input, message, text, info, checklist, radiolist, and
gauge.  

Install dialog if you would like to create TTY dialog boxes.

%prep
%setup -q
%patch0 -p1 -b .ncurses
%patch1 -p1 -b .opt
%patch2 -p1 -b .loop
%patch3 -p1 -b .mint
cd src
make depend

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1}

make PREFIX=$RPM_BUILD_ROOT/usr install

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/dialog.1
strip $RPM_BUILD_ROOT/usr/bin/dialog
stack --fix=64k $RPM_BUILD_ROOT/usr/bin/dialog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING dialog.lsm INSTALL README samples
/usr/bin/dialog
/usr/man/man1/dialog.1.gz

%changelog
* Wed Sep 14 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- initial release
