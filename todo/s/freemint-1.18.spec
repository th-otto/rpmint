Summary       : The FreeMiNT kernel
Name          : freemint
Version       : 1.18.0
Release       : 1
License       : MiNT license, GPL, LGPL
Group         : Base System/Kernel

Packager      : Marc-Anton Kehr <makehr@ndh.net>
Vendor        : Sparemint
URL           : http://sparemint.atariforge.net/

BuildRequires : mintlib-devel >= 0.57
BuildRequires : bash gcc make bison flex mintbin binutils sed
BuildRequires : sh-utils fileutils

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: http://sparemint.atariforge.net/pub/sparemint/mint/kernel/%{version}/%{name}-%{version}-src.tar.gz
Patch0: freemint-1.18.0-CONFIGVARS.patch

%package net
Summary       : The FreeMiNT TCP/IP stack (MiNTNet)
Group         : Base System/Kernel
Requires      : %{name} = %{version}
Obsoletes     : mintnet
Conflicts     : mintnet

%package sbin
Summary       : The FreeMiNT system tools
Group         : Base System/Kernel
Requires      : %{name} = %{version}

%package gem
Summary       : The FreeMiNT GEM system tools
Group         : Base System/Kernel
Requires      : %{name} = %{version}

%package xaaes
Summary	      : The Freemint AES (XaAES)
Group	      : Base System/Kernel
Requires      : %{name} = %{version}


%description
This is the FreeMiNT kernel and all official supported modules.

%description net
This is the networking package for FreeMiNT also known as MiNTNet.

%description sbin
This package includes the system tools for runtime configuration and
maintaining the system.

It also include the GlueSTiK and MGW gateway to MiNTNet.

%description gem
This package includes the GEM system tools for FreeMiNT, namely
TosWin2 and the FSetter configuration utility.

%description xaaes
This package includes a full AES replacement for FreeMiNT.

%prep
%setup -q


