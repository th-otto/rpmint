Summary       : NFS server daemons
Summary(de)   : NFS-Server-Dämonen
Name          : nfs-server
Version       : 2.2beta47
Release       : 2
Copyright     : GPL
Group         : Networking/Daemons

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://linux.mathematik.tu-darmstadt.de/pub/linux/people/okir/

Requires      : /sbin/chkconfig portmap

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source0: ftp://linux.mathematik.tu-darmstadt.de/pub/linux/people/okir/nfs-server-%{version}.tar.gz
Source1: nfs.init
Source2: exportfs
Patch0: nfs-server-2.2beta36-redhat.patch
Patch1: nfs-server-2.2beta37-sigpwr.patch
Patch2: nfs-server-2.2beta47-mint.patch
Patch3: nfs-server-2.2beta47-getmnthack.patch


%description
The NFS and mount daemons are used to create an NFS server which
can export filesystems to other machines.  This package is not
needed to mount NFS filesystems -- that functionality is already
in the FreeMiNT kernel (by the nfs.xfs).

%description -l de
Die NFS- und Mount-Dämonen werden zum Erstellen eines NFS-Servers 
benutzt, der Dateisysteme auf andere Computer exportieren kann. 
Dieses Paket wird zum Montieren von NFS-Dateisysteme nicht benötigt, 
da es sich um eine Funktion handelt, die bereits im FreeMiNT-Kernel  
eingebaut ist (mittels des nfs.xfs).


%prep
%setup -q
%patch0 -p1 -b .redhat
%patch1 -p1 -b .sigpwr
%patch2 -p1 -b .mint
%patch3 -p1 -b .mint


%build
echo | ./BUILD --hosts-access=yes --libwrap-directory=%{_prefix}/lib \
	--exports-uid=0 --exports-gid=0 --log-mounts=yes \
	--ugidd=no --multi=no
make CFLAGS="${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	man5dir=${RPM_BUILD_ROOT}%{_prefix}/share/man/man5 \
	man8dir=${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -m755 -o 0 -g 0 %{SOURCE1} ${RPM_BUILD_ROOT}/etc/rc.d/init.d/nfs
install -m755 -o 0 -g 0 %{SOURCE2} ${RPM_BUILD_ROOT}%{_prefix}/sbin/exportfs

strip ${RPM_BUILD_ROOT}%{_prefix}/sbin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:

# fix symlinks
( cd ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8;
  for file in *.8; do \
    echo "processing $file ..."; \
    target=`readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/chkconfig --add nfs

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del nfs
fi


%files
%doc NEWS README
%config /etc/rc.d/init.d/nfs
%{_prefix}/sbin/*
%{_prefix}/share/man/man*/*


%changelog
* Sun Feb 01 2004 Jan Krupka <jkrupka@volny.cz>
- bugs in init script removed, recompiled against mintlib-0.57.4
* Fri Sep 28 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
