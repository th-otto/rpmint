Summary       : A network traffic monitoring tool.
Name          : tcpdump
Version       : 3.6.2
Release       : 2
Copyright     : BSD
Group         : Applications/Internet

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.tcpdump.org/

Requires      : freemint-net netbase

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://www.tcpdump.org/release/tcpdump-3.6.2.tar.gz
Source1: http://www.tcpdump.org/release/libpcap-0.6.2.tar.gz
Source2: ftp://ftp.ee.lbl.gov/arpwatch-2.1a11.tar.gz
Source3: arpwatch.init
Source4: tcpslice-CVS.20010207.tar.gz
Source5: arpwatch.sysconfig
Source6: arpwatch-ethercodes.dat
Patch0:  libpcap-0.4-mint.patch
Patch1:  libpcap-0.6.2-mint.patch
Patch5:  tcpdump-3.6.2-tcpslice-time.patch
Patch6:  tcpdump-3.6.2-usageman.patch
Patch7:  tcpdump-3.6.2-redhat.patch
Patch8:  tcpdump-3.6.1-droproot2.patch 
Patch9:  tcpdump-3.6.1-smb-quiet.patch
Patch10: tcpdump-3.6.1-portnumbers.patch
Patch12: tcpdump-3.6.2-afsprinting.patch
Patch34: arpwatch-2.1a4-fhs.patch
Patch35: arpwatch-2.1a10-man.patch
Patch38: arpwatch-drop.patch
Patch39: arpwatch-drop-man.patch


%description
Tcpdump is a command-line tool for monitoring network traffic.
Tcpdump can capture and display the packet headers on a particular
network interface or on all interfaces. Tcpdump can display all of the
packet headers, or just the ones that match particular criteria.

%package -n libpcap
Version       : 0.6.2
Summary       : A system-independent interface for user-level packet capture.
Group         : Development/Libraries

%description -n libpcap
Libpcap provides a portable framework for low-level network
monitoring. Libpcap can provide network statistics collection,
security monitoring and network debugging. Since almost every system
vendor provides a different interface for packet capture, the libpcap
authors created this system-independent API to ease in porting and to
alleviate the need for several system-dependent packet capture modules
in each application.

Install libpcap if you need to do low-level network traffic monitoring
on your network.

%package -n arpwatch
Version       : 2.1a11
Summary       : Network monitoring tools for tracking IP addresses on a network.
Group         : Applications/System
Prereq        : /sbin/chkconfig
#Prereq        : /sbin/service

%description -n arpwatch
The arpwatch package contains arpwatch and arpsnmp. Arpwatch and
arpsnmp are both network monitoring tools. Both utilities monitor
Ethernet or FDDI network traffic and build databases of Ethernet/IP
address pairs, and can report certain changes via email.

Install the arpwatch package if you need networking monitoring devices
which will automatically keep track of the IP addresses on your
network.


%define PCAP_UID 77
%define PCAP_GID 77
%define	tcpdump_dir	tcpdump-3.6.2
%define tcpslice_dir	tcpslice
%define	libpcap_dir	libpcap-0.6.2
%define	arpwatch_dir	arpwatch-2.1a11


%prep
%setup -q -c -a 1 -a 2 -a 4

%patch5 -p1 -b .tcpslicetime
%patch7 -p0 -b .rh

cd %libpcap_dir
%patch0 -p1 -b .mint
%patch1 -p1 -b .mint
autoconf
cd ..

cd %tcpslice_dir
cp /usr/lib/rpm/config.guess .
cp /usr/lib/rpm/config.sub .
aclocal
autoconf
cd ..

cd %tcpdump_dir
%patch6 -p1 -b .usageman
%patch8 -p1 -b .droproot
%patch9 -p1 -b .smb
%patch10 -p1 -b .portnumbers
%patch12 -p1 -b .afsprinting
autoconf
cd ..

cd %arpwatch_dir
%patch34 -p1 -b .fhs
%patch35 -p1 -b .arpsnmpman
%patch38 -p1 -b .droproot
%patch39 -p0 -b .droprootman
chmod u+w ethercodes.dat
cp %{SOURCE6} ethercodes.dat
cp /usr/lib/rpm/config.guess .
cp /usr/lib/rpm/config.sub .
aclocal
autoconf
cd ..


