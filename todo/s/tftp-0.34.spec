Summary          : TFTP server daemon and client
Name          	 : tftp
Version       	 : 0.34
Copyright     	 : GPL
Group         	 : Applications/Internet 
Release		 : 1
Packager      	 : Jens Syckor <js712688@mail.inf.tu-dresden.de>
Vendor       	 : Sparemint

Prefix        	 : %{_prefix}
Docdir       	 : %{_prefix}/doc
BuildRoot     	 : %{_tmppath}/%{name}-%{version}

Source: %{name}-%{version}.tar

%description
This is the mint port of tftp-hpa, a conglomerate of a number of versions of the BSD TFTP code, changed around to port to a whole collection of operating systems.  

Includes the tftpd server daemon and tftp client. TFTP is very useful
for booting diskless computers over network (for instance with the bootloader grub).

%prep


%build
cd tftp-0.34
make

%install
cd tftp-0.34
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man8

install -c tftp/tftp $RPM_BUILD_ROOT/usr/bin/
install -c -m 644 tftp/tftp.1 $RPM_BUILD_ROOT/usr/man/man1/
install -c tftpd/tftpd $RPM_BUILD_ROOT/usr/sbin/
install -c -m 644 tftpd/tftpd.8 $RPM_BUILD_ROOT/usr/man/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/tftp
/usr/sbin/tftpd
/usr/man/man1/tftp.1
/usr/man/man8/tftpd.8

%changelog
* Sun Jun 29 2003 Jens Syckor <js712688@inf.tu-dresden.de>
- first release for freemint
