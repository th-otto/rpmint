%define initdir /etc/rc.d/init.d
%define auth %(test -f /etc/pam.d/system-auth && echo /etc/pam.d/system-auth || echo)

Summary: The Samba SMB/CIFS server.
Name: samba
Version: 3.0.1
Release: 1
License: GNU GPL Version 2
Group: System Environment/Daemons
Packager: Mark Duckworth <mduckworth@atari-source.com>
Vendor: Sparemint
URL: http://www.samba.org/
Requires: samba-common = %{version} 
Requires: logrotate >= 3.4
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prereq: /bin/mktemp /usr/bin/killall
Prereq: fileutils sed /etc/init.d 
BuildRequires: readline-devel, ncurses-devel, fileutils
BuildRequires: mintlib-devel >= 0.57.4
Source: ftp://us2.samba.org/pub/samba/%{name}-%{version}.tar.bz2
Source1: smb.init
Source2: samba.sysconfig
Source3: samba.log
Patch0: samba-3.0.1-mint.patch

%description
Samba is the protocol by which a lot of PC-related machines share
files, printers, and other information (such as lists of available
files and printers). The Windows NT, OS/2, and Linux operating systems
support this natively, and add-on packages can enable the same thing
for DOS, Windows, VMS, UNIX of all kinds, MVS, and more. This package
provides an SMB server that can be used to provide network services to
SMB (sometimes called "Lan Manager") clients. Samba uses NetBIOS over
TCP/IP (NetBT) protocols and does NOT need the NetBEUI (Microsoft Raw
NetBIOS frame) protocol.

%package client
Summary: Samba (SMB) client programs.
Group: Applications/System
Requires: samba-common = %{version}
Obsoletes: smbfs

%description client
The samba-client package provides some SMB clients to compliment the
built-in SMB filesystem in Linux. These clients allow access of SMB
shares and printing to SMB printers.

%package common
Summary: Files used by both Samba servers and clients.
Group: Applications/System

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%package swat
Summary: The Samba SMB server configuration program.
Group: Applications/System
Requires: samba = %{version}

%description swat
The samba-swat package includes the new SWAT (Samba Web Administration
Tool), for remotely managing Samba's smb.conf file using your favorite
Web browser.

%prep
%setup -q
%patch0 -p1

# copy sparemint scripts
cp %{SOURCE1} packaging/RedHat/
cp %{SOURCE2} packaging/RedHat/

# crap
rm -f examples/VFS/.cvsignore
mv source/VERSION source/VERSION.orig
sed -e 's/SAMBA_VERSION_VENDOR_SUFFIX=$/&\"%{release}\"/' < source/VERSION.orig > source/VERSION
cd source
script/mkversion.sh
cd ..



%build
cd source
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
CPPFLAGS="$CPPFLAGS -I/usr/include/openssl"; export CPPFLAGS
LIBS="-lsocket"; export LIBS
CC="/usr/local/bin/gcc" ; export CC
./configure \
	--build=m68k-atari-mint \
	--host=m68k-atari-mint \
	--target=m68k-atari-mint \
	--with-codepagedir=%{_datadir}/samba/codepages \
	--with-fhs \
	--prefix=/usr \
	--localstatedir=/var \
	--libdir=/usr/lib/samba \
	--with-configdir=/etc/samba \
	--enable-static \
	--disable-shared \
	--with-libsmbclient \
	--with-lockdir=/var/cache/samba \
	--with-piddir=/var/run \
	--with-privatedir=/etc/samba \
	--with-swatdir=%{_datadir}/swat \
	--with-syslog \
	--with-utmp \
	--with-vfs \
	--without-smbwrapper

make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" debug2html
make CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" smbfilter

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/{sbin,bin}
mkdir -p $RPM_BUILD_ROOT/%{initdir}
mkdir -p $RPM_BUILD_ROOT/usr/private
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
mkdir -p $RPM_BUILD_ROOT/var/spool/samba
mkdir -p $RPM_BUILD_ROOT/var/log/samba
mkdir -p $RPM_BUILD_ROOT/var/cache/samba
mkdir -p $RPM_BUILD_ROOT/var/cache/samba/winbindd_privileged
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/swat/using_samba
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/samba/codepages 

cd source

%makeinstall \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	BASEDIR=$RPM_BUILD_ROOT%{_prefix} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	DATADIR=$RPM_BUILD_ROOT%{_datadir} \
	LOCKDIR=$RPM_BUILD_ROOT/var/cache/samba \
	PRIVATEDIR=$RPM_BUILD_ROOT/etc/samba \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/samba \
	CONFIGDIR=$RPM_BUILD_ROOT/etc/samba \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	VARDIR=$RPM_BUILD_ROOT/var/log/samba \
	CODEPAGEDIR=$RPM_BUILD_ROOT%{_datadir}/samba/codepages \
	SWATDIR=$RPM_BUILD_ROOT%{_datadir}/swat \
	SAMBABOOK=$RPM_BUILD_ROOT%{_datadir}/swat/using_samba \
	PIDDIR=$RPM_BUILD_ROOT/var/run

cd ..