%build

cd %libpcap_dir
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS=-lsocket \
./configure \
	--prefix=%{_prefix}
rm net
make
cd ..

cd %tcpslice_dir
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS=-lsocket \
./configure \
	--prefix=%{_prefix}
make
cd ..

cd %tcpdump_dir
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS=-lsocket \
./configure \
	--prefix=%{_prefix}
make
cd ..

cd %arpwatch_dir
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
LIBS=-lsocket \
./configure \
	--prefix=%{_prefix}
make ARPDIR=/var/arpwatch
cd ..


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man3
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin

cd %libpcap_dir
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/include/pcap/net
make install \
	DESTDIR=${RPM_BUILD_ROOT} \
	mandir=%{_prefix}/share/man \
	includedir=%{_prefix}/include/pcap
cd ..

cd %tcpslice_dir
install -m755 tcpslice ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m644 tcpslice.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/tcpslice.8
cd ..

cd %tcpdump_dir
install -m755 tcpdump ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m644 tcpdump.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8/tcpdump.8
cd ..

cd %arpwatch_dir
make install install-man \
	DESTDIR=${RPM_BUILD_ROOT} \
	MANDEST=%{_prefix}/share/man

mkdir -p ${RPM_BUILD_ROOT}/var/arpwatch
for n in arp2ethers arpfetch massagevendor massagevendor-old; do
	install -m755 $n ${RPM_BUILD_ROOT}/var/arpwatch
done
for n in *.awk *.dat missingcodes.txt; do
	install -m644 $n ${RPM_BUILD_ROOT}/var/arpwatch
done
cd ..

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig
install -c -m755 %{SOURCE3} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/arpwatch
install -c -m644 %{SOURCE5} ${RPM_BUILD_ROOT}/etc/sysconfig/arpwatch

rm -rf ${RPM_BUILD_ROOT}%{_prefix}/include/pcap/net

strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:
stack --fix=80k ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post -n arpwatch
/sbin/chkconfig --add arpwatch
chown pcap.pcap /var/arpwatch

%pre -n arpwatch
/usr/sbin/groupadd -g %{PCAP_GID} pcap  2> /dev/null || :  
/usr/sbin/useradd -u %{PCAP_UID} -g %{PCAP_GID} \
        -s /bin/nologin -M -r -d /var/arpwatch pcap 2> /dev/null || :

%postun -n arpwatch
#if [ "$1" -ge "1" ]; then
#  /sbin/service arpwatch condrestart >/dev/null 2>&1
#fi

%preun -n arpwatch
if [ $1 = 0 ]; then
#  /sbin/service arpwatch stop > /dev/null 2>&1
  /sbin/chkconfig --del arpwatch
fi


%files
%defattr(-,root,root)
%doc %tcpdump_dir/README %tcpdump_dir/CHANGES
%{_prefix}/sbin/tcpdump
%{_prefix}/sbin/tcpslice
%{_prefix}/share/man/man8/tcpslice.8*
%{_prefix}/share/man/man8/tcpdump.8*

%files -n libpcap
%defattr(-,root,root)
%doc %libpcap_dir/README %libpcap_dir/CHANGES
%{_prefix}/include/pcap
%{_prefix}/lib/libpcap.*
%{_prefix}/share/man/man3/pcap.3*

%files -n arpwatch
%defattr(-,root,root)
%doc %arpwatch_dir/README %arpwatch_dir/CHANGES
%{_prefix}/sbin/arpwatch
%{_prefix}/sbin/arpsnmp
%{_prefix}/share/man/man8/arpwatch.8*
%{_prefix}/share/man/man8/arpsnmp.8*
%config	/etc/rc.d/init.d/arpwatch
%config(noreplace) /etc/sysconfig/arpwatch
%defattr(-,pcap,pcap)
%config	/var/arpwatch/arp.dat
%config	/var/arpwatch/ethercodes.dat
%config	/var/arpwatch/missingcodes.txt
/var/arpwatch/*.awk
/var/arpwatch/arp2ethers
/var/arpwatch/arpfetch
/var/arpwatch/massagevendor
/var/arpwatch/massagevendor-old


%changelog
* Fri Sep 28 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
