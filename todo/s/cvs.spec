Summary       : A version control system.
Name          : cvs
Version       : 1.11.1p1
Release       : 1
Group         : Development/Tools
Copyright     : GPL

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.cvshome.org/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.cvshome.org/pub/cvs-%{version}/cvs-%{version}.tar.gz
Source1: cederqvist-1.11.1p1.html.tgz


%description
CVS means Concurrent Version System; it is a version control
system which can record the history of your files (usually,
but not always, source code). CVS only stores the differences
between versions, instead of every version of every file
you've ever created. CVS also keeps a log of who, when and
why changes occurred, among other aspects.

CVS is very helpful for managing releases and controlling
the concurrent editing of source files among multiple
authors. Instead of providing version control for a
collection of files in a single directory, CVS provides
version control for a hierarchical collection of
directories consisting of revision controlled files.

These directories and files can then be combined together
to form a software release.

Install the cvs package if you need to use a version
control system.


%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix}

make LDFLAGS=-s

tar xzf %{SOURCE1}
mv cederqvist-1.11.1p1.html html


%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{_prefix} install install-info

# make q-funk happy
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_prefix}/share/

gzip -9nf $RPM_BUILD_ROOT%{_prefix}/share/man/*/*
gzip -9nf $RPM_BUILD_ROOT%{_prefix}/info/cvs*

strip $RPM_BUILD_ROOT%{_prefix}/bin/cvs
stack --fix=512k $RPM_BUILD_ROOT%{_prefix}/bin/cvs || :


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_prefix}/info/cvs.info.gz %{_prefix}/info/dir --entry="* cvs: (cvs).          A version control system for multiple developers."
/sbin/install-info %{_prefix}/info/cvsclient.info.gz %{_prefix}/info/dir --entry="* cvsclient: (cvsclient).                       The CVS client/server protocol."

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete %{_prefix}/info/cvs.info.gz %{_prefix}/info/dir --entry="* cvs: (cvs).		A version control system for multiple developers."
	/sbin/install-info --delete %{_prefix}/info/cvsclient.info.gz %{_prefix}/info/dir --entry="* cvsclient: (cvsclient).                       The CVS client/server protocol."
fi


%files
%defattr(-,root,root)
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README
%doc html/ doc/*.ps
%{_prefix}/bin/cvs
%{_prefix}/bin/cvsbug
%{_prefix}/bin/rcs2log
%{_prefix}/info/cvs*
%{_prefix}/share/cvs
%{_prefix}/share/man/man1/cvs.1.gz
%{_prefix}/share/man/man5/cvs.5.gz
%{_prefix}/share/man/man8/cvsbug.8.gz


%changelog
* Mon Aug 20 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.11.1p1

* Thu Dec 05 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 1.11
- linked against bugfixed MiNTLib (fix the cannot parse date problem)

* Wed May 30 2000 Frank Naumann <fnaumann@freemint.de>
- recompiled against MiNTLib 0.55
- increased stack size

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
