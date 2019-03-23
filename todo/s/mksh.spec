# norootforbuild

%define _bindir   /bin

Name:             mksh
Version:          40e
Release:          4.1
Summary:          MirBSD Korn Shell
# ISC (strlcpy.c), MirOS (the rest)
License:          MirOS and ISC
Group:            System/Shells
URL:              http://mirbsd.de/%{name}
Source0:          https://www.mirbsd.org/MirOS/dist/mir/%{name}/%{name}-R%{version}.cpio.gz
Source1:          https://www.mirbsd.org/MirOS/dist/hosted/other/prt.mkshrc
# Patch0:         mksh-cvs.diff
Patch1:           mksh-fix.diff
BuildRoot:        %{_tmppath}/%{name}-%{version}-build
%ifnos FreeMiNT
BuildRequires:    gcc glibc-devel util-linux ed
Requires(post):   coreutils grep
Requires(postun): sed
%else
# to be filled in by the SpareMiNT guys
%endif

%description
mksh is the MirBSD enhanced version of the Public Domain Korn
shell (pdksh), a Bourne-compatible shell which is largely si‐
milar to the original AT&T Korn shell; mksh is the only pdksh
derivate currently being actively developed.  It includes bug
fixes and feature improvements, in order to produce a modern,
robust shell good for interactive and especially script use.
mksh has UTF-8 support (in substring operations and the Emacs
editing mode) and, while R40e corresponds to OpenBSD 5.1-cur‐
rent ksh (without GNU bash-like PS1 and fancy character clas‐
ses), adheres to SUSv4 and is much more robust.  The code has
been cleaned up and simplified, bugs fixed, standards compli‐
ance added, and several enhancements (for extended compatibi‐
lity to other modern shells – as well as a couple of its own)
are available. It has sensible defaults as usual with BSD.

Authors:
	Thorsten Glaser <tg@mirbsd.org>