# Install other stuff
install -m644 packaging/RedHat/smb.conf $RPM_BUILD_ROOT/etc/samba/smb.conf
install -m755 packaging/RedHat/smb.init $RPM_BUILD_ROOT/etc/rc.d/init.d/smb
install -m644 packaging/RedHat/samba.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/samba
install -m755 source/script/mksmbpasswd.sh $RPM_BUILD_ROOT%{_bindir}
install -m644 packaging/RedHat/smbusers $RPM_BUILD_ROOT/etc/samba/smbusers
install -m755 packaging/RedHat/smbprint $RPM_BUILD_ROOT%{_bindir}
install -m644 $RPM_SOURCE_DIR/samba.log $RPM_BUILD_ROOT/etc/logrotate.d/samba
echo 127.0.0.1 localhost > $RPM_BUILD_ROOT/etc/samba/lmhosts

rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/editreg.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/log2pcap.1*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/smbsh.1*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/mount.cifs.8*

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=128K ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:
stack --fix=128K ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat <<EOF
=================
!!! IMPORTANT !!!
=================
Thanks for installing samba.  Note, the config dir is /etc/samba.  The 
private dir (smbpasswd) is in /usr/private.  You will have to customize
the smb.conf file so that it has an interfaces line in order for samba
to work, i.e. interfaces = 192.168.80.0/24 127.0.0.0/24.
In addition this build has a tendency to stop working after a while
and complain of a lack of memory when there's clearly plenty of available.
A restart of smbd and nmbd is the only thing that seems to fix it.
For other bug reports, especially with the rpm build or installation 
paths, please email mduckworth@atari-source.com... until then, happy 
networking!
EOF

%preun
if [ $1 = 0 ] ; then
    rm -rf /var/log/samba/* /var/cache/samba/*
fi
exit 0

%files
%defattr(-,root,root)
%doc README COPYING Manifest 
%doc WHATSNEW.txt Roadmap
%doc docs
%doc examples/autofs examples/LDAP examples/libsmbclient examples/misc examples/printer-accounting
%doc examples/printing

%{_sbindir}/smbd
%{_sbindir}/nmbd
# %{_bindir}/make_unicodemap
%{_bindir}/mksmbpasswd.sh
%{_bindir}/smbcontrol
%{_bindir}/smbstatus
# %{_bindir}/smbadduser
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%config(noreplace) /etc/sysconfig/samba
%config(noreplace) /etc/samba/smbusers
%config(noreplace) /etc/logrotate.d/samba
%config(noreplace) /etc/rc.d/init.d/smb
# %{_mandir}/man1/make_unicodemap.1*
%{_mandir}/man1/smbcontrol.1*
%{_mandir}/man1/smbstatus.1*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*
#%{_mandir}/man7/Samba.7*
%{_mandir}/man8/nmbd.8*
%{_mandir}/man8/pdbedit.8*
%{_mandir}/man8/smbd.8*
%{_mandir}/man8/tdbbackup.8*
#%{_mandir}/ja/man1/smbstatus.1*
#%{_mandir}/ja/man5/smbpasswd.5*
#%{_mandir}/ja/man7/samba.7*
#%{_mandir}/ja/man8/smbd.8*
#%{_mandir}/ja/man8/nmbd.8*
%{_libdir}/samba/vfs

%attr(0700,root,root) %dir /var/log/samba
%attr(1777,root,root) %dir /var/spool/samba
%attr(0700,root,root) %dir /usr/private

%files swat
%defattr(-,root,root)
%{_datadir}/swat
%{_sbindir}/swat
%{_mandir}/man8/swat.8*
#%{_mandir}/ja/man8/swat.8*
%attr(755,root,root) %{_libdir}/samba/*.msg

%files client
%defattr(-,root,root)
%{_libdir}/samba/lowcase.dat
%{_libdir}/samba/upcase.dat
%{_libdir}/samba/valid.dat
%{_bindir}/rpcclient
%{_bindir}/findsmb
%{_mandir}/man8/smbmnt.8*
%{_mandir}/man8/smbmount.8*
%{_mandir}/man8/smbumount.8*
%{_mandir}/man8/smbspool.8*
%{_bindir}/nmblookup
%{_bindir}/smbclient
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_bindir}/net
%{_bindir}/smbtree
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man8/net.8*
#%{_mandir}/ja/man1/smbtar.1*
#%{_mandir}/ja/man1/smbclient.1*
#%{_mandir}/ja/man1/nmblookup.1*

%files common
%defattr(-,root,root)
%{_libdir}/libsmbclient.a
%{_includedir}/libsmbclient.h
%{_bindir}/testparm
%{_bindir}/testprns
%{_bindir}/smbpasswd
%{_bindir}/ntlm_auth
%{_bindir}/pdbedit
%{_bindir}/profiles
%{_bindir}/smbcquotas
%dir /var/cache/samba
%attr(750,root,root) %dir /var/cache/samba/winbindd_privileged
%config(noreplace) /etc/samba/smb.conf
%config(noreplace) /etc/samba/lmhosts
%dir %{_datadir}/samba
%dir %{_datadir}/samba/codepages
%dir /etc/samba
%{_mandir}/man1/ntlm_auth.1*
%{_mandir}/man1/profiles.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/testparm.1*
%{_mandir}/man1/testprns.1*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/lmhosts.5*
%{_mandir}/man8/smbpasswd.8*
%{_mandir}/man1/wbinfo.1*
%{_mandir}/man8/winbindd.8*
%{_mandir}/man1/vfstest.1*

%changelog
* Wed Feb 18 2004 Mark Duckworth <mduckworth@atari-source.com> 3.0.1-1
- Initial port to sparemint with spec creation
