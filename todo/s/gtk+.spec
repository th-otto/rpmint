Summary       : The GIMP ToolKit (GTK+), a library for creating GUIs for X.
Name          : gtk+
Version       : 1.2.8
Release       : 2
Copyright     : LGPL
Group         : Development/Libraries

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gtk.org/

Prereq        : /sbin/install-info
BuildRequires : XFree86-devel, glib >= %{version}
Requires      : XFree86-devel, glib >= %{version}

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gimp.org/pub/gtk/v1.2/%{name}-%{version}.tar.gz
Source1: gtkrc-default
Source2: gtk+-1.2.4-po.tar.gz
Source3: gtk+-i18n-files.tar.gz
Patch0:  gtk+-1.2.8-mint-x11.patch


%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

Install gtk+-devel if you need to develop GTK+ applications.  You'll also
need to install the gtk+ package.


%prep
%setup -n %{name}-%{version} -q
# better we fix the xserver font things
#%patch0 -p1

tar xzf %{SOURCE2}
tar xzf %{SOURCE3}
cp configure.in AA && \
        cat AA | sed 's|^ALL_LINGUAS.*$|ALL_LINGUAS="ca cs de es fi fr hr hu it ja ko nl no pl pt ru sl sk sv wa zh_TW.Big5"|' > configure.in


%build
[ -f ./autogen.sh ] && {
CFLAGS="${RPM_OPT_FLAGS}" \
sh ./autogen.sh \
	--prefix=%{_prefix} \
	--sysconfdir="/etc" \
	--with-xinput=xfree \
	--enable-debug=no
} || {
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--sysconfdir="/etc" \
	--with-xinput=xfree \
	--enable-debug=no
}

make


%install
rm -rf ${RPM_BUILD_ROOT}

make prefix=${RPM_BUILD_ROOT}%{_prefix} sysconfdir=${RPM_BUILD_ROOT}/etc install
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/g*.info*
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*

install -m 444 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/gtk/gtkrc

# i18n garbage with this one.
rm -f ${RPM_BUILD_ROOT}/etc/gtk/gtkrc

cat > ${RPM_BUILD_ROOT}/etc/gtk/gtkrc << EOF
style "gtk-tooltips-style" {
  bg[NORMAL] = "#ffffc0"
}

widget "gtk-tooltips" style "gtk-tooltips-style"
EOF


%clean
rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/gdk.info.gz %{_prefix}/info/dir --entry="* gdk: (gtk+).                                  GDK, the General Drawing Kit."
/sbin/install-info %{_prefix}/info/gtk.info.gz %{_prefix}/info/dir --entry="* gtk: (gtk+).                                  GTK, the GIMP Toolkit."

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_prefix}/info/gdk.info.gz %{_prefix}/info/dir --entry="* gdk: (gtk+).                                  GDK, the General Drawing Kit."
  /sbin/install-info --delete %{_prefix}/info/gtk.info.gz %{_prefix}/info/dir --entry="* gtk: (gtk+).                                  GTK, the GIMP Toolkit."
fi


%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%doc docs/html
%config /etc/gtk/*
%{_prefix}/share/themes/Default
%{_prefix}/share/locale/*/*/*
%{_prefix}/lib/*a
%{_prefix}/include/*
%{_prefix}/info/*.info*
%{_prefix}/share/aclocal/*
%{_prefix}/share/man/man1/*
%{_prefix}/bin/*


%changelog
* Fri Dec 22 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
