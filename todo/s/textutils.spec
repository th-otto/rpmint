Summary       : GNU Text Utilities
Summary(de)   : GNU-Text-Hilfsmittel
Summary(fr)   : Utilitaires texte de GNU
Summary(tr)   : GNU metin iþleme araçlarý
Name          : textutils
Version       : 2.0.11
Release       : 2
Copyright     : GPL
Group         : Applications/Text

Packager      : Guido Flohr <guido@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/textutils/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://alpha.gnu.org/gnu/fetish/textutils-%{version}.tar.gz
Patch0: textutils-2.0.11-security.patch
Patch1: textutils-2.0.11-mint.patch
Patch2: textutils-2.0.11-getopt.patch
Patch3: textutils-2.0.11-mint-physmem.patch


%description
These are the GNU text file (actually, file contents) processing
utilities.  Most of these programs have significant advantages over
their Unix counterparts, such as greater speed, additional options,
and fewer arbitrary limits.
The programs in this package are: cat, cksum, comm, csplit, cut,
expand, fmt, fold, head, join, md5sum, nl, od, paste, pr, ptx, sort,
split, sum, tac, tail, tr, tsort, unexpand, uniq, and wc.

Bug Reports:
============
    <bug-textutils@gnu.org>

Authors:
========
    Jim Meyering <meyering@ascend.com>
    François Pinard <pinard@iro.umontreal.com>
    and others (use option "--version" to learn about the actual author)
    
%description -l de
Dies sind die GNU-Textdatei- (oder, richtiger gesagt: Dateiinhalts-) 
Hilfsmittel. Die meisten dieser Programme haben bedeutende Vorteile 
gegenüber ihren Unix-Pendants, wie größere Geschwindigkeit, mehr Optionen
und weniger willkürliche Limits.
Die Programme in diesem Paket sind: cat, cksum, comm, csplit, cut,
expand, fmt, fold, head, join, md5sum, nl, od, paste, pr, ptx, sort,
split, sum, tac, tail, tr, tsort, unexpand, uniq und wc.

Fehlerberichte:
===============
    <bug-textutils@gnu.org>

Autoren:
========
    Jim Meyering <meyering@ascend.com>
    François Pinard <pinard@iro.umontreal.com>
    und andere (die Option "--version" spuckt den Namen des Autors aus)


%prep
%setup -q
%patch0 -p1 -b .sec
%patch1 -p1 -b .mint
%patch2 -p1 -b .getopt
%patch3 -p1 -b .physmem


%build
# The configure option --with-included-gettext is needed because the
# installed libintl.a may conflict with the libc (because it uses
# fstat).  The mktime test fails on slow machines because the code
# times out before finished (although the test succeeds).
ac_cv_func_working_mktime=yes \
ac_cv_glibc=yes \
ac_cv_gnu_library=yes \
CFLAGS="$RPM_OPT_FLAGS -Dunix" \
./configure \
	--prefix=%{_prefix} \
	--enable-nls
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	localedir=${RPM_BUILD_ROOT}%{_prefix}/share/locale \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

# move some files
mkdir -p ${RPM_BUILD_ROOT}/bin
for f in cat sort; do
	mv ${RPM_BUILD_ROOT}%{_prefix}/bin/$f ${RPM_BUILD_ROOT}/bin/$f
done

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* || :

# This ridiculously large stacksize is needed because cksum needs
# a buffer of 64k allocated from the stack.
stack --size=160k ${RPM_BUILD_ROOT}%{_prefix}/bin/cksum
stack --size=80k  ${RPM_BUILD_ROOT}/bin/sort
stack --size=80k  ${RPM_BUILD_ROOT}%{_prefix}/bin/tsort
stack --size=80k  ${RPM_BUILD_ROOT}%{_prefix}/bin/wc

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/textutils*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/textutils.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/textutils.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc NEWS README
/bin/*
%{_prefix}/bin/*
%{_prefix}/info/textutils*
%{_prefix}/share/locale/*/*/*
%{_prefix}/share/man/man*/*


%changelog
* Fri Jun 27 2003 Frank Naumann <fnaumann@freemint.de>
- special physmem detection for FreeMiNT/TOS; don't
  default to 64 MB memory

* Mon Sep 17 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0.11

* Tue Apr 10 2000 Guido Flohr <guido@freemint.de>
- upgrade to 2.0
- install sort and cat in /bin, not in/usr/bin
- built against MiNTLib 0.55.2
- work around a bug in MiNTLib 0.55.2 that defines unix to an empty string
- added credits

* Thu Aug 12 1999 Guido Flohr <guido@freemint.de>
- changed vendor to Sparemint

* Sun Jul 18 1999 Guido Flohr <guido@freemint.de>
- built against MiNTLib 0.52.3a
- increased stack size for sort from 10k to 64k, for wc from default
  to 64k
