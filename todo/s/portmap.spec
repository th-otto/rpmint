Summary       : A program which manages RPC connections.
Name          : portmap
Version       : 4.0
Release       : 4
Copyright     : BSD
Group         : System Environment/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint

Prereq        : /sbin/chkconfig netbase
BuildRequires : mintlib-devel >= 0.57.1

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://coast.cs.purdue.edu/pub/tools/unix/portmap/portmap_4.tar.gz
Source1: portmap.init
Source2: pmap_set.8
Source3: pmap_dump.8
Source4: portmap.8
Patch0: portmap-4.0-linux.patch
Patch1: portmap-malloc.patch
Patch2: portmap-4.0-cleanup.patch
Patch3: portmap-4.0-rpc_user.patch
Patch4: portmap-4.0-sigpipe.patch
Patch5: portmap-4.0-mint.patch


%description
The portmapper program is a security tool which prevents theft of NIS
(YP), NFS and other sensitive information via the portmapper.  A
portmapper manages RPC connections, which are used by protocols like
NFS and NIS.

The portmap package should be installed on any machine which acts as a
server for protocols using RPC.


%prep 
%setup -q -n portmap_4
%patch0 -p1 -b .linux
%patch1 -p1 -b .malloc
%patch2 -p1 -b .cleanup
%patch3 -p1 -b .rpcuser
%patch4 -p1 -b .sigpipe
%patch5 -p1 -b .mint


%build
make \
	FACILITY=LOG_AUTH \
	ZOMBIES="-DIGNORE_SIGCHLD -Dlint" \
	AUX="" \
	LIBS="-lsocket -liio" \
	RPM_OPT_FLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 portmap ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 pmap_set ${RPM_BUILD_ROOT}%{_prefix}/sbin
install -m 755 pmap_dump ${RPM_BUILD_ROOT}%{_prefix}/sbin

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m 755 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/portmap

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8
install -m 444 %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8
install -m 444 %{SOURCE3} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8
install -m 444 %{SOURCE4} ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

# strip binaries
strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/chkconfig --add portmap
/usr/sbin/groupadd -g 32 rpc > /dev/null 2>&1
/usr/sbin/useradd -c "Portmapper RPC user" -d / -g 32 -M -s /bin/false -u 32 rpc > /dev/null 2>&1
exit 0

%preun
if [ $1 = 0 ] ; then
#  service portmap stop > /dev/null 2>&1
  /sbin/chkconfig --del portmap
fi

%postun
#if [ "$1" -ge "1" ]; then
#  service portmap condrestart > /dev/null 2>&1
#fi


%files
%defattr(-,root,root)
%doc README CHANGES BLURB
%config	/etc/rc.d/init.d/portmap
%{_prefix}/sbin/portmap
%{_prefix}/sbin/pmap_dump
%{_prefix}/sbin/pmap_set
%{_prefix}/share/man/man8/*


%changelog
* Wed Sep 26 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
