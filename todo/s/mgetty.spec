Summary       : A getty replacement for use with data and fax modems.
Name          : mgetty
Version       : 1.1.22
Release       : 1
Copyright     : distributable
Group         : Applications/Communications

Packager      : Marc-Anton Kehr <m.kehr@ndh.net>
Vendor        : Sparemint
URL           : ftp://ftp.leo.org/pub/comp/os/unix/networking/mgetty/

BuildRequires : groff, tetex, tetex-latex, texinfo, XFree86-devel
Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source:  ftp://ftp.leo.org/pub/comp/os/unix/networking/mgetty/mgetty%{version}-Aug17.tar.gz
Patch1:  mgetty-1.1.14-config.patch
Patch2:  mgetty-1.1.5-makekvg.patch
Patch3:  mgetty-1.1.14-policy.patch
Patch4:  mgetty-1.1.5-strip.patch
Patch5:  mgetty-1.1.14-echo.patch
Patch6:  mgetty-1.1.14-logrotate.patch
Patch7:  mgetty-1.1.9-imakefile.patch
Patch8:  mgetty-1.1.20-docfix.patch
Patch9:  mgetty-1.1.21-faxprint.patch
Patch10: mgetty-pointer.patch
Patch11: mgetty-1.1.21-void.patch
Patch12: mgetty-1.1.21-paths.patch
Patch13: mgetty-1.1.21-root.patch
Patch14: mgetty-1.1.21-ia64.patch
Patch15: mgetty_elsapatch.patch
Patch16: mgetty-1.1.21-giftopnm.patch
Patch17: mgetty-1.1.22-excl.patch
Patch18: mgetty-1.1.22-mint.patch


%package sendfax
Summary       : Provides support for sending faxes over a modem.
Group         : Applications/Communications
Requires      : mgetty = %{PACKAGE_VERSION}
Requires      : netpbm-progs

%package voice
Summary       : A program for using your modem and mgetty as an answering machine
Group         : Applications/Communications
Requires      : mgetty = %{PACKAGE_VERSION}

%package viewfax
Summary       : An X Window System fax viewer.
Group         : Applications/Communications
Requires      : XFree86

%description
The mgetty package contains a "smart" getty which allows logins over a
serial line (i.e., through a modem).  If you're using a Class 2 or 2.0
modem, mgetty can receive faxes.  If you also need to send faxes,
you'll need to install the sendfax program.

If you'll be dialing in to your system using a modem, you should
install the mgetty package.  If you'd like to send faxes using mgetty
and your modem, you'll need to install the mgetty-sendfax program.  If
you need a viewer for faxes, you'll also need to install the
mgetty-viewfax package.

%description sendfax
Sendfax is a standalone backend program for sending fax files.  The
mgetty program (a getty replacement for handling logins over a serial
line) plus sendfax will allow you to send faxes through a Class 2
modem.

If you'd like to send faxes over a Class 2 modem, you'll need to
install the mgetty-sendfax and the mgetty packages.

%description voice
The mgetty-voice package contains the vgetty system, which enables
mgetty and your modem to support voice capabilities.  In simple terms,
vgetty lets your modem act as an answering machine.  How well the
system will work depends upon your modem, which may or may not be able
to handle this kind of implementation.

Install mgetty-voice along with mgetty if you'd like to try having
your modem act as an answering machine.

%description viewfax
Viewfax displays the fax files received using mgetty in an X11 window.
Viewfax is capable of zooming in and out on the displayed fax.

If you're installing the mgetty-viewfax package, you'll also need to
install mgetty.


%prep
%setup -q
%patch1 -p1 -b .config
%patch2 -p1 -b .makekvg
%patch3 -p1 -b .policy
%patch4 -p1 -b .strip
%patch5 -p1 -b .echo
%patch6 -p1
%patch7 -p1
# new texinfo is much stricter about xrefs
#%patch8 -p1 -b .docfix
%patch9 -p1 -b .faxprint
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1 -b .elsa
%patch16 -p1 -b .giftopnm
%patch17 -p1 -b .excl
%patch18 -p1


%build
cp policy.h-dist policy.h
make "RPM_OPT_FLAGS=$RPM_OPT_FLAGS -DUSE_POLL" CONFDIR=/etc/mgetty+sendfax

pushd voice
make CFLAGS="$RPM_OPT_FLAGS" CONFDIR=/etc/mgetty+sendfax
popd

pushd frontends/X11/viewfax-2.4
xmkmf
make depend
make CDEBUGFLAGS="$RPM_OPT_FLAGS" CONFDIR=/etc/mgetty+sendfax
popd


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/info
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/mgetty+sendfax
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man
mkdir -p ${RPM_BUILD_ROOT}/sbin
mkdir -p ${RPM_BUILD_ROOT}/var/spool

