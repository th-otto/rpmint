Summary: A fast, compact editor based on the slang screen library.
Name: jed
Version: 0.99.16
Release: 2
Copyright: GPL
Group: Applications/Editors
Source: ftp://space.mit.edu/pub/davis/jed/v0.99/%{name}-0.99-16.tar.gz
Requires: slang >= 1.4.4
Prefix: %{_prefix}
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Vendor: Sparemint
Packager: Keith Scroggins <kws@radix.net>

%description
Jed is a fast, compact editor based on the slang screen library. Jed
features include emulation of the Emacs, EDT, WordStar and Brief editors;
support for extensive customization with slang macros, colors, keybindings,
etc.; and a variety of programming modes with syntax highlighting.

%package common
Summary: Files needed by any Jed editor.
Group: Applications/Editors
%description common
The jed-common package contains files (such as .sl files) that are
needed by any jed binary in order to run.

%package -n rgrep
Summary: A grep utility which can recursively descend through directories.
Group: Applications/Text

%description -n rgrep
The rgrep utility can recursively descend through directories as
it greps for the specified pattern.  Note that this ability does
take a toll on rgrep's performance, which is somewhat slow.  Rgrep
will also highlight the matching expression.

Install the rgrep package if you need a recursive grep which can
highlight the matching expression.

%prep
rm -rf $RPM_BUILD_DIR/%{name}-0.99-16
%setup -q -n %{name}-0.99-16

%build
./configure --prefix=/usr -exec-prefix=/usr 
make all JED_ROOT=/usr/jed
make getmail JED_ROOT=/usr/jed

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr
make install prefix=$RPM_BUILD_ROOT/usr exec_prefix=/usr BIN_DIR=$RPM_BUILD_ROOT/usr/bin/ JED_ROOT=$RPM_BUILD_ROOT/usr/jed/
sed -e \
  's/file = "\/etc\/jed-defaults.sl";/%file = "\/etc\/jed-defaults.sl";/;' \
  $RPM_BUILD_ROOT/usr/jed/lib/site.sl > $RPM_BUILD_ROOT/usr/jed/lib/site.sl.new
mv -f $RPM_BUILD_ROOT/usr/jed/lib/site.sl.new $RPM_BUILD_ROOT/usr/jed/lib/site.sl
# now make .slc files
JED_ROOT=$RPM_BUILD_ROOT/usr/jed $RPM_BUILD_ROOT/usr/bin/jed -batch -n -l preparse.sl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/jed

%files common
%defattr(-,root,root)
%doc COPYING COPYRIGHT doc INSTALL INSTALL.be INSTALL.pc INSTALL.unx INSTALL.vms README changes.txt
/usr/man/man1/jed.1*
/usr/jed/bin
/usr/jed/info
/usr/jed/lib

%files -n rgrep
%defattr(-,root,root)
/usr/bin/rgrep
/usr/man/man1/rgrep.1*

%post
ln -sf /usr/doc/jed-common-%{version}/doc /usr/jed/doc

%preun
rm -f /usr/jed/doc

%changelog
* Tue Mar 02 2004 Keith Scroggins <kws@radix.net>
- Fixed install location.

* Tue Nov 04 2003 Keith Scroggins <kws@radix.net>
- Initial build of Jed/rgrep for FreeMiNT
