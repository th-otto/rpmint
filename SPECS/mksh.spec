#
# spec file for package mksh
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2013 Guido Berhoerster.
# Copyright (c) 2013, 2014, 2019 Thorsten Glaser.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# Please see OBS home:mirabile/mksh for a package for other distributions.

Name:           mksh
Version:        57
Release:        2.4
Summary:        MirBSD Korn Shell
License:        MirOS AND ISC
Group:          System/Shells
Url:            http://www.mirbsd.org/mksh.htm
Source:         https://www.mirbsd.org/MirOS/dist/mir/mksh/%{name}-R%{version}.tgz
# PATCH-FEATURE-OPENSUSE mksh-vendor-mkshrc.patch gber@opensuse.org -- Add support for a vendor-supplied kshrc which is read by interactive shells before $ENV or $HOME/.mkshrc are processed
Patch0:         mksh-vendor-mkshrc.patch
BuildRequires:  ed
# for %%check
BuildRequires:  perl
BuildRequires:  screen
BuildRequires:  sed
BuildRequires:  update-alternatives
%if 0%{?suse_version} >= 1315
# replaces pdksh in openSUSE >= 13.2 and SLES >= 12
Provides:       pdksh = %{version}
Obsoletes:      pdksh < %{version}
%if !0%{?is_opensuse}
Provides:       ksh = %{version}
Obsoletes:      ksh < %{version}
%endif
Provides:       /bin/ksh
Requires(post): update-alternatives
Requires(preun): update-alternatives
%else
# for SLES or openSUSE < 13.2 which do not mksh
Requires(post): grep
Requires(postun): awk
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
The MirBSD Korn Shell is an actively developed free implementation of the Korn
Shell programming language and a successor to the Public Domain Korn Shell
(pdksh).

%prep
%setup -q -n %{name}
%patch0 -p1 -b .p0

ed -s mksh.1 <<-'EOF'
	/insert-your-name-here/s/^\.\\" //
	s/insert-your-name-here/SUSE/
	w
	EOF
# " Stupid double quote for vi

ln -s . examples

%build
%define _lto_cflags %{nil}
#
# sys_errlist and sys_siglist *are* deprecated
# Be aware of the _SYS_SIGLIST and _SYS_ERRLIST macros as well
#
HAVE_SYS_SIGLIST=0
HAVE_SYS_ERRLIST=0
HAVE__SYS_SIGLIST=0
HAVE__SYS_ERRLIST=0
export HAVE_SYS_SIGLIST HAVE_SYS_ERRLIST HAVE__SYS_SIGLIST HAVE__SYS_ERRLIST

#
# -ftree-loop-linear
#    Perform loop nest optimizations.  Same as -floop-nest-optimize.
#    To use this code transformation, GCC has to be configured with
#    --with-isl to enable the Graphite loop transformation infrastructure.
#
export CC=gcc
if $CC -Werror -ftree-loop-linear -S -o /dev/null -xc /dev/null > /dev/null 2>&1
then
    export CFLAGS='%{optflags} -Wuninitialized -Wall -Wextra -ftree-loop-linear -pipe'
else
    export CFLAGS='%{optflags} -Wuninitialized -Wall -Wextra -pipe'
fi
case "$(uname -m)" in
ppc64)   CFLAGS="$CFLAGS -mbig-endian -mcpu=power4"  ;;
ppc64le) CFLAGS="$CFLAGS -mtune=power8 -mcpu=power8" ;;
esac
export CPPFLAGS='-DMKSH_VENDOR_MKSHRC_PATH=\"/etc/mkshrc\" -DMKSH_EARLY_LOCALE_TRACKING -DMKSH_ASSUME_UTF8'
export LDFLAGS='-Wl,--as-needed -Wl,-O2'
vendor=OpenBuildService
%if 0%{?suse_version} > 0
%if !0%{?is_opensuse}
vendor=SLES
%else
vendor=openSUSE
%endif
%endif
CPPFLAGS="$CPPFLAGS -DKSH_VERSIONNAME_VENDOR_EXT=\\\"\ +$vendor\\\""
if grep -q _DEFAULT_SOURCE /usr/include/features.h; then
	CPPFLAGS="$CPPFLAGS -D_DEFAULT_SOURCE"
fi
# filter compiler warnings and errors from configuration tests
{
    sh Build.sh -r || touch build.failed
    mv test.sh test-mksh.sh
    # build lksh to automatically enable -o posix if called as sh
    CPPFLAGS="$CPPFLAGS -DMKSH_BINSHPOSIX"
    sh Build.sh -L -r || touch build.failed
    mv test.sh test-lksh.sh
} 2>&1 | sed -r \
  -e 's!conftest.c:([0-9]*(:[0-9]*)*): error:!cE(\1) -!g' \
  -e 's!conftest.c:([0-9]*(:[0-9]*)*): warning:!cW(\1) -!g' \
  -e 's!conftest.c:([0-9]*(:[0-9]*)*): note:!cN(\1) -!g'
test ! -e build.failed

%install
install -d %{buildroot}/bin
for shell in mksh lksh; do
    install -D -p -m 755 ${shell} %{buildroot}%{_bindir}/${shell}
    install -D -p -m 644 ${shell}.1 %{buildroot}%{_mandir}/man1/${shell}.1
    ln -s %{_bindir}/${shell} %{buildroot}/bin/${shell}
done
install -d -m 755 %{buildroot}%{_sysconfdir}/alternatives
ln -s %{_sysconfdir}/bash.bashrc %{buildroot}%{_sysconfdir}/mkshrc
%if 0%{?suse_version} >= 1315
# compatibility symlinks for pdksh, lksh replaces pdksh in openSUSE >= 13.2
ln -s /bin/lksh %{buildroot}/bin/pdksh
ln -s %{_bindir}/lksh %{buildroot}%{_bindir}/pdksh
ln -s %{_mandir}/man1/lksh.1%{ext_man} \
    %{buildroot}%{_mandir}/man1/pdksh.1%{ext_man}