instflags="
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	spool=${RPM_BUILD_ROOT}/var/spool \
	BINDIR=${RPM_BUILD_ROOT}%{_prefix}/bin \
	SBINDIR=${RPM_BUILD_ROOT}%{_prefix}/sbin \
	LIBDIR=${RPM_BUILD_ROOT}%{_prefix}/lib/mgetty+sendfax \
	CONFDIR=${RPM_BUILD_ROOT}/etc/mgetty+sendfax \
	MAN1DIR=${RPM_BUILD_ROOT}%{_prefix}/share/man/man1 \
	MAN4DIR=${RPM_BUILD_ROOT}%{_prefix}/share/man/man4 \
	MAN5DIR=${RPM_BUILD_ROOT}%{_prefix}/share/man/man5 \
	MAN8DIR=${RPM_BUILD_ROOT}%{_prefix}/share/man/man8 \
	INFODIR=${RPM_BUILD_ROOT}%{_prefix}/info \
	INSTALL=%{__install}"
make install ${instflags}
install -m700 callback/callback ${RPM_BUILD_ROOT}/%{_prefix}/sbin
install -m4711 callback/ct ${RPM_BUILD_ROOT}%{_prefix}/bin

# compress info files
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*

mv ${RPM_BUILD_ROOT}%{_prefix}/sbin/mgetty ${RPM_BUILD_ROOT}/sbin

# this conflicts with efax
mv ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/fax.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/mgetty_fax.1

# voice mail extensions
mkdir -p ${RPM_BUILD_ROOT}/var/spool/voice/{messages,incoming}
make -C voice install ${instflags}
mv ${RPM_BUILD_ROOT}%{_prefix}/sbin/vgetty ${RPM_BUILD_ROOT}/sbin
install -m 600 -c voice/voice.conf-dist ${RPM_BUILD_ROOT}/etc/mgetty+sendfax/voice.conf

make -C frontends/X11/viewfax-2.4 install DESTDIR=${RPM_BUILD_ROOT}
make -C frontends/X11/viewfax-2.4 install.man DESTDIR=${RPM_BUILD_ROOT} MANDIR=%{_prefix}/share/man/man1

# install logrotate control files
mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 0644 logrotate.mgetty ${RPM_BUILD_ROOT}/etc/logrotate.d/mgetty
install -m 0644 logrotate.sendfax ${RPM_BUILD_ROOT}/etc/logrotate.d/sendfax

