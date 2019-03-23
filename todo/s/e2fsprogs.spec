Summary       : Utilities for managing the second extended (ext2) filesystem.
Name          : e2fsprogs
Version       : 1.27
Release       : 2
Copyright     : GPL
Group         : System Environment/Base

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://e2fsprogs.sourceforge.net/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://download.sourceforge.net/pub/sourceforge/e2fsprogs/e2fsprogs-%{version}.tar.gz
Patch0: e2fsprogs-1.27-mint.patch


%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in second
extended (ext2) filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters) and most of the other core ext2fs
filesystem utilities.

You should install the e2fsprogs package if you are using any ext2
filesystems (if you're not sure, you probably should install this
package).

%package devel
Summary       : Ext2 filesystem-specific static libraries and headers.
Group         : Development/Libraries
Requires      : e2fsprogs

%description devel
E2fsprogs-devel contains the libraries and header files needed to
develop second extended (ext2) filesystem-specific programs.

You should install e2fsprogs-devel if you want to develop ext2
filesystem-specific programs.  If you install e2fsprogs-devel, you'll
also need to install e2fsprogs.


%prep
%setup -q
%patch0 -p1 -b .mint


%build
CFLAGS="${RPM_OPT_FLAGS} -m68020 -DE2FSPROGS_WRAPPER -DHAVE_EXT2_IOCTLS -D_GNU_SOURCE" \
./configure \
	--build=m68k-atari-mint \
	--prefix=%{_prefix}

make libs progs docs


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

export PATH=/sbin:$PATH
make install install-libs \
	DESTDIR="${RPM_BUILD_ROOT}" \
	mandir=%{_prefix}/share/man \
	root_sbindir=/sbin \
	root_libdir=/lib

stack --fix=80k ${RPM_BUILD_ROOT}/sbin/* || :
stack --fix=80k ${RPM_BUILD_ROOT}%{_prefix}/sbin/* || :

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post devel
if [ -x /sbin/install-info ]; then
   /sbin/install-info /usr/info/libext2fs.info.gz /usr/info/dir
fi

%postun devel
if [ $1 = 0 -a -x /sbin/install-info ]; then
   /sbin/install-info --delete /usr/info/libext2fs.info.gz /usr/info/dir
fi


%files
%defattr(-,root,root)
%doc COPYING README RELEASE-NOTES

/sbin/badblocks
/sbin/debugfs
/sbin/dumpe2fs
/sbin/e2fsck
/sbin/e2image
/sbin/e2label
/sbin/fsck
/sbin/fsck.ext2
/sbin/mke2fs
/sbin/mkfs.ext2
/sbin/resize2fs
/sbin/tune2fs
%{_prefix}/share/man/man8/badblocks.8*
%{_prefix}/share/man/man8/debugfs.8*
%{_prefix}/share/man/man8/dumpe2fs.8*
%{_prefix}/share/man/man8/e2fsck.8*
%{_prefix}/share/man/man8/e2image.8*
%{_prefix}/share/man/man8/e2label.8*
%{_prefix}/share/man/man8/fsck.8*
%{_prefix}/share/man/man8/fsck.ext2.8*
%{_prefix}/share/man/man8/mke2fs.8*
%{_prefix}/share/man/man8/mkfs.ext2.8*
%{_prefix}/share/man/man8/resize2fs.8*
%{_prefix}/share/man/man8/tune2fs.8*

%{_prefix}/sbin/mklost+found
%{_prefix}/share/man/man8/mklost+found.8*

%{_prefix}/bin/chattr
%{_prefix}/bin/lsattr
%{_prefix}/bin/uuidgen
%{_prefix}/share/man/man1/chattr.1*
%{_prefix}/share/man/man1/lsattr.1*
%{_prefix}/share/man/man1/uuidgen.1*

%files devel
%defattr(-,root,root)
%{_prefix}/bin/compile_et
%{_prefix}/bin/mk_cmds
%{_prefix}/share/man/man1/compile_et.1*

%{_prefix}/include/e2p
%{_prefix}/include/et
%{_prefix}/include/ext2fs
%{_prefix}/include/ss
%{_prefix}/include/uuid
%{_prefix}/lib/libcom_err.a
%{_prefix}/lib/libe2p.a
%{_prefix}/lib/libext2fs.a
%{_prefix}/lib/libss.a
%{_prefix}/lib/libuuid.a
%{_prefix}/share/et
%{_prefix}/share/ss
%{_prefix}/share/man/man3/*.3*
%{_prefix}/info/libext2fs.info*


%changelog
* Wed Nov 19 2003 Frank Naumann <fnaumann@freemint.de>
- reworked mint_io.c, incorporated the changes from the mint cvs
  version with the patches from Standa; mke2fs should now
  work as expected

* Thu Apr 04 2002 Frank Naumann <fnaumann@freemint.de>
- updated to 1.27

* Wed Oct 25 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 1.19
- completly rewritten device I/O layer, now transparent;
  badblocks, e2label work now too

* Mon Jun 13 2000 Frank Naumann <fnaumann@freemint.de>
- small patch to accept all DOS partitions

* Mon Mar 27 2000 Frank Naumann <fnaumann@freemint.de>
- rebuild against new MiNTLib 0.55 and without FPU dependency

* Fri Sep 03 1999 Frank Naumann <fnaumann@freemint.de>
- enhanced FreeMiNT patches, drives with physical sector size
  greater than 512 bytes work now

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