# symlinks for update-alternatives
touch %{buildroot}%{_sysconfdir}/alternatives/ksh \
    %{buildroot}%{_sysconfdir}/alternatives/usr-bin-ksh \
    %{buildroot}%{_sysconfdir}/alternatives/ksh.1%{ext_man}
ln -sf %{_sysconfdir}/alternatives/ksh %{buildroot}/bin/ksh
ln -sf %{_sysconfdir}/alternatives/usr-bin-ksh %{buildroot}/%{_bindir}/ksh
ln -sf %{_sysconfdir}/alternatives/ksh.1%{ext_man} \
    %{buildroot}/%{_mandir}/man1/ksh.1%{ext_man}
%endif

%check
# should always run in a clean environment as otherwise
# tests might fail due wrong line numbering
SCREENDIR=$(mktemp -d ${PWD}/screen.XXXXXX) || exit 1
trap 'rm -rf $SCREENDIR' EXIT
SCREENRC=${SCREENDIR}/mksh
export SCREENRC SCREENDIR
export HOME=${SCREENDIR}
exec 0< /dev/null
SCREENLOG=${SCREENDIR}/log
cat > $SCREENRC<<-EOF
	deflogin off
	deflog on
	logfile $SCREENLOG
	logfile flush 1
	logtstamp off
	log on
	setsid on
	scrollback 0
	silence on
	utf8 on
	EOF
> $SCREENLOG
tail -q -s 0.5 -f $SCREENLOG & pid=$!
for shell in mksh lksh; do
    screen -D -m sh -c "./test-${shell}.sh -v -f || > failed"
done
kill -TERM $pid
if test -e failed
then
    sed -rn '/FAIL /,/^pass /p' $SCREENLOG
    exit 1
fi

%clean
rm -Rf %{buildroot}

%if 0%{?suse_version} >= 1315
%post
%{_sbindir}/update-alternatives \
  --install /bin/ksh ksh %{_bindir}/lksh 15 \
  --slave %{_bindir}/ksh usr-bin-ksh %{_bindir}/lksh \
  --slave %{_mandir}/man1/ksh.1%{?ext_man} ksh.1%{?ext_man} %{_mandir}/man1/lksh.1%{?ext_man}

%preun
if test $1 -eq 0 ; then
    %{_sbindir}/update-alternatives --remove ksh /bin/lksh
fi
%else
# for SLE or openSUSE < 13.2 which do not support mksh
%post
for entry in /bin/mksh %{_bindir}/mksh; do
    grep -q ${entry} %{_sysconfdir}/shells ||\
        printf '%%s\n' ${entry} >>%{_sysconfdir}/shells
done

%postun
test -x %{_bindir}/mksh && awk '
($1 != "/bin/mksh") && ($1 != "%{_bindir}/mksh") {
    line[n++] = $0
}
END {
    for (i = 0; i < n; i++) {
        print line[i] >"%{_sysconfdir}/shells"
    }
}' '%{_sysconfdir}/shells' || true
%endif

%files
%defattr(-,root,root)
%doc examples/dot.mkshrc
%{_sysconfdir}/mkshrc
/bin/mksh
/bin/lksh
%{_bindir}/mksh
%{_bindir}/lksh
%{_mandir}/man1/mksh.1%{?ext_man}
%{_mandir}/man1/lksh.1%{?ext_man}
%if 0%{?suse_version} >= 1315
/bin/pdksh
%{_bindir}/pdksh
%{_mandir}/man1/pdksh.1%{?ext_man}
/bin/ksh
%{_bindir}/ksh
%{_mandir}/man1/ksh.1%{?ext_man}
%ghost %{_sysconfdir}/alternatives/ksh
%ghost %{_sysconfdir}/alternatives/usr-bin-ksh
%ghost %{_sysconfdir}/alternatives/ksh.1%{?ext_man}
%endif

%changelog
* Thu Sep  5 2019 m@mirbsd.org
- Disable LTO, GCC’s is too buggy and generates wrong code
  (note LTO was disabled earlier already, but apparently,
  it’s now enabled distro-wide which we need to counteract)
* Tue Apr  9 2019 t.glaser@tarent.de
- KSH_VERSIONNAME_VENDOR_EXT needs to begin with a space and plus
* Tue Apr  9 2019 t.glaser@tarent.de
- Fix CPPFLAGS double shell escape of space character
* Tue Apr  9 2019 t.glaser@tarent.de
- KSH_VERSIONNAME_VENDOR_EXT needs to begin with a space
* Tue Apr  9 2019 t.glaser@tarent.de
- Ensure the extra CPPFLAGS are actually used, oops…
* Tue Apr  9 2019 t.glaser@tarent.de
- Remove virt-what from build dependencies, it just fails or,
  worse, makes the package unresolvable; also from lewellyn
- Ensure KSH_VERSIONNAME_VENDOR_EXT is always set to something,
  because the patch deviating from upstream is always applied