# forcibly strip all binaries
strip ${RPM_BUILD_ROOT}{%{_prefix}/bin,%{_prefix}/sbin,/sbin}/* || :

# compress all manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:

# rename symbolic links
( cd ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1;
  for file in *.1; do \
    echo "processing $file ..."; \
    target=`readlink $file`; \
    ln -s $target.gz $file.gz; \
    rm $file; \
  done
)

# don't ship documentation that is executable...
find samples -type f -exec chmod 644 {} \;
chmod 644 ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/mgetty.info.gz %{_prefix}/info/dir --entry="* mgetty: (mgetty).		Package to handle faxes, voicemail and more."

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/mgetty.info.gz %{_prefix}/info/dir --entry="* mgetty: (mgetty). 	Package to handle faxes, voicemail and more."
fi


%files
%defattr(-,root,root)
%doc BUGS ChangeLog README.1st THANKS doc/modems.db samples 
%doc doc/mgetty.ps doc/*.txt
%dir /etc/mgetty+sendfax
%config /etc/mgetty+sendfax/login.config
%config /etc/mgetty+sendfax/mgetty.config
%config /etc/mgetty+sendfax/dialin.config
%config /etc/logrotate.d/mgetty
/sbin/mgetty
%{_prefix}/info/mgetty.info-1.gz
%{_prefix}/info/mgetty.info-2.gz
%{_prefix}/info/mgetty.info-3.gz
%{_prefix}/info/mgetty.info-4.gz
%{_prefix}/info/mgetty.info.gz
%{_prefix}/sbin/callback
%{_prefix}/share/man/man4/mgettydefs.4*
%{_prefix}/share/man/man8/callback.8*
%{_prefix}/share/man/man8/mgetty.8*

%files sendfax
%defattr(-,root,root)
%config /etc/mgetty+sendfax/sendfax.config
%config /etc/mgetty+sendfax/faxrunq.config
%config /etc/mgetty+sendfax/faxheader
%config /etc/logrotate.d/sendfax
%dir /var/spool/fax
%dir /var/spool/fax/incoming
%dir /var/spool/fax/outgoing
%dir /var/spool/fax/outgoing/locks
%{_prefix}/bin/kvg
%{_prefix}/bin/newslock
%{_prefix}/bin/g3cat
%{_prefix}/bin/g32pbm
%{_prefix}/bin/pbm2g3
%{_prefix}/bin/faxspool
%{_prefix}/bin/faxrunq
%{_prefix}/bin/faxq
%{_prefix}/bin/faxrm
%attr(0755,root,root) %{_prefix}/bin/ct
%{_prefix}/sbin/sendfax
%{_prefix}/sbin/faxrunqd
%dir %{_prefix}/lib/mgetty+sendfax
%{_prefix}/lib/mgetty+sendfax/cour25.pbm
%{_prefix}/lib/mgetty+sendfax/cour25n.pbm
%{_prefix}/share/man/man1/g32pbm.1*
%{_prefix}/share/man/man1/pbm2g3.1*
%{_prefix}/share/man/man1/g3cat.1*
%{_prefix}/share/man/man1/mgetty_fax.1*
%{_prefix}/share/man/man1/faxspool.1*
%{_prefix}/share/man/man1/faxrunq.1*
%{_prefix}/share/man/man1/faxq.1*
%{_prefix}/share/man/man1/faxrm.1*
%{_prefix}/share/man/man1/coverpg.1*
%{_prefix}/share/man/man5/faxqueue.5*
%{_prefix}/share/man/man8/faxrunqd.8*
%{_prefix}/share/man/man8/sendfax.8*

%files voice
%defattr(-,root,root)
%config /etc/mgetty+sendfax/voice.conf
%dir /var/spool/voice
%dir /var/spool/voice/incoming
%dir /var/spool/voice/messages
/sbin/vgetty
%{_prefix}/bin/autopvf
%{_prefix}/bin/basictopvf
%{_prefix}/bin/lintopvf
%{_prefix}/bin/pvfamp
%{_prefix}/bin/pvfcut
%{_prefix}/bin/pvfecho
%{_prefix}/bin/pvffft
%{_prefix}/bin/pvffile
%{_prefix}/bin/pvfmix
%{_prefix}/bin/pvfreverse
%{_prefix}/bin/pvfsine
%{_prefix}/bin/pvfspeed
%{_prefix}/bin/pvftoau
%{_prefix}/bin/pvftobasic
%{_prefix}/bin/pvftolin
%{_prefix}/bin/pvftormd
%{_prefix}/bin/pvftovoc
%{_prefix}/bin/pvftowav
%{_prefix}/bin/rmdfile
%{_prefix}/bin/rmdtopvf
%{_prefix}/bin/vm
%{_prefix}/bin/voctopvf
%{_prefix}/bin/wavtopvf
%{_prefix}/share/man/man1/autopvf.1*
%{_prefix}/share/man/man1/basictopvf.1*
%{_prefix}/share/man/man1/lintopvf.1*
%{_prefix}/share/man/man1/pvf.1*
%{_prefix}/share/man/man1/pvfamp.1*
%{_prefix}/share/man/man1/pvfcut.1*
%{_prefix}/share/man/man1/pvfecho.1*
%{_prefix}/share/man/man1/pvffft.1*
%{_prefix}/share/man/man1/pvffile.1*
%{_prefix}/share/man/man1/pvfmix.1*
%{_prefix}/share/man/man1/pvfreverse.1*
%{_prefix}/share/man/man1/pvfsine.1*
%{_prefix}/share/man/man1/pvfspeed.1*
%{_prefix}/share/man/man1/pvftoau.1*
%{_prefix}/share/man/man1/pvftobasic.1*
%{_prefix}/share/man/man1/pvftolin.1*
%{_prefix}/share/man/man1/pvftormd.1*
%{_prefix}/share/man/man1/pvftovoc.1*
%{_prefix}/share/man/man1/pvftowav.1*
%{_prefix}/share/man/man1/rmdfile.1*
%{_prefix}/share/man/man1/rmdtopvf.1*
%{_prefix}/share/man/man1/voctopvf.1*
%{_prefix}/share/man/man1/wavtopvf.1*
%{_prefix}/share/man/man1/zplay.1*

%files viewfax
%defattr(-,root,root)
%doc frontends/X11/viewfax-2.4/C* frontends/X11/viewfax-2.4/README
%{_prefix}/bin/viewfax
%dir %{_prefix}/lib/mgetty+sendfax
%{_prefix}/lib/mgetty+sendfax/viewfax.tif
%{_prefix}/share/man/man1/viewfax.1x*


%changelog
* Thu Jan 09 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.1.22
- integrated all Redhat 7.0 patches
- patched to compile with current MiNTLib
- added built of X11 faxviewer package
