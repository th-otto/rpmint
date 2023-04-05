Summary       : The GNU data compression program.
Summary(de)   : Das GNU Datenkompressionsprogramm.
Name          : gzip
Version       : 1.3
Release       : 1
Copyright     : GPL
Group         : Applications/File

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gzip.org/

Prereq        : /sbin/install-info
Requires      : mktemp

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://alpha.gnu.org/gnu/gzip/gzip-%{version}.tar.gz
Patch0: gzip-1.3-mktemp.patch
Patch1: gzip-1.2.4-zforce.patch
Patch2: gzip-1.2.4a-dirinfo.patch
Patch3: gzip-1.3-stderr.patch
Patch4: gzip-1.3-zgreppipe.patch
Patch5: gzip-1.3-mint.patch
Patch6: gzip-1.3-mint-getopt.patch


%description
The gzip package contains the popular GNU gzip data compression
program.  Gzipped files have a .gz extension.  

Gzip should be installed on your FreeMiNT system, because it is a
very commonly used data compression program.

%description -l de
Das Paket gzip enthält das beliebte Datenkompressionsprogramm gzip.  
Ge'gzip'te Dateien haben .gz als Namenserweiterung.  

Gzip sollte auf Ihrem FreeMiNT-System installiert werden, weil es ein
sehr weit verbreitetes Datenkompressionsprogramm ist.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .mint
%patch6 -p1 -b .mint-getopt


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--bindir=/bin
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	bindir=${RPM_BUILD_ROOT}/bin

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
ln -sf ../../bin/gzip ${RPM_BUILD_ROOT}%{_prefix}/bin/gzip
ln -sf ../../bin/gunzip ${RPM_BUILD_ROOT}%{_prefix}/bin/gunzip

for i in zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore ; do
    mv ${RPM_BUILD_ROOT}/bin/$i ${RPM_BUILD_ROOT}%{_prefix}/bin/$i
done

strip ${RPM_BUILD_ROOT}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

stack --fix=64k ${RPM_BUILD_ROOT}/bin/* ||:
stack --fix=64k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/gzip.info*


cat > ${RPM_BUILD_ROOT}%{_prefix}/bin/zless <<EOF
#!/bin/sh
/bin/zcat "\$@" | %{_prefix}/bin/less
EOF
chmod 755 ${RPM_BUILD_ROOT}%{_prefix}/bin/zless


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/gzip.info.gz %{_prefix}/info/dir 

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/gzip.info.gz %{_prefix}/info/dir
fi


%files
%doc NEWS README AUTHORS ChangeLog THANKS TODO
/bin/*
%{_prefix}/bin/*
%{_prefix}/info/gzip.info*
%{_prefix}/share/man/*/*


%changelog
* Fri Sep 07 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.3

* Thu Feb 03 2000 Edgar Aichinger <eaiching@t0.or.at>
- fixed symlink bug in specfile
- changed location of manpages to /usr/share/man
- added german summary/description (release 4)

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
