Summary       : Smart decoder for uuencode, xxencode, Base64 and BinHex
Name          : uudeview
Version       : 0.5.18
Release       : 1
Copyright     : GPL
Group         : Applications/File

Packager      : Clement Benrabah <clement.benrabah@wanadoo.fr>
Vendor        : Sparemint
URL           : http://www.fpx.de/fp/Software/UUDeview/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: http://www.fpx.de/fp/Software/UUDeview/download/uudeview-0.5.18.tar.gz
Patch0: uudeview-0.5.18-tcl.patch


%description
UUDeview is a smart decoder for several surfaces which are common in
email and Usenet. It can decode uuencode, xxencode, Base64 and BinHex.
It can handle multiple files and multiple parts, even in random order.
Also an encoder is attached, UUEnview.


%prep
%setup -q
%patch0 -p1 -b .tcl


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix} \
	--disable-tcl
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	BINDIR=${RPM_BUILD_ROOT}%{_prefix}/bin \
	MANDIR=${RPM_BUILD_ROOT}%{_prefix}/share/man

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=96k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc COPYING HISTORY IAFA-PACKAGE README
%{_prefix}/bin/*
%{_prefix}/share/man/*/*


%changelog
* Sat Jan 04 2003 Clement Benrabah <clement.benrabah@wanadoo.fr> 
- Updated to 0.5.18
