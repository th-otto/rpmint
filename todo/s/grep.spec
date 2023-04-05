Summary       : The GNU versions of grep pattern matching utilities.
Name          : grep
Version       : 2.4.2
Release       : 1
Copyright     : GPL
Group         : Applications/Text

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : ftp://ftp.gnu.org/pub/gnu/grep/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.gz
Patch0: grep-2.4.2-i18n.patch
Patch1: grep-2.4.2-mint.patch


%description
The GNU versions of commonly used grep utilities.  Grep searches
through textual input for lines which contain a match to a specified
pattern and then prints the matching lines.  GNU's grep utilities
include grep, egrep and fgrep.

You should install grep on your system, because it is a very useful
utility for searching through text.


%prep
%setup -q
%patch0 -p1 -b .i18n
%patch1 -p1 -b .mint


%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=/
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}

stack --fix=128k ${RPM_BUILD_ROOT}/bin/* || :

# compress manuals
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/*.info
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/*/*

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/


%post
/sbin/install-info %{_prefix}/info/grep.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_prefix}/info/grep.info.gz %{_prefix}/info/dir
fi


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog
/bin/*
%{_prefix}/info/grep.info*
%{_prefix}/share/locale/*/LC_MESSAGES/grep*
%{_prefix}/share/man/*/*


%changelog
* Tue Mar 20 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.4.2

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