%prep
%setup -q -T -c "%{name}-%{version}"
%__gzip -dc "%{SOURCE0}" | cpio -mid
mv %{name}/* .
rmdir %{name}
# prozent patch0 -p3
%patch1 -p1

%build
docomp() {
  # Prevent build log scanners from picking up mirtoconf output
  sh Build.sh "$@" 2>&1 | sed \
    -e 's!conftest.c:\([0-9]*\(:[0-9]*\)*\): error:!cE(\1) -!g' \
    -e 's!conftest.c:\([0-9]*\(:[0-9]*\)*\): warning:!cW(\1) -!g'
}
echo '=== trying to build with LTO ==='
if CC="%__cc" CFLAGS="%{optflags}" docomp -r -c lto && test -f %{name}; then
  echo '=== done, wonderful ==='
elif test -f Rebuild.sh; then
  # usually when LTO doesn't exist and we failback to -c combine
  echo '=== FAILED because your gcc is broken ==='
  echo
  echo '=== trying to build withOUT -fwhole-program --combine ==='
  sh Rebuild.sh
  echo '=== note: for better optimisation, fix your gcc! ==='
else
  echo '=== FAILED ==='
  echo
  echo '=== trying to build with basic options ==='
  CC="%__cc" CFLAGS="%{optflags}" docomp -r
fi

# run regression test
regresswithscript=true
%ifos FreeMiNT
# mostly because script is part of util-linux
regresswithscript=false
%endif
(set +e; if $regresswithscript; then
  # run with controlling tty faked by script
  :>test.wait
  script -qc './test.sh -v; x=$?; rm -f test.wait; exit $x'
  maxwait=0
  while test -e test.wait; do
    sleep 1
    maxwait=$(expr $maxwait + 1)
    test $maxwait -lt 900 || break
  done
else
  # skip tests needing a controlling tty
  ./test.sh -v -C regress:no-ctty
fi)

%install
%__install -d -m0755 "%{buildroot}%{_bindir}"
%__install -d -m0755 "%{buildroot}%{_mandir}/man1"
%__install -d -m0755 "%{buildroot}/etc/skel"
%__install -c -m0755 %{name} "%{buildroot}%{_bindir}/%{name}"
%__install -c -p -m0644 %{name}.1 "%{buildroot}%{_mandir}/man1/%{name}.1"
%__install -c -p -m0644 dot.mkshrc "%{buildroot}/etc/mkshrc"
%__install -c -p -m0644 "%{SOURCE1}" "%{buildroot}/etc/skel/.mkshrc"

%post
grep -q "^%{_bindir}/%{name}$" "%{_sysconfdir}/shells" 2>/dev/null || \
    echo "%{_bindir}/%{name}" >>"%{_sysconfdir}/shells"

%postun
[ -x "%{_bindir}/%{name}" ] || sed \
    -e 's@^%{_bindir}/%{name}$@POSTUNREMOVE@' \
    -e '/^POSTUNREMOVE$/d' \
    -i "%{_sysconfdir}/shells"

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,root,root,-)
%doc dot.mkshrc
%config /etc/skel/.mkshrc
%config(noreplace) /etc/mkshrc
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Sun Mar 25 2012 Thorsten Glaser <tg@mirbsd.org> 40e-4
- initial SpareMiNT support, with ragnar76
- regression testsuite failures are no longer fatal to the build
* Sun Mar 25 2012 Thorsten Glaser <tg@mirbsd.org> 40e-3
- fix regression: http://article.gmane.org/gmane.os.miros.mksh/19
* Sat Mar 24 2012 Thorsten Glaser <tg@mirbsd.org> 40e-2
- new stable upstream version, ChangeLog: http://mirbsd.de/mksh#r40e
- switch licence field to SPDX, says rpmlint
* Sun Dec 11 2011 Thorsten Glaser <tg@mirbsd.org> 40d-1
- update prt.mkshrc: better ANSI escape handling
- new stable upstream version, ChangeLog: http://mirbsd.de/mksh#r40d
* Tue Nov 22 2011 Thorsten Glaser <tg@mirbsd.org> 40c-1
- update prt.mkshrc from MirBSD CVS (now uses $'...' to
  set the new PS1 instead of containing raw control chars)
- new stable upstream version, ChangeLog: http://mirbsd.de/mksh#r40c
* Wed Aug  3 2011 Thorsten Glaser <tg@mirbsd.org> 40b-3
- update to R40-stable CVS to get minor bugfixes
- catch build errors better
* Sat Jul 16 2011 Thorsten Glaser <tg@mirbsd.org> 40b-2
- fix typo in description (spotted when porting to FreeWRT)
* Sat Jul 16 2011 Thorsten Glaser <tg@mirbsd.org> 40b-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r40b
* Sun Jun 12 2011 Thorsten Glaser <tg@mirbsd.org> 40-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r40
* Sun Jun  5 2011 Thorsten Glaser <tg@mirbsd.org> 39c+20110605-10
- first attempt at Link Time Optimisation
* Sun Jun  5 2011 Thorsten Glaser <tg@mirbsd.org> 39c+20110605-1
- this is mksh R40 Release Candidate 3 – http://mirbsd.de/mksh#clog
* Sat Jun  4 2011 Thorsten Glaser <tg@mirbsd.org> 39c+20110604-1
- update prt.mkshrc from CVS
- catch early build failures better
- this is mksh R40 Release Candidate 2 – http://mirbsd.de/mksh#clog
* Sun May 29 2011 Thorsten Glaser <tg@mirbsd.org> 39c+20110529-1
- update prt.mkshrc from CVS
- this is mksh R40 Release Candidate – http://mirbsd.de/mksh#clog
* Tue Mar 29 2011 Thorsten Glaser <tg@mirbsd.org> 39c+20110329-1
- new upstream snapshot from CVS – http://mirbsd.de/mksh#clog
- drop mentions of setmode.c, which is gone (thus, BSD licence too)
- if build with -c combine fails, retry using Rebuild.sh instead
  of re-running the whole autoconf stuff
- add (if'd out) ability to run the testsuite without ctty, for Fedora
* Mon Feb 14 2011 Thorsten Glaser <tg@mirbsd.org> 39c+20110213-2
- new upstream snapshot from CVS – http://mirbsd.de/mksh#clog
* Fri Jul 23 2010 Thorsten Glaser <tg@mirbsd.org> 39c+20100721-1
- new upstream snapshot from CVS – http://mirbsd.de/mksh#clog
* Thu Jul 15 2010 Thorsten Glaser <tg@mirbsd.org> 39c+20100715-5
- switch to new configuration scheme where /etc/skel/.mkshrc only
  sources /etc/mkshrc by default (idea from Michal Hlavinka); the
  new /etc/skel/.mkshrc file is now only config (replaced on an
  update) but /etc/mkshrc is config(noreplace)
- use postun rule and requisites from Robert Scheck and Michal Hlavinka
- keep, in general, closer to the RHEL/Fedora packages
- upgrade to a stable development snapshot
- remove the now obsolete arc4random.c source file
- optimise the post and postun rules
- take care of rpmlint warnings
* Fri Feb 26 2010 Thorsten Glaser <tg@mirbsd.org> 39c-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r39c
* Fri Feb 12 2010 Thorsten Glaser <tg@mirbsd.org> 39b-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r39b
- new upstream version of arc4random.c (bugfixes; homepage will be
  http://www.mirbsd.org/a4rcontrb.htm in the future); Changes:
  https://www.mirbsd.org/cvs.cgi/contrib/code/Snippets/arc4random.c
* Sat Oct 10 2009 Thorsten Glaser <tg@mirbsd.org> 39-7
- (oops, the patchlevel was bogus)
- RPM apparently executes build commands with “set -e” so we
  need some different code to deal with build failures
* Sat Oct 10 2009 Thorsten Glaser <tg@mirbsd.org> 39-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r39
- new upstream version of arc4random.c (fix more warnings and Win32-only bugs)
- try to use “-combine” but retry without if that fails
* Fri Aug 28 2009 Thorsten Glaser <tg@mirbsd.org> 38c-5
- fix rpmlint warnings
* Fri Aug 28 2009 Thorsten Glaser <tg@mirbsd.org> 38c-4
- install dot.mkshrc as /etc/skel/.mkshrc like in all other distros
- install the docfile dot.mkshrc gzip'd
* Sun May 31 2009 Thorsten Glaser <tg@mirbsd.org> 38c-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r38c
* Sun May 31 2009 Thorsten Glaser <tg@mirbsd.org> 38b-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r38b
* Wed May 27 2009 Thorsten Glaser <tg@mirbsd.org> 38-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r38
- new upstream version of arc4random.c (some gcc-snapshot warnings fixed)
* Thu Apr  9 2009 Thorsten Glaser <tg@mirbsd.org> 37c-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r37c
- note that https://bugs.launchpad.net/ubuntu/+source/gcc-defaults/+bug/352475
  contains details regarding the gcc bug leading to 37b-2 creation
* Sun Apr  5 2009 Thorsten Glaser <tg@mirbsd.org> 37b-2
- revert use of ‘-combine’ due to gcc bugs (again… *sigh*)
* Sun Apr  5 2009 Thorsten Glaser <tg@mirbsd.org> 37b-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r37b
- use ‘-combine’ option instead of parallel make for better optimisation
- note: The MirOS Licence is now OSI approved
* Sat Dec 13 2008 Thorsten Glaser <tg@mirbsd.org> 36b-1
- new upstream version of mksh, ChangeLog: http://mirbsd.de/mksh#r36b
- new upstream version of arc4random.c
* Sat Oct 25 2008 Thorsten Glaser <tg@mirbsd.org> 36-7
- new upstream version of mksh
- new upstream version of arc4random.c
- simplify build scripts
- debug packages are handled via OBS injection
- do not use unportable pushd, popd, install -D
- remove -Q from Build.sh options as it no longer exists
- by suggestion of Robert Scheck (Fedora), use _sysconfdir,
  _bindir, add post-uninstall
* Sat Apr 12 2008 Pascal Bleser <guru@unixtech.be>
- new upstream version
* Thu Apr  3 2008 - guru@unixtech.be
- added missing buildrequires for "ed", used in tests
- update to 33c
* Fri Mar 28 2008 - guru@unixtech.be
- update to 33b
* Mon Mar  3 2008 - guru@unixtech.be
- update to 33
* Fri Oct 26 2007 - guru@unixtech.be
- update to 32
* Mon Oct 15 2007 - guru@unixtech.be
- update to 31d
- pass -j to Build.sh to build in parallel (new in this version)
* Tue Sep 11 2007 - guru@unixtech.be
- update to 31b
* Sat Sep  8 2007 - guru@unixtech.be
- update to 31
* Fri Jul 27 2007 - guru@unixtech.be
- update to 30
* Mon Jul 23 2007 - guru@unixtech.be
- update to 29g
* Sun Jun 10 2007 - guru@unixtech.be
- add arc4random patch
* Sun May 27 2007 - guru@unixtech.be
- update to 29f
* Wed May 23 2007 - guru@unixtech.be
- update to 29e
* Tue May  1 2007 - guru@unixtech.be
- update to 29d
* Wed Apr 25 2007 - guru@unixtech.be
- re-enable -D_FORTIFY_SOURCE but pass HAVE_CAN_FWHOLEPGM=0 in environment, bug was actually triggered by -fwhole-program --combine
* Wed Apr 25 2007 - guru@unixtech.be
- remove -D_FORTIFY_SOURCE from CFLAGS, breaks build on 10.0 and 10.2 (and Factory) because of some obscure inlining error in unistd.h
* Tue Apr 24 2007 - guru@unixtech.be
- update to 29c
* Mon Mar 12 2007 - guru@unixtech.be
- CHANGES: some spin-loop bugs related to invalid multibyte input were fixed
- CHANGES: the -fstack-protector-all (ProPolice SSP) argument was added to CFLAGS if it is supported by the compiler
- CHANGES: a gcc bug is worked around if an affected version is detected
- CHANGES: minor code and man page cleanup was done
- CHANGES: fixes were made for the manual page.
- update to 29b
- use primary upstream source instead of Debian's (introduces having to use an cpio.gz archive which is not natively
  supported by rpmbuild)
* Sun Mar 04 2007 - mrueckert@suse.de
- update to 28.9.20070218
* Thu Oct 05 2006 - mrueckert@suse.de
- initial package of R28. based on the debian sources as they are
  maintained by upstream