%build
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/boot/kernel
mkdir -p ${RPM_BUILD_ROOT}/boot/modules/net
mkdir -p ${RPM_BUILD_ROOT}/boot/xaaes/widgets
mkdir -p ${RPM_BUILD_ROOT}/boot/xaaes/img/8b
mkdir -p ${RPM_BUILD_ROOT}/boot/xaaes/img/hc
mkdir -p ${RPM_BUILD_ROOT}/opt/cops
mkdir -p ${RPM_BUILD_ROOT}/opt/toswin2
mkdir -p ${RPM_BUILD_ROOT}/opt/fsetter
mkdir -p ${RPM_BUILD_ROOT}/opt/hypview
mkdir -p ${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/mktbl/keyboards
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man2
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man5
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man8

# kernel
install -m 755 sys/.compile_000/mint000.prg      ${RPM_BUILD_ROOT}/boot/kernel/
install -m 755 sys/.compile_020/mint020.prg      ${RPM_BUILD_ROOT}/boot/kernel/
install -m 755 sys/.compile_030/mint030.prg      ${RPM_BUILD_ROOT}/boot/kernel/
install -m 755 sys/.compile_040/mint040.prg      ${RPM_BUILD_ROOT}/boot/kernel/
install -m 755 sys/.compile_mil/mintmil.prg      ${RPM_BUILD_ROOT}/boot/kernel/
install -m 755 sys/.compile_ara/mintara.prg	 ${RPM_BUILD_ROOT}/boot/kernel/
install -m 755 sys/.compile_col/mintv4e.prg      ${RPM_BUILD_ROOT}/boot/kernel/

# sockets
install -m 755 sys/sockets/inet4.xdd		 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/sockets/xif/biodma.xif        ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/de600.xif         ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/dial.xif          ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/lance.xif         ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/pamsdma.xif       ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/plip.xif          ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rieblmst.xif      ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rieblmst_fast.xif ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rieblspc.xif      ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rieblspc_fast.xif ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rieblste.xif      ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/riebltt.xif       ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rtl8012.xif       ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/rtl8012st.xif     ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/slip.xif          ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/nfeth/nfeth.xif	 ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/ethernat/ethernat.xif	 ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/fec/fec.xif	 ${RPM_BUILD_ROOT}/boot/modules/net/
install -m 755 sys/sockets/xif/daynaport/scsilink.xif	 ${RPM_BUILD_ROOT}/boot/modules/net/


# xdd
install -m 755 sys/xdd/audio/audiodev.xdd        ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/dsp56k/dsp56k.xdd	 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/flop-raw/flop_raw.xdd     ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/lp/lp.xdd		 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/mfp/mfp.xdd               ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/mfp/mfp_mil.xdd           ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/scc/scc.xdd               ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/uart/uart.xdd             ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/nfstderr/nfstderr.xdd	 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xdd/xconout2/xconout2.xdd     ${RPM_BUILD_ROOT}/boot/modules/


# xfs
install -m 755 sys/xfs/aranym/aranym.xfs	 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xfs/hostfs/hostfs.xfs	 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xfs/ext2fs/ext2.xfs           ${RPM_BUILD_ROOT}/boot/modules/
#install -m 755 sys/xfs/isofs/isofs.xfs		 ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xfs/minixfs/minix.xfs         ${RPM_BUILD_ROOT}/boot/modules/
install -m 755 sys/xfs/nfs/nfs.xfs               ${RPM_BUILD_ROOT}/boot/modules/

# IO
install -m 644 tools/IO/libIO.a 		 ${RPM_BUILD_ROOT}/%{_prefix}/lib/

# cops
install -m 755 tools/cops/cops.app  		 ${RPM_BUILD_ROOT}/opt/cops/
install -m 755 tools/cops/cops_de.app		 ${RPM_BUILD_ROOT}/opt/cops/	
install -m 755 tools/cops/cops_fr.app		 ${RPM_BUILD_ROOT}/opt/cops/

# crypto
install -m 755 tools/crypto/crypto 		 ${RPM_BUILD_ROOT}/%{_prefix}/sbin/

# fdisk
install -m 755 tools/fdisk/fdisk 		 ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/fdisk/sfdisk 		 ${RPM_BUILD_ROOT}/sbin/

install -m 644 tools/fdisk/sfdisk.8 		 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man8/

# fsetter
install -m 755 tools/fsetter/fsetter.app 	 ${RPM_BUILD_ROOT}/opt/fsetter/
install -m 644 tools/fsetter/fsetter.hrd 	 ${RPM_BUILD_ROOT}/opt/fsetter/
install -m 644 tools/fsetter/fsetter.rsc 	 ${RPM_BUILD_ROOT}/opt/fsetter/
install -m 644 tools/fsetter/fsetter_e.rsc 	 ${RPM_BUILD_ROOT}/opt/fsetter/

# gluestik
install -m 755 tools/gluestik/gluestik.prg 	 ${RPM_BUILD_ROOT}%{_prefix}/sbin/gluestik

# hypview
install -m 755 tools/hypview/hyp_view.app 	 ${RPM_BUILD_ROOT}/opt/hypview/
install -m 644 tools/hypview/hyp_view.hrd 	 ${RPM_BUILD_ROOT}/opt/hypview/
install -m 644 tools/hypview/hyp_view.rsc 	 ${RPM_BUILD_ROOT}/opt/hypview/
install -m 644 tools/hypview/hyp_view.cfg 	 ${RPM_BUILD_ROOT}/opt/hypview/

# lpflush
install -m 755 tools/lpflush/lpflush 		 ${RPM_BUILD_ROOT}/sbin

install -m 644 tools/lpflush/lpflush.1 		 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man1/

# mgw
install -m 755 tools/mgw/mgw.prg 		 ${RPM_BUILD_ROOT}%{_prefix}/sbin/mgw

# minix
install -m 755 tools/minix/fsck/fsck.minix 	 ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/minix/minit/minit 		 ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/minix/tools/flist 		 ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/minix/tools/mfsconf 	 ${RPM_BUILD_ROOT}/sbin/

# mkfatfs
install -m 755 tools/mkfatfs/mkfatfs 		 ${RPM_BUILD_ROOT}/sbin/

# mktbl
install -m 755 tools/mktbl/mktbl		 ${RPM_BUILD_ROOT}/sbin/
install -m 644 tools/mktbl/keyboards/british.src ${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/british-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/french.src	 ${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/french-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/german.src	 ${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/german-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/italian.src ${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/italian-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/spanish.src ${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/spanish-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/swiss_french.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/swiss_french-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/swiss_german.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/swiss_german-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/
install -m 644 tools/mktbl/keyboards/usa-pl.src	${RPM_BUILD_ROOT}/usr/share/mktbl/keyboards/

# net-tools
install -m 755 tools/net-tools/arp ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/diald ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/ifconfig ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/iflink ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/ifstats ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/masqconf ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/netstat ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/pppconf ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/route ${RPM_BUILD_ROOT}/sbin/
install -m 755 tools/net-tools/slattach ${RPM_BUILD_ROOT}/sbin/

install -m 644 tools/net-tools/ifconfig.8 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man8/
install -m 644 tools/net-tools/netstat.8 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man8/
install -m 644 tools/net-tools/route.8 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man8/

# nfs
install -m 755 tools/nfs/mount_nfs ${RPM_BUILD_ROOT}/sbin/

install -m 644 tools/nfs/mount.8 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man8/
install -m 644 tools/nfs/mtab.5 ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man5/

# strace
#install -m 755 tools/strace/strace ${RPM_BUILD_ROOT}/sbin/

# swkbdtbl
#install -m 755 tools/swkbdtbl/swkbdtbl ${RPM_BUILD_ROOT}/sbin/
	
# sysctl
install -m 755 tools/sysctl/sysctl ${RPM_BUILD_ROOT}/sbin/

# toswin2
install -m 755 tools/toswin2/toswin2.app ${RPM_BUILD_ROOT}/opt/toswin2/
install -m 644 tools/toswin2/toswin2.rsc ${RPM_BUILD_ROOT}/opt/toswin2/
install -m 644 tools/toswin2/toswin2.hrd ${RPM_BUILD_ROOT}/opt/toswin2/
install -m 644 tools/toswin2/tw-call/tw-call.app ${RPM_BUILD_ROOT}/opt/toswin2/


# wikitools
install -m 744 tools/wikitools/getxml.sh	${RPM_BUILD_ROOT}/sbin/
install -m 744 tools/wikitools/makenodes	${RPM_BUILD_ROOT}/sbin/
install -m 744 tools/wikitools/u2w		${RPM_BUILD_ROOT}/sbin/
install -m 744 tools/wikitools/w2u		${RPM_BUILD_ROOT}/sbin/


# xaaes
install -m 755 xaaes/src.km/xaloader/xaloader.prg ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaesst.km 		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaes000.km		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaes030.km		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaes040.km		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaes060.km		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaesdeb.km		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/xaaesv4e.km		  ${RPM_BUILD_ROOT}/boot/xaaes
#install -m 644 xaaes/src.km/xaaes.cnf		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 644 xaaes/src.km/xaaes016.rsc	  ${RPM_BUILD_ROOT}/boot/xaaes
#install -m 644 xaaes/src.km/xa_mono.rsc		  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 644 xaaes/src.km/xa_xtobj.rsc	  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/adi/whlmoose/moose.adi  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 755 xaaes/src.km/adi/whlmoose/moose_w.adi  ${RPM_BUILD_ROOT}/boot/xaaes
install -m 644 xaaes/src.km/img/8b/*.img	  ${RPM_BUILD_ROOT}/boot/xaaes/img/8b
install -m 644 xaaes/src.km/img/hc/*.img	  ${RPM_BUILD_ROOT}/boot/xaaes/img/hc
install -m 644 xaaes/src.km/widgets/*.hrd	  ${RPM_BUILD_ROOT}/boot/xaaes/widgets
install -m 644 xaaes/src.km/widgets/*.rsc	  ${RPM_BUILD_ROOT}/boot/xaaes/widgets

# strip down anything
find ${RPM_BUILD_ROOT} -perm 755 -type f | xargs strip

# manpages
(for i in doc/programmer/man/man2/*.2;
 do
  install -m 644 $i ${RPM_BUILD_ROOT}/%{_prefix}/share/man/man2/
 done
)

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc BUGS COPYING* ChangeLog* HACKING README doc
/boot/kernel/*
/boot/modules/ext2.xfs
/boot/modules/minix.xfs
/boot/modules/nfs.xfs
/boot/modules/audiodev.xdd
/boot/modules/flop_raw.xdd
/boot/modules/mfp.xdd
/boot/modules/mfp_mil.xdd
/boot/modules/scc.xdd
/boot/modules/uart.xdd
/boot/modules/xconout2.xdd
%{_prefix}/share/man/man2/*

%files net
%defattr(-,root,root)
/boot/modules/inet4.xdd
/boot/modules/net/*.xif

/sbin/arp
/sbin/diald
/sbin/ifconfig
/sbin/iflink
/sbin/ifstats
/sbin/masqconf
/sbin/netstat
/sbin/pppconf
/sbin/route
/sbin/slattach
%{_prefix}/share/man/man8/ifconfig*
%{_prefix}/share/man/man8/netstat*
%{_prefix}/share/man/man8/route*

/sbin/mount_nfs
%{_prefix}/share/man/man8/mount*
%{_prefix}/share/man/man5/mtab*

%files sbin
%defattr(-,root,root)
/sbin/fdisk
/sbin/sfdisk
%{_prefix}/share/man/man8/sfdisk*
/sbin/fsck.minix
/sbin/minit
/sbin/flist
/sbin/mfsconf
/sbin/mkfatfs
/sbin/mktbl
#/sbin/strace
#/sbin/swkbdtbl
/sbin/sysctl
/sbin/getxml.sh
/sbin/makenodes
/sbin/u2w
/sbin/w2u
/sbin/lpflush
%{_prefix}/sbin/crypto
%{_prefix}/sbin/gluestik
%{_prefix}/sbin/mgw
%{_prefix}/share/man/man1/lpflush*


%files gem
%defattr(-,root,root)
/opt/toswin2
/opt/fsetter
/opt/cops
/opt/hypview

%files xaaes
%defattr(-,root,root)
/boot/xaaes/xaloader.prg
/boot/xaaes/*.km
#/boot/xaaes/xaaes.cnf
/boot/xaaes/*.rsc
/boot/xaaes/*.adi
/boot/xaaes/img/8b/*
/boot/xaaes/img/hc/*
/boot/xaaes/widgets/*.rsc
/boot/xaaes/widgets/*.hrd

%changelog
* Wed Apr 03 2013 Marc-Anton Kehr <makehr@ndh.net>
- version 1.18 release
* Thu Jan 31 2013 Marc-Anton Kehr <makehr@ndh.net>
- version 1.17 release
* Thu Jul 26 2007 Marc-Anton Kehr <makehr@ndh.net>
- first release for Sparemint