* Tue Apr  9 2019 t.glaser@tarent.de
- Update to version R57 (reminded by lewellyn)
  R57 rolls up bugfixes, with few hard changes:
    [gecko2] Update operating environment reporting for the Macintosh
    [Martijn Dekker] make ${foo#'bar'} in here document behave like ksh93
    [Martijn Dekker] quote empty strings for re-entry into shell
    [tg, G.raud Meyer] Improve documentation, especially for tty states
    [tg] Protect against entering line editing with bad saved tty state
    [tg] Fix set -o allexport for arrays (which we apparently do)
    [tg] Handle lseek(2) returning -1 as pointed out by Coverity Scan
    [tg] Fix left-padding UTF-8 strings
    [tg, G.raud Meyer] Fix using the “-m” flag on the command line
    [tg] Update to UCD 11.0.0
    [multiplexd] Fix a segfault using ^W during search in Vi mode
    [tg] Fix an error message; add a test for controlling tty
    [tg] Permit unsetting LINES and COLUMNS, for those who need it
    [tg] Fix manpage bug (RedHat BZ#1612173)
    [tg] Minor spelling cleanup
    [tg] Unbreak high-bit7 (nōn-ASCII) heredoc separators (LP#1779179)
    [tg] Allow dumping high-bit7-char-containing strings in DEBUG mode
    [tg] Add some testcases for behaviour questions popped up in IRC
    [tg] Trick a GCC warning, to make up for it ignoring lint(1) hints
    [tg] Add O_MAYEXEC support for CLIP OS
    [tg] Make dup-to-self with ksh-style fd≥3 closing work; catern via IRC
    [tg] Add compat glue for newer GNU groff mdoc to the manpages
    [tg] Trigger EXIT trap after single-command subshells (Debian #910276)
    [tg] Document set -eo pipefail caveat (LP#1804504)
    [tg] Fix MKSH_EARLY_LOCALE_TRACKING warning
    [tg] Document that, when your Unix is broken, GIGO applies (LP#1817959)
    [tg] Improve error message for inaccessible executables (LP#1817789)
- Switch from patching check.t, sh.h and Build.sh to using
  KSH_VERSIONNAME_VENDOR_EXT and appending to CPPFLAGS beforehand
- Remove qemu/ppc patches that are upstreamed/no longer necessary
- Drop LTO support which was already always disabled
- Handle newer GCC note output during configure stage
* Tue Apr 17 2018 werner@suse.de
- Remove patch mksh-locale.patch and use upstream compile flags
  MKSH_EARLY_LOCALE_TRACKING as replacement
* Tue Apr 17 2018 werner@suse.de
- Update to version R56c
  R56c is a bugfix-only release everyone must upgrade to:
    [komh] Remove redundant OS/2-specific code, clean up others
    [komh, tg] Fix drive-qualified (absolute and relative) DOS-style
    path support in realpath functionality, partially other places
    [tg] Don’t substitute ${ENV:-~/.mkshrc} result again
    [tg] Improve OS/2 $PATH (et al.) handling, drive-relative paths
    [tg] Add MKSH_ENVDIR compile-time option for Jehanne and Plan 9
    [tg] Limit nesting when parsing malformed code (Debian #878947)
    [tg] Update wcwidth data with bugfixed script (still Unicode 10;
    resulting values are identical to glibc git master for extant chars)
    [Dr. Werner Fink] Raise some time limits in the testsuite
    [Shamar] Add support for the Jehanne operating system
    [komh] Set stdin to text mode before executing child processes on OS/2
    [komh] Pass arguments via a resonse file if executing a child fails
    [Dr. Werner Fink] Early locale tracking as a compile-time option
    [tg] Fix regressions introduced with new fast character classes
  R56b is a bugfix-only release everyone should upgrade to:
    [tg] Reference the FAQ webpage
    [panpo, Riviera] Fix documentation bug wrt. Esc+Ctrl-L
    [tg, Larry Hynes] Fix “0” movement in vi mode
    [tg] Replace broken libcs’ offsetof macro with MirBSD’s
  R56 is a bugfix release with some experimental fixes:
    [tg, Seb] Do not apply alias name restrictions to hash/tilde tracking
    [tg] Restore ‘.’, ‘:’ and ‘[’ in alias names (“[[” is still forbidden)
    [tg] Fix accidentally defanged $PATHSEP test
    [tg] On ^C (INTR and QUIT edchars), shove edit line into history
    [iSKUNK, tg] Begin porting to z/OS using EBCDIC encoding, incomplete
    [tg] Redo fast character classes code, adding POSIX and other helpers
    [tg] bind parses backslash-escaped ‘^’ (and ‘\’) as escaped
    [tg] Building with -DMKSH_ASSUME_UTF8=0 no longer causes a known
    failure in the testsuite
    [tg] New test.sh option -U to pass a UTF-8 locale to use in the tests
    [tg] re_format(7) BSD: [[ $x = *[[:\<:]]foo[[:\>:]]* ]]
    [tg, iSKUNK] Use Config in check.pl only if it exists
    [tg] New matching code for bracket expressions, full POSIX (8bit)
    [komh] Exclude FAT/HPFS/NTFS-unsafe tests on OS/2 (and Cygwin/MSYS)
    [tg] Update to Unicode 10.0.0
    [tg, selk] Make readonly idempotent
    [tg, multiplexd] When truncating the persistent history, do not change
    the underlying file, do all operations on the locked one; do not
    stop using the history at all if it has been truncated
    [tg, Jörg] Turn off UTF-8 mode upon turning on POSIX mode
    [Martijn Dekker, Geoff Clare, many on the Austin list, tg] In POSIX
    mode, make the exec builtin force a $PATH search plus execve
    [tg] Fix GCC 7, Coverity Scan warnings
    [tg, Michal Hlavinka] Track background process PIDs even interactive
    [tg] Always expose mksh’s hexdump shell function; speed it up by
    working on the input in chunks; use character classes to make it EBCDIC safe
    [tg] Revamp dot.mkshrc default editor selection mechanism
  R55 is mostly a feature release with summary bugfixes:
    [komh] Fix OS/2 search_access() and UNC path logic
    [tg] Undocument printf(1) to avoid user confusion
    [Jean Delvare, tg] Fix printf builtin -R option
    [tg] Make ${var@x}, unknown x, fail (thanks izabera)
    [tg] ${var=x} must evaluate x in scalar context (10x Martijn Dekker)
    [tg] Fixup relation between lksh and mksh, reduce delta
    [tg] Improve manpage display; add OS/2 $PATH FAQ
    [Jean Delvare] Fix bugs in manpage
    [tg] Review tilde expansion, removing “odd use of KEEPASN” and
    introduce POSIX “declaration utility” concept; wait isn’t one
    [tg] Add \builtin utility, declaration utility forwarder
    [tg] Make $'\xz' expand to xz, not \0
    [tg] Use fixed string pooling (requires the above change in host mksh)
    [tg] POSIX declaration commands can have varassign and redirections
    [Martijn Dekker] Add typeset -g, replacing homegrown “global”
    [Harvey-OS] Disable NOPROSPECTOFWORK, APEX is reportedly fixed now
    [tg] Display ulimit -a output with flags; improve Haiku
    [tg] Drop old let] hack, use \builtin internally
    [tg] Fix padding in Lb64encode in dot.mkshrc
    [tg] Move FAQ content to a separate, new FAQ section in the manpage
    [tg] Add new standard variable PATHSEP (‘:’, ‘;’ on OS/2)
    [Martijn Dekker] Fix LINENO in eval and alias
    [komh] Fix “\builtin” on OS/2
    [tg] Improve (internal) character classes code for speed
    [tg] Fix: the underscore is no drive letter
    [tg] No longer hard-disable persistent history support in lksh
    [tg] Introduce build flag -T for enabling “textmode” on OS/2
    (supporting CR+LF line endings, but incompatible with mksh proper)
    [tg] Merge mksh-os2
    [tg] Permit changing $OS2_SHELL during a running shell
    [tg] Fix multibyte handling in ^R (Emacs search-history)
    [tg] Allow “typeset -p arrname[2]” to work
    [tg] Make some error messages more consistent
    [tg, komh] Disable UTF-8 detection code for OS/2 as unrealistic
    [tg, sdaoden] Limit alias name chars to POSIX plus non-leading ‘-’
    [tg, Martijn Dekker] Expand aliases at COMSUB parse time
    [tg] Make “typeset -f” output alias-resistent
    [tg, Martijn Dekker] Permit “eval break” and “eval continue”
    [tg] Make -masm=intel safe on i386[tg] Disambiguate
    $((…)) vs. $((…)…) in “typeset -f” output
    [Jean Delvare] Clarify the effect of exit and return in a subshell
    [tg] Simplify compile-time asserts and make them actually compile-time
    [tg] Fix ^O in Emacs mode if the line was modified (LP#1675842)
    [tg] Address Coverity Scan… stuff… now that it builds again
    [Martijn Dekker, tg] Add test -v
    [tg] Document set -o posix/sh completely
* Fri Dec 15 2017 werner@suse.de
- Add patch mksh-locale.patch to enable the mksh to set internal
  lcoale settings like utf support during runtime
* Wed Nov 22 2017 werner@suse.de
- Do not change Build.sh for not using hard coded list of signals
  and errors but the cpp macros for this (requested by upstream)
* Tue Nov 14 2017 werner@suse.de
- The AT&T ksh is still part of openSUSE but on SLES only mksh
  should be used (bsc#1067195)
* Thu Feb 23 2017 werner@suse.de
- Avoid deprecated API for errors and signals
- Be sure to use a clean history file
* Tue Feb 21 2017 werner@suse.de
- Make errors ini test suite fatal
- Avoid -flto as this breaks even with gcc 6.3.1 20170202
* Tue Feb 14 2017 werner@suse.de
- Use screen to provide a tty for test suite scripts
* Tue Feb 14 2017 werner@suse.de
- Update to version R54
  R54 is a bugfix release with moderate new features:
    [tg] Simplify and improve code and manual page
    [tg] Try GCC 5’s new -malign-data=abi
    [tg] Allow interrupting builtin cat even on fast devices (LP#1616692)
    [tg] Update to Unicode 9.0.0
    [Andreas Buschka] Correct English spelling
    [tg] Handle set -e-related error propagation in || and && constructs correctly
    [tg] Initialise memory for RNG even when not targeting Valgrind
    [tg] Shrink binary size
    [Brian Callahan] Improve support for the contemporary pcc compiler
    [tg] Fix side effects with lazy evaluation; spotted by ormaaj
    [tg] New flags -c (columnise), -l, -N for the print builtin
    [Larry Hynes] Fix English, spelling mistakes, typos in the manpage
    [tg, ormaah] Return 128+SIGALRM if read -t times out, like GNU bash
    [Martijn Dekker] Install both manpages from Build.sh
    [Martijn Dekker] Document case changes are ASCII-only
    [Ronald G. Minnich, Elbing Miss, Álvaro Jurado, tg] Begin porting to Harvey-OS and APEX (similar to Plan 9 and APE)
    [KO Myung-Hun] More infrastructure for the OS/2 (EMX, KLIBC) port
  R53a is a snapshot/feature release:
    [lintian] Fix spelling
    [tg] Unbreak multi-line command history broken by history flush
    [tg] Fix redefining POSIX functions that were Korn functions before
    [tg, TNF] Fix bounds checks in Vi editing mode
    [tg] Handle combining characters at end of string or output correctly
    [tg] Fix ${!#} ${!?} ${!-} (POSIX, prompted by izabera)
    [tg] Fix shf.c-internal buffer overread on printing digits
    [J�rg] Fix a typo in the testsuite
    [arekm] Increase default edit line size (unless MKSH_SMALL)
    [tg] Improve description of Emacs mode keybindings, especially ^U
    [tg, arekm, jilles] Abort read builtin in case of read(2) errors
    [tg, izabera, carstenh] Fix most of the ambiguous corner cases related to ${[pfx]var[op[word]]} (${@:-1} still unsupported)
    [carstenh] Contribute some more testsuite coverage
    [tg] WDS_TPUTS now emits QCHAR newline reentrant-safe
    [tg] Fix var=<< implementation (LP#1380389)
    [tg, FreeBSD] Make XSI test(1) extensions behave as if they were POSIX
    [tg, izabera] Add $(<<<x) and $(<<EOF…) implementation
    [tg] Lower minimum screen size accepted as “sane” from the OS to 4×2
    [tg, Torsten Sillke] Simplify tilde-expanded parameters
    [tg, Torsten Sillke] Fix default PS1 for substring matches
    [tg] Apply defer-builtin-with-arguments logic to realpath builtin
    [tg] Rework string pooling (own vs. compiler’s) (LP#1580348)
    [tg] Feature: print -A, prints arguments as characters
    [tg, izabera] Replace <<< and >>> as ROL and ROR operators with their new ^< and ^> spelling as per this proposal
    [tg, slagtc] Clear-to-EOL under tmux to work around its anti-feature
    [tg, p120ph37] Remove support for using file descriptors with more than a single digit, in preparation for named file descriptors
    [tg] Correct, but simplify (at the potential cost of more tty I/O than strictly necessary, though never redundant and (probably) not more than before when it was miscalculated), line clearing and redrawing
    [slagtc, tg] Implement new evaluate-region editing command Esc+Ctrl-E
    [tg] Prefer external rename utility over the recovery builtin
    [tg] Remove redundant full-line redraws
    [tg, Natureshadow] Fix errorlevel of ‘.’ (“dot” special builtin) when the sourced script does not run any commands, for POSIX compliance
    [tg] Refactor op tokens and edchars to shave off some more bytes
    [tg] Fix some bugs in the manpage and some occasional/minor code bugs
    [tg, Brian Callahan] Mark tests requiring new perl as !need-pass
    [tg, slagtc] Add $KSH_MATCH and, to make it usable, ${foo@/bar/baz}
    [tg, Score_Under] Fix bogus patch from OpenBSD: only NULL the global source in unwind when actually reclaiming its Area
    [izabera] Mention in the manpage that integer bases go up to 36
    [Natureshadow] Fix /= operator broken during refactoring
  R52c is a bugfix-only release:
    [tg] Shave 200 bytes off .text by revisiting string pooling
    [tg, J�rg] Fix manpage for ditroff on Schillix
    [tg, wbx] Use sed 1q instead of unportable head(1)
    [tg] Implement underrun debugging tool for area-based memory allocator
    [tg] Fix history underrun when first interactive command is entered
    [tg, bef0rd] Do not misinterpret “${0/}” as “${0//”, fixes segfault
    [tg, Stéphane Chazelas] Fix display problems with special parameters
    [tg, Stéphane Chazelas] Catch attempt to trim $* and $@ with ?, fixes segfault (Todd Miller did this in 2004 for ${x[*]} already, so just sync)
    [Martijn Dekker] Fix “command -p” with -Vv to behave as POSIX requires
    [tg, jilles, Oleg Bulatov] Fix recusive parser with active heredocs
    [tg] Flush even syntax-failing or interrupted commands to history
    [tg, fmunozs] Fix invalid memory access for “'\0'” in arithmetics
    [tg] Explicitly reserve SIGEXIT and SIGERR for ksh
    [tg, izabera] Catch missing here documents at EOF even under “set -n”
    [kre, tg] Document Austin#1015 handling (not considered a violation)
    [tg, fmunozs] Fix buffer overread for empty nameref targets
    [tg] Fix warnings pointed out by latest Debian gcc-snapshot
    [tg, Martijn Dekker] Document upcoming set +o changes
    [Martijn Dekker] Expand testsuite for command/whence
  R52b is a strongly recommended bugfix-only release:
    [tg] Recognise ksh93 compiled scripts and LZIP compressed files as binary (i.e. to not run as mksh plaintext script)
    [tg] Document that we will implement locale tracking later
    [tg] Add EEXIST to failback strerror(3)
    [jilles] Make set -C; :>foo race-free
    [tg] Don’t use unset in portable build script
    [tg] Plug warning on GNU/kFreeBSD, GNU/Hurd
    [tg] Document read -a resets the integer base
    [J�rg] Fix manpage: time is not a builtin but a reserved word
    [J�rg, tg] Make exit (and return) eat -1
    [tg] parse “$( (( … ) … ) … )” correctly (LP#1532621), Jan Palus
    [tg] reduce memory footprint by free(3)ing more aggressively
    [tg] fix buffer overrun (LP#1533394), bugreport by izabera
    [tg] correctly handle nested ADELIM parsing (LP#1453827), Teckids
    [tg] permit “read -A/-a arr[idx]” as long as only one element is read; fix corruption of array indicēs with this construct (LP#1533396), izabera
    [tg] Sanitise OS-provided signal number in even more places
    [tg] As requested by J�rg, be clear manpage advice is for mksh
    [tg] Revert (as it was a regression) POSIX bugfix from R52/2005 related to accent gravis-style command substitution until POSIX decides either way
    [tg] Handle export et al. after command (Austin#351)
    [tg] Catch EPIPE in built-in cat and return as SIGPIPE (LP#1532621)
    [tg] Fix errno in print/echo builtin; optimise that and unbksl
    [tg] Update documentation, point out POSIX violation (Austin#1015)
  R52 is a strongly recommended bugfix release:
    [_0bitcount] Move moving external link from mksh(1) to the #ksh channel homepage linked therein
    [tg] Make setenv “set -u”-safe and fix when invoked with no args
    [tg] Make “typeset -f” output reentrant if name is a reserved word
    [oksh] Zero-pad seconds in “time” output to align columns
    [tg] Check signals and errorlevels from OS to be within bounds
    [komh, tg] Quote and document ‘;’ as PATH separator in some places
    [oksh, tg] Simplify code to call afree() even if arg is NULL
    [tg] Fix tree-printing and reentrancy of multiple here documents
    [tg] Work around LP#1030581 by permitting exactly one space after
    [tg, oksh] Code quality work, cleanups
    [tg] New code for here documents/strings with several bugfixes
    [tg] Stop using issetugid(2) for ±p checks, wrong tool for the job
    [tg] Reintroduce some -o posix changes lost in 2005, plus fixes
    [tg] Make “source” into a built-in command
    [tg] Drop “stop” alias, lksh(1) functionality to auto-unalias
    [tg] Fix \u0000 ignored in $'…' and print
    [tg] Improve portability of Build.sh
    [Jilles Tjoelker] Improve portability of testsuite
    [tg] Fix tilde expansion for some substitutions (izabera, Chet, Geoff)
    [tg] Improve reparsing of ((…) |…) as ( (…) |…)
    [Martijn Dekker] Fix test(1) not returning evaluation errors
    [tg] Fix ${*:+x} constructs (carstenh)
    [tg] Make (( … )) into a compound command (ormaaj)
    [tg] Repair a few parameter substitution expansion mistakes
  R51 is a strongly recommended feature release:
    [tg] OpenBSD sync: handle integer base out of band like ksh93 does
    [tg] Protect standard code (predefined aliases, internal code, aliases and functions in dot.mkshrc) from being overridden by aliases and, in some cases, shell functions (i.e. permit overriding but ignore it)
    [tg] Implement GNU bash’s enable for dot.mkshrc using magic aliases to redirect the builtins to external utilities; this differs from GNU bash in that enable takes precedence over functions
    [tg] Move unaliasing an identifier when defining a POSIX-style function with the same name into lksh, as compatibility kludge
    [tg] Korn shell style functions now have locally scoped shell options
    [tg, iSKUNK] Change some ASCII-isms to be EBCDIC-aware or pluggable
    [tg, Ypnose] Mention lksh build instructions on manpage and website
    [tg] Overhaul signal handling; support new POSIX NSIG_MAX, add sysconf(_SC_NSIG) as a later TODO item
    [tg] Fix signal bounds (1 ≤ signum < NSIG)
    [tg] Improve manual pages, especially wrt. standards compliance
    [tg, iSKUNK] Initial EBCDIC work for dot.mkshrc
    [tg, iSKUNK] Add list of z/OS signals to Build.sh
    [tg] Work around the sh(1) backslash-newline problem by moving the code triggering it out of *.opt and into the consumers
    [colona] Bind another well-known ANSI Del key in the Emacs mode
    [tg] Fix ${foo/*/x} pattern checks, spotted by izabera
    [carstenh] Fix error output of cd function in dot.mkshrc
    [tg] read partial returns in -N and timeout cases
    [tg] Fix $LINENO inside PS1; spotted by carstenh
    [tg] Ensure correct padding of at least 2 spaces in print_columns
    [tg] Note issues with nested complex parameter expansions and follow-up bugfixes to expect
    [OpenBSD] Some language fixes in documentation; comments
    [tg] Reimplement multi-line command history (Debian #783978) + fixes
    [Martijn Dekker] Fix command -v for “shell reserved words”
    [tg] In dot.mkshrc make use of latest feature: local options
    [tg] Fix ""$@ to emit a word
    [tg] Change cat(1) hack to look first and not ignore builtin
    [KO Myung-Hun] Begin porting mksh to OS/2
    [komh, tg] Some generic minor bugfixes from OS/2 porting
    [tg] Document mknod(8) isn’t normally part of mksh(1)
    [tg] Quote arguments to : in build/test scripts as well
    [tg] Add cat(1) hack for printf(1)-as-builtin: always prefer external
    [tg] Explicitly use binary mode for any and all file I/O in stock mksh
    [Ilya Zakharevich] Use termio, not termios(4), on OS/2
    [tg] Set edchars to sane BSD defaults if any are NUL
    [tg] Implement support for PC scancodes in Vi and Emacs editing mode
    [komh] OS/2 uses ‘;’ as PATH separator plus support drive letters
* Mon Apr 20 2015 gber@opensuse.org
- mention vendor modifications in manpage as requested by upstream
* Mon Apr 20 2015 gber@opensuse.org
- update to version 50f
  - [tg] OpenBSD sync: handle integer base out of band like ksh93
    does
  - [tg] Protect standard code (predefined aliases, internal code,
    aliases and functions in dot.mkshrc) from being overridden by
    aliases and, in some cases, shell functions (i.e. permit
    overriding but ignore it)
  - [tg] Implement GNU bash’s enable for dot.mkshrc using magic
    aliases to redirect the builtins to external utilities; this
    differs from GNU bash in that enable takes precedence over
    functions
  - [tg] Move unaliasing an identifier when defining a POSIX-style
    function with the same name into lksh, as compatibility kludge
  - [tg] Korn shell style functions now have locally scoped shell
    options
  - [tg] Add a patch marker for vendor patch versioning to mksh.1
  - [tg] SECURITY: make unset HISTFILE actually work
  - [tg] Document some more issues with the current history code
  - [tg] Remove some unused code
  - [tg] RCSID-only sync with OpenBSD, for bogus and irrelevant
    changes
  - [tg] Also disable field splitting for alias 'local=\typeset'
  - [tg] Fix read -n-1 to not be identical to read -N-1
  - [tg] Several fixes and improvements to lksh(1) and mksh(1)
    manpages
  - [tg] More code (int → size_t), comment and testsuite fixes
  - [tg] Make dot.mkshrc more robust (LP#1441853)
  - [tg] Fix issues with IFS='\' read, found by edualbus
  - [enh, tg] Fix integer overflows related to file descriptor
    parsing, found by Pawel Wylecial (LP#1440685); reduce memory
    usage for I/O redirs
  - [tg] Document in the manpage how to set ±U according to the
    current locale settings via LANG/LC_* parameters (cf. Debian
    [#782225])
  - [igli, tg] Some code cleanup and restructuring
  - [tg, oksh] Handle number parsing and storing more carefully
* Sun Mar  1 2015 gber@opensuse.org
- update to version 50e
  - [tg] Add more tests detailing behaviour difference from GNU
    bash
  - [tg] Introduce a memory leak for x=<< fixing use of freed
    memory instead, bug tracked as LP#1380389 still live
  - [tg] Add x+=<< parallel to x=<<
  - [tg, ormaaj, jilles] POSIX “command” loses builtin special-ness
  - [tg] Fix LP#1381965 and LP#1381993 (more field splitting)
  - [jilles] Update location of FreeBSD testsuite for test(1)
  - [Martin Natano] Remove dead NULL elements from Emacs
    keybindings
  - [tg, Stéphane Chazelas, Geoff Clare] Change several testcases
    for $*/$@ expansion with/without quotes to expected-fail, with
    even more to come ☹
  - [tg] Fix miscalculating required memory for encoding the
    double-quoted parts of a here document or here string
    delimiter, leading to a buffer overflow; discovered by zacts
    from IRC
  - [RT] Rename a function conflicting with a MacRelix system
    header
  - [tg] Use size_t (and ssize_t) consistently, stop using
    ptrdiff_t; fixes some arithmetics and S/390 bugs
  - [tg] Remove old workarounds for Clang 3.2 scan-build
  - [tg] Remove all Clang/Coverity assertions, making room for new
    checks
  - [tg] Fix NSIG generation on Debian sid gcc-snapshot
  - [tg] Make a testcase not fail in a corner case
  - [tg] Fix issues detected by GCC’s new sanitisers: data type of
    a value to be shifted constantly must be unsigned (what not, in
    C…); shebang check array accesses are always unsigned char
  - [tg] Be even more explicit wrt. POSIX in the manpage
  - [tg] Fix shebang / file magic decoding
  - [tg] More int → bool conversion
  - [tg] Let Build.sh be run by GNU bash 1.12.1 (Slackware 1.01)
  - [Stéphane Chazelas, tg] Fix here string parsing issue
  - [tg] Point out more future changes in the manpage
  - [tg] Call setgid(2), setegid(2), setuid(2) before seteuid(2)
  - [tg] Fix spurious empty line after ENOENT “whence -v”, found by
    Ypnose
  - [tg] Optimise dot.mkshrc and modernise it a bit
  - [tg] Use MAXPATHLEN from <sys/param.h> for PATH_MAX fallback
  - [tg] Some code cleanup and warnings fixes
  - [tg] Add options -a argv0 and -c to exec
  - [jsg] Prevent use-after-free when hitting multiple errors
    unwinding
  - [tg] Fix use of $* and $@ in scalar context: within [[ … ]] and
    after case (spotted by Stéphane Chazelas) and in here documents
    (spotted by tg@); fix here document expansion
  - [tg] Unbreak when $@ shares double quotes with others
  - [tg] Fix set -x in PS4 expansion infinite loop
* Tue Oct  7 2014 tg@mirbsd.org
- update to regression bugfix version 50d
  - [Goodbox] Fix NULL pointer dereference on “unset x; nameref x”
  - [tg] Fix severe regression in field splitting (LP#1378208)
  - [tg] Add a warning about not using tainted user input (including
    from the environment) in arithmetics, until Stéphane writes it up
    nicely
- refresh vendor patch
* Fri Oct  3 2014 tg@mirbsd.org
- update to SECURITY version 50c
  - [tg] Know more rare signals when generating sys_signame[] replacement
  - [tg] OpenBSD sync (mostly RCSID only)
  - [tg] Document HISTSIZE limit; found by luigi_345 on IRC
  - [zacts] Fix link to Debian .mkshrc
  - [tg] Cease exporting $RANDOM (Debian #760857)
  - [tg] Fix C99 compatibility
  - [tg] Work around klibc bug causing a coredump (Debian #763842)
  - [tg] Use issetugid(2) as additional check if we are FPRIVILEGED
  - [tg] SECURITY: do not permit += from environment
  - [tg] Fix more field splitting bugs reported by Stephane Chazelas and
    mikeserv; document current status wrt. ambiguous ones as testcases too
- use build log cleaner sed command from home:mirabile package
- enable lksh build-time option to automatically run "set -o posix"
  when called as sh or -sh, like home:mirabile package did
* Thu Sep  4 2014 gber@opensuse.org
- update to version 50b
  - [Ypnose] Fix operator description in the manpage
  - [tg] Change all mention of “eglibc” to “glibc”, it is merged
    back
  - [Colona] Fix rare infinite loop with invalid UTF-8 in the edit
    buffer
  - [tg] Make more clear when a shell is interactive in the manpage
  - [tg] Document that %% is a symmetric remainder operation, and
    how to get a mathematical modulus from it, in the manpage
  - [tg, Christopher Ferris, Elliott Hughes] Make the cat(1)
    builtin also interruptible in the write loop, not just in the
    read loop, and avoid it getting SIGPIPE in the smores function
    in dot.mkshrc by terminating cat upon user quit
  - [tg] Make some comments match the code, after jaredy from obsd
    changed IFS split handling
  - [tg] Fix some IFS-related mistakes in the manual page
  - [tg] Document another issue as known-to-fail test IFS-subst-3
  - [tg] Improve check.pl output in some cases
  - [tg, Jb_boin] Relax overzealous nameref RHS checks
* Thu Aug 21 2014 pth@suse.de
- We use update-alternatives so there is no need to obsolete ksh.
- Do not differentiate between openSUSE and SLES and simply state
  that this is the SUSE version.
* Tue Aug 19 2014 pth@suse.de
- Test for suse_version 1315 as that is what SLE12 will be using.
* Sun Jun 29 2014 gber@opensuse.org
- update to version 50
  - [tg] Fix initial IFS whitespace not being ignored when
    expanding
  - [tg] MKSH_BINSHREDUCED no longer mistakenly enables brace
    expansion
  - [tg] Explain more clearly Vi input mode limitations in the
    manpage
  - [tg] Improve error reporting of the check.pl script (which
    needs a maintainer since I don’t speak any perl(1), really),
    for lewellyn
  - [tg] Use $TMPDIR in test.sh for scratch space
  - [tg, Polynomial-C] Check that the scratch space is not mounted
    noexec
  - [pekster, jilles, tg] Use termcap(5) names, not terminfo(5)
    names, in tput(1) examples, for improved portability (e.g. to
    MidnightBSD)
  - [tg] Avoid C99 Undefined Behaviour in mirtoconf LFS test
    (inspired by Debian #742780)
  - [tg] Fix ${!foo} for when foo is unset
  - [tg] Improve nameref error checking (LP#1277691)
  - [tg] Fix readonly bypass found by Bert Münnich
  - [Ryan Schmidt] Improved system reporting for Mac OS X
  - [nDuff] Explain better [[ extglob handling in the manpage
  - [tg] Remove arr=([index]=value) syntax due to regressions
  - [tg] IFS-split arithmetic expansions as per POSIX 201x
  - [OpenBSD] Add more detailed Authors section to manpage
  - [tg] Fix set ±p issue for good: drop privs unless requested
  - [tg] Improve signal handling and use a more canonical probing
    order
  - [tg] Fix return values $? and ${PIPESTATUS[*]} interaction with
    set -o pipefail and COMSUBs
  - [enh] Detect ENOEXEC ELF files and use a less confusing error
    message
  - [tg] Update to Unicode 7.0.0
  - [tg] Shut up valgrind in the $RANDOM code
  - [tg] Use -fstack-protector-strong in favour of
  - fstack-protector-all
  - [tg] Fix access-after-free crash spotted by Enjolras via IRC
* Sat Feb  8 2014 gber@opensuse.org
- adjust update-alternative usage to packaging policy
  (see http://lists.opensuse.org/opensuse-packaging/2014-02/msg00024.html)
* Sun Jan 12 2014 gber@opensuse.org
- update to version 49
  - [tg] dot.mkshrc: fix two issues with the cd wrapper
  - [tg] Unbreak set +p (wider issue still to be addressed)
  - [Steffen Daode Nurpmeso] Use WCONTINUED with waitpid(2)
  - [millert] Add proper suspend builtin handling tty(4) and
    setpgrp(2)
  - [tg] Sanitise and slightly optimise control character handling
  - [tg] Add O_BINARY to all open(2) calls for OS/2 kLIBC support
  - [tg] Generate option strings for shell, set, ulimit at compile
    time
  - [Steffen Daode Nurpmeso] Drop ISTRIP termios(4) mode
  - [tg] Mention negative history numbers, octals in the manpage
  - [tg] Make check.pl work with Perl < 5.6.1 again
  - [tg] Detect getsid(2) and skip the oksh suspend builtin
    otherwise
  - [tg] Document that set -o noclobber is unsafe for tempfiles
  - [tg] Update to Unicode 6.3.0
  - [RT] Restore some portability
  - [tg] Fix parsing positional argument variable names
  - [tg] Sprinkle a few __attribute__((__pure__)); fix warnings
  - [tg] Fix build on OSX: always use our wcwidth code; only use
    our strlcpy(3) code if the OE doesn’t provide one (prompted by
    jonthn on IRC)
  - [tg] Optimise sh -c to exec even in MKSH_SMALL
  - [tg] Use new BAFH for hashing
* Fri Oct 18 2013 gber@opensuse.org
- replace pdksh in openSUSE >= 13.2, lksh provides backwards
  compatibility
  - create corresponding symlinks
  - use update-alternatives to allow for lksh as (/usr)/bins/ksh
* Tue Oct  8 2013 tg@mirbsd.org
- fix spelling in mksh-vendor-mkshrc.patch
- split off nōn-SuSE package into OBS home:mirabile/mksh
* Tue Oct  8 2013 gber@opensuse.org
- fix typo in %%postun
* Sun Oct  6 2013 gber@opensuse.org
- apply compiler workarounds for >= 13.1
* Thu Oct  3 2013 gber@opensuse.org
- make sure the patch is only applied on openSUSE/SLE
- %%post/%%postun are not needed for releases after 13.1
* Sat Sep 28 2013 gber@opensuse.org
- add mksh-vendor-mkshrc.patch which adds support for a
  vendor-supplied kshrc which is read by interactive shells before
  $ENV or $HOME/.mkshrc are processed
* Thu Sep 26 2013 gber@opensuse.org
- Initial packaging for openSUSE
