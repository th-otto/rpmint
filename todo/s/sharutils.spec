Summary       : The GNU shar utilities for packaging and unpackaging shell archives.
Name          : sharutils
Version       : 4.2.1
Release       : 1
Copyright     : GPL
Group         : Applications/Archiving

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/sharutils/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://prep.ai.mit.edu/pub/gnu/sharutils/sharutils-%{version}.tar.gz
Patch1: sharutils-4.2-gmo.patch
Patch2: sharutils-4.2-man.patch
Patch3: sharutils-4.2-po.patch
Patch4: sharutils-4.2-share.patch
Patch5: sharutils-4.2-uudecode.patch


%description
The sharutils package contains the GNU shar utilities, a set of tools
for encoding and decoding packages of files (in binary or text format)
in a special plain text format called shell archives (shar).  This
format can be sent through e-mail (which can be problematic for regular
binary files).  The shar utility supports a wide range of capabilities
(compressing, uuencoding, splitting long files for multi-part
mailings, providing checksums), which make it very flexible at
creating shar files.  After the files have been sent, the unshar tool
scans mail messages looking for shar files.  Unshar automatically
strips off mail headers and introductory text and then unpacks the
shar files.

Install sharutils if you send binary files through e-mail.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix}
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install install-man \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/{sharutils*,remsync*}

# fix jp location
mv ${RPM_BUILD_ROOT}%{_prefix}/share/locale/ja_JP.EUC \
	${RPM_BUILD_ROOT}%{_prefix}/share/locale/ja


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/sharutils.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/sharutils.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc AUTHORS BACKLOG COPYING NEWS README THANKS TODO
%{_prefix}/bin/*
%{_prefix}/info/*info*
%{_prefix}/share/man/*/*
%{_prefix}/share/locale/*/*/*


%changelog
* Thu Sep 06 2001 Frank Naumann <fnaumann@freemint.de>
- initial Sparemint release
