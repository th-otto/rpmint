#
# spec file for package p7zip
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%if 0%{?suse_version} >= 1320 || 0%{?is_opensuse}
# Temporarily disable GUI build as it needs wxWidgets < 3.0 that is no longer
# available in TW
%bcond_with buildgui
%endif
Name:           p7zip
Version:        16.02
Release:        9.3
Summary:        7-zip file compression program
License:        LGPL-2.1-or-later
Group:          Productivity/Archiving/Compression
URL:            http://p7zip.sourceforge.net/
# Update note: RAR sources need to be removed from the package because of the incompatible licence
# Run the following commands after each package update to remove them
# export VERSION=16.02
# wget http://downloads.sourceforge.net/project/p7zip/p7zip/${VERSION}/p7zip_${VERSION}_src_all.tar.bz2
# tar xjvf p7zip_${VERSION}_src_all.tar.bz2
# rm -rf p7zip_${VERSION}/CPP/7zip/Compress/Rar*
# rm -rf p7zip_${VERSION}/DOC/unRarLicense.txt
# tar cjvf p7zip_${VERSION}_src_all-norar.tar.bz2 p7zip_${VERSION}
# rm -rf p7zip_${VERSION}_src_all.tar.bz2
Source:         p7zip_%{version}_src_all-norar.tar.bz2
# Debian gzip-like CLI wrapper for p7zip (the version shipped within the p7zip tarball is too old)
Source1:        https://salsa.debian.org/debian/p7zip/raw/master/debian/scripts/p7zip
Source2:        https://salsa.debian.org/debian/p7zip/raw/master/debian/p7zip.1
Patch1:         CVE-2016-9296.patch
# PATCH-FIX-SUSE bnc#1077978 kstreitova@suse.com -- adjust makefile not to use CPP/7zip/Compress/Rar* files
Patch2:         p7zip_16.02_norar.patch
# PATCH-FIX-UPSTREAM bnc#1077725 kstreitova@suse.com -- fix heap-based buffer overflow in a shrink decoder
Patch3:         p7zip-16.02-CVE-2017-17969.patch
BuildRequires:  fdupes
BuildRequires:  gcc-c++
Suggests:       p7zip-full
%if %{with buildgui}
BuildRequires:  cmake
BuildRequires:  hicolor-icon-theme
BuildRequires:  kf5-filesystem
BuildRequires:  ninja
BuildRequires:  wxWidgets-devel < 3.0
%endif
%ifarch x86_64
BuildRequires:  yasm
%endif

%description
p7zip is a quick port of 7z.exe and 7za.exe (command line version of
7zip, see www.7-zip.org) for Unix. 7-Zip is a file archiver with
highest compression ratio. Since 4.10, p7zip (like 7-zip) supports
little-endian and big-endian machines.

This package provides:
  * %{_bindir}/7zr - a light stand-alone executable that supports only 7z/LZMA/BCJ/BCJ2 archives
  * %{_bindir}/p7zip - a gzip-like wrapper around 7zr

%package full
Summary:        7z and 7za archivers that handle more types of archives than 7zr
Group:          Productivity/Archiving/Compression
Requires:       %{name} = %{version}
Provides:       %{name}:%{_bindir}/7z
Provides:       %{name}:%{_bindir}/7za

%description full
p7zip is a quick port of 7z.exe and 7za.exe (command line version of
7zip, see www.7-zip.org) for Unix. 7-Zip is a file archiver with
highest compression ratio. Since 4.10, p7zip (like 7-zip) supports
little-endian and big-endian machines.

This package provides:
 * %{_bindir}/7z - uses plugins to handle many types of archives
 * %{_bindir}/7za - a stand-alone executable (handles less archive formats than 7z)

This package allows e.g. File Roller or Ark to create/extract 7z archives.

%if %{with buildgui}
%package gui
Summary:        GUI for 7-zip file compression program
Group:          Productivity/Archiving/Compression
Requires:       %{name} = %{version}
Requires:       %{name}-full = %{version}
Requires:       kf5-filesystem
Requires(post): hicolor-icon-theme
Requires(post): update-desktop-files
Requires(postun): hicolor-icon-theme
Requires(postun): update-desktop-files

%description gui
p7zip is a quick port of 7z.exe and 7za.exe (command line version of
7zip, see www.7-zip.org) for Unix. 7-Zip is a file archiver with
highest compression ratio. Since 4.10, p7zip (like 7-zip) supports
little-endian and big-endian machines.
%endif

%package        doc
Summary:        HTML manual for 7-zip
Group:          Productivity/Archiving/Compression
Provides:       %{name}:%{_defaultdocdir}/%{name}/MANUAL
BuildArch:      noarch

%description    doc
This package contains the HTML documentation for 7-Zip.

%prep
%setup -q -n %{name}_%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%ifarch x86_64
cp makefile.linux_amd64_asm makefile.machine
%else
%ifarch ppc64 s390x
cp makefile.linux_amd64 makefile.machine
%else
cp makefile.linux_any_cpu_gcc_4.X makefile.machine
%endif
%endif

sed -i s,444,644,g install.sh
sed -i s,555,755,g install.sh
%if %{with buildgui}
chmod 755 CPP/7zip/CMAKE/generate.sh
rm GUI/kde4/p7zip_compress2.desktop
%endif

perl -pi -e 's/ -s / /' makefile.machine
perl -pi -e 's/(\$\(LOCAL_FLAGS\))/'"%{optflags} -fno-strict-aliasing"' \\\n\t$1/' makefile.machine

# move license files
mv DOC/License.txt DOC/copying.txt .

%build
%if %{with buildgui}
pushd CPP/7zip/CMAKE/
./generate.sh
popd
%make_build OPTFLAGS="%{optflags} -fno-strict-aliasing -Wl,-z,now -fPIC -pie -Wno-error=narrowing" all3 7zG
%else
%make_build OPTFLAGS="%{optflags} -fno-strict-aliasing -Wl,-z,now -fPIC -pie -Wno-error=narrowing" all3
%endif

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
./install.sh \
    %{_bindir} \
    %{_libdir}/%{name} \
    %{_mandir} \
    %{_defaultdocdir}/%{name} \
    %{buildroot}
%if %{with buildgui}
mkdir -p %{buildroot}%{_kf5_servicesdir}/ServiceMenus
for i in 16x16 32x32; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$i/apps
done
install -m644 GUI/kde4/*.desktop %{buildroot}%{_kf5_servicesdir}/ServiceMenus
install -m644 GUI/p7zip_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/p7zip.png
install -m644 GUI/p7zip_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/p7zip.png
chmod 755 %{buildroot}%{_bindir}/p7zipForFilemanager
%endif

# Install p7zip wrapper and its manpage
install -m755 %{SOURCE1} %{buildroot}%{_bindir}/p7zip
install -m644 %{SOURCE2} %{buildroot}%{_mandir}/man1/p7zip.1
# Remove a mention of the p7zip-rar package that we don't have
sed -i 's/RAR (if the non-free p7zip-rar package is installed)//g' %{buildroot}%{_mandir}/man1/p7zip.1

# remove superfluous DOC directory
mv %{buildroot}%{_defaultdocdir}/%{name}/DOC/* %{buildroot}%{_defaultdocdir}/%{name}
rmdir %{buildroot}%{_defaultdocdir}/%{name}/DOC/

%fdupes -s %{buildroot}

%check
%if ! 0%{?qemu_user_space_build}
%make_build test
%make_build test_7z
%make_build test_7zr
%endif

%if %{with buildgui}
%post gui
%desktop_database_post
%icon_theme_cache_post

%postun gui
%desktop_database_postun
%icon_theme_cache_postun
%endif

%files
%license copying.txt License.txt
%doc ChangeLog
%doc %{_defaultdocdir}/%{name}
%exclude %{_defaultdocdir}/%{name}/MANUAL
%{_bindir}/7zr
%{_bindir}/p7zip
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/7zr
%{_mandir}/man1/7zr.1%{?ext_man}
%{_mandir}/man1/p7zip.1%{?ext_man}

%files full
%{_bindir}/7z
%{_bindir}/7za
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/7z
%{_libdir}/%{name}/7za
%{_libdir}/%{name}/7z.so
%{_libdir}/%{name}/7zCon.sfx
%{_mandir}/man1/7z.1%{?ext_man}
%{_mandir}/man1/7za.1%{?ext_man}

%if %{with buildgui}
%files gui
%{_bindir}/7zG
%{_bindir}/p7zipForFilemanager
%{_libdir}/%{name}/7zG
%dir %{_libdir}/%{name}/Lang
%{_libdir}/%{name}/Lang/*.txt
%{_libdir}/%{name}/Lang/en.ttt
%{_datadir}/icons/hicolor/*/apps/p7zip.png
%dir %{_kf5_servicesdir}/ServiceMenus
%{_kf5_servicesdir}/ServiceMenus/*.desktop
%endif

%files doc
%doc %{_defaultdocdir}/%{name}/MANUAL

%changelog
* Tue Mar 10 2020 Martin Liška <mliska@suse.cz>
- Add -Wno-error=narrowing in order to fix boo#1158195.
- Use %%make_build.
* Tue Oct 15 2019 Yifan Jiang <yfjiang@suse.com>
- Update the Source1 and Source2 links to the latest upstream URL.
* Tue May 15 2018 kstreitova@suse.com
- p7zip package now provides 7zr binary only. 7z and 7za binaries
  are moved to the new pzip-full subpackage [bsc#899627]
- add a new p7zip-doc subpackage (contains HTML manual)
- pack /usr/bin/p7zip script (gzip-like CLI wrapper for p7zip)
  [bsc#965140]
- 7zG requires 7z.so - pzip-gui should require pzip-full package
- remove unused Codecs dir
- tweak %%descriptions
- pack documentation and licenses properly (avoid duplications)
- use %%license instead of %%doc [bsc#1082318]
- run test_7zr test
- run spec-cleaner
* Tue Feb  6 2018 kstreitova@suse.com
- add p7zip-16.02-CVE-2017-17969.patch to fix a heap-based buffer
  overflow in a shrink decoder [bnc#1077725], [CVE-2017-17969]
* Mon Jan 29 2018 kstreitova@suse.com
- remove CPP/7zip/Compress/Rar* files from the tar archive as they
  have incompatible license [bnc#1077978]
  * also remove DOC/unRarLicense.txt
  * add p7zip_16.02_norar.patch to adjust makefile according to it
  * remove no longer used Codecs
* Thu Aug 10 2017 mimi.vx@gmail.com
- remove 7zr manpage, fixes boo#899627
* Tue Feb  7 2017 dimstar@opensuse.org
- Explicitly package %%{_docdir}/%%{name} to fix build with RPM 4.13.
* Thu Nov 24 2016 idonmez@suse.com
- Add CVE-2016-9296.patch to fix a null pointer dereference
  problem (CVE-2016-9296)
* Fri Jul 15 2016 joerg.lorenzen@ki.tng.de
- Update to version 16.02
  - From Windows version of 7-Zip 16.02:
  - The BUG in 16.00 - 16.01 was fixed: 7-Zip mistakenly reported
    the warning "There are some data after the end of the payload
    data" for split archives.
- Version 16.01 (never published)
  - From Windows version of 7-Zip 16.01:
  - The bugs in SWM (WIM), EXE (PE) and CHM code were fixed.
  - There are some internal changes in source code for better
    compatibility with VS2015 C++ compiler.
- Version 16.00 (never published)
  - Better support for OpenBsd (CPP/Windows/System.cpp), thanks Josh
    (https://sourceforge.net/p/p7zip/discussion/383043/thread/ee32dcd8/?limit=25#c322).
  - From Windows version of 7-Zip 16.00:
  - 7-Zip now can extract multivolume ZIP archives (z01, z02,
    ... , zip).
  - Some fixed bugs:
  - bzip2 decoder -mmt2 reported E_FAIL
    (for k_My_HRESULT_WritingWasCut case), if we extract
    partial file.
  - 7z solid update (hang in break).
  - sha1 worked incorrectly for call after call with ((size & 3) != 0).
  - 7z update bcj bugs were fixed.
  - Split (aaa.001) fixed.
  - iso loop fix.
  - rar4 multivol -stdin kpidSize.
  - Drag and drop 1<2.txt.
  - Memory access violation fix.
- Removed CVE-2016-2334.patch and CVE-2016-2335.patch, fixed upstream.
* Fri May 13 2016 mpluskal@suse.com
- Temporarily disable gui building
* Fri May 13 2016 idonmez@suse.com
- Fix security issues:
  - CVE-2016-2334: 7zip HFS+ NArchive::NHfs::CHandler::ExtractZlibFile
    Code Execution Vulnerability (boo#979822)
  - CVE-2016-2335: 7zip UDF CInArchive::ReadFileItem Code Execution
    Vulnerability (boo#979823)
  (CVE-2016-2334.patch, CVE-2016-2335.patch)
* Sat Apr 30 2016 joerg.lorenzen@ki.tng.de
- Build 7zG (gui for p7zip) and added subpackage p7zip-gui for
  openSUSE >= 13.2 and Leap 42.1.
* Thu Apr 21 2016 joerg.lorenzen@ki.tng.de
- Update to version 15.14.1
  - Patch #32 Compiling in OS X fails with p7zip_15.14.
- Fixed spec file to build with copied makefile.linux_amd64_asm
  for arch x86-64 and added required yasm as BuildRequires.
* Mon Mar 14 2016 idonmez@suse.com
- Update to version 15.14
  * Based on 7-zip 15.14 release
  * Build fixes
  * All the fixes from 7-zip 15.14, see the included ChangeLog
- Drop p7zip-CVE-2015-1038.patch, upstream.
* Tue Dec 15 2015 idonmez@suse.com
- Enable PIE & LD_BIND_NOW security features
- Package all the text documentation
* Thu Oct 22 2015 idonmez@suse.com
- Update to version 15.09
  * Based on 7-zip 15.09 release
  * 7-Zip now can extract ext2 and multivolume VMDK images.
  * 7-Zip now can extract ext3 and ext4 (Linux file system) images.
  * 7-Zip now can extract GPT images and single file QCOW2, VMDK, VDI images.
  * 7-Zip now can extract solid WIM archives with LZMS compression.
  * 7-Zip now can extract RAR5 archives.
  * 7-Zip now doesn't sort files by type while adding to solid 7z archive.
    new -mqs switch to sort files by type while adding to solid 7z archive.
  * 7-Zip now can create 7z, xz and zip archives with 1536 MB dictionary for LZMA/LZMA2.
  * 7-Zip now can extract .zipx (WinZip) archives that use xz compression.
- Refresh p7zip-CVE-2015-1038.patch
* Tue Jun 23 2015 pgajdos@suse.com
- fixed CVE-2015-1038 [bnc#912878]
  + p7zip-CVE-2015-1038.patch
* Fri Mar  6 2015 joerg.lorenzen@ki.tng.de
- update to 9.38.1
  - bug #145 "p7zip crashes while moving memory in MoveItems"
* Mon Feb  9 2015 vcizek@suse.com
- update to 9.38
  - patch #23 fixes "7z with unicode file name with surrogate pair is not handled well in Linux"
  - bug #139 "password from commanline is visible in processes list"
    Now the characters of the password are replaced with *.
  - bug#138 If you extract the password with # program crashes
    7z now supports long password in RAR 3 and 4.
  - 7-Zip could ignore some options when you created ZIP archives.
    For example, it could use ZipCrypto cipher instead of AES-256.
  - New -mf=FilterID switch to specify compression filter. Examples:
    7z a -mf=bcj2 a.7z a.tar
    7z a -mf=delta:4 a.7z a.wav
    7z a -mf=bcj a.tar.xz a.tar
  - New class FString for file names at file systems.
  - Speed optimization in CRC code for big-endian CPUs.
  - Speed optimizations in AES code for Intel's 32nm CPUs.
  - Speed optimizations in CRC calculation code for Intel's Atom CPUs.
  - bug with multi archives which are links.
  - #3283518 : Asm/x{32,64}/7zCrcT8U.asm introduces executable stack
* Sat Oct  1 2011 crrodriguez@opensuse.org
- test suite segfaults on qemu-arm, we will see if it is a bug
  in p7zip or a glitch in qemu later.
* Wed Sep 28 2011 idonmez@suse.com
- Enable assembly support for x86-64
- Update to version 9.20
  - From Windows version of 7-zip 9.20, What's new after 7-Zip 4.65 (2009-02-03):
  - 7-Zip now supports LZMA2 compression method.
  - 7-Zip now can update solid .7z archives.
  - 7-Zip now supports XZ archives.
  - 7-Zip now supports PPMd compression in ZIP archives.
  - 7-Zip now can unpack NTFS, FAT, VHD, MBR, APM, SquashFS, CramFS, MSLZ archives.
  - 7-Zip now can unpack GZip, BZip2, LZMA, XZ and TAR archives from stdin.
  - 7-Zip now can unpack some TAR and ISO archives with incorrect headers.
  - 7-Zip now supports files that are larger than 8 GB in TAR archives.
  - NSIS and WIM support was improved.
  - Partial parsing for EXE resources, SWF and FLV.
  - The support for archives in installers was improved.
  - 7-Zip now can stores NTFS file timestamps to ZIP archives.
  - Speed optimizations in PPMd codec.
  - Speed optimizations in CRC calculation code for Intel's Atom CPUs.
  - New -scrc switch to calculate total CRC-32 during extracting / testing.
  - 7-Zip File Manager now doesn't use temp files to open nested archives stored without compression.
  - Disk fragmentation problem for ZIP archives created by 7-Zip was fixed.
  - Some bugs were fixed.
  - New localizations: Hindi, Gujarati, Sanskrit, Tatar, Uyghur, Kazakh.
  - Not in p7zip : Speed optimizations in AES code for Intel's 32nm CPUs.
  - From Windows version of 7-zip 9.17
  - Disk fragmentation problem for ZIP archives created by 7-Zip was fixed.
    Notes: 7-Zip now uses 4 MB RAM buffer as file cache, when you create ZIP archives.
    It reduces the number of Move_File_Position and Write_to_File operations.
  - From Windows version of 7-zip 9.18
  - 7-Zip now can unpack SquashFS and CramFS filesystem images.
  - 7-Zip now can unpack some TAR and ISO archives with incorrect headers.
  - Some bugs were fixed.
  - From Windows version of 7-zip 9.16
  - 7-Zip now supports files that are larger than 8 GB in TAR archives.
  - NSIS support was improved :
  - 7-Zip now supports BZip2 method in NSIS installers.
  - 7-Zip now can extract identical files from NSIS installers.
  - Some bugs were fixed.
  - New localizations: Hindi, Gujarati, Sanskrit.
  - From Windows version of 7-zip 9.15
  - Some bugs were fixed.
  - New localization: Tatar
  - From Windows version of 7-zip 9.14
  - WIM support was improved. 7-Zip now can create WIM archives without compression.
  - sf#3069545 "kSignatureDummy?" fixed
* Wed May 25 2011 chris@computersalat.de
- fix deps
  o no fdupes on suse_version < 1100 (SLES9, SLE10)
- remove Author from description
* Mon May 31 2010 freespacer@gmx.de
- update to version 9.13
  * From Windows version of 7-zip 9.12
  - Some bugs were fixed.
  * #2863580 "Crash in Rar decoder on a corrupted file" fixed
  * #2860898 "Dereferencing a zero pointer in cab handler" fixed
  * #2860679 "Division by zero in cab decoder" fixed
- update to version 9.12
  * From Windows version of 7-zip 9.12
  - ZIP / PPMd compression ratio was improved in Maximum and Ultra modes.
  - The BUG in 7-Zip 9.* beta was fixed: LZMA2 codec didn't work,
    if more than 10 threads were used (or more than 20 threads in some modes).
  * makefile.openbsd is now compatible with OpenBSD ports tree.
    (thanks to jggimi)
  * cmake projects added.
  * 7zFM and 7zG can be built on MacOSX but these ports are in very alpha stage.
    make app to build p7zip.app (p7zip for MacOSX)
- update to version 9.11 (never published)
  * From Windows version of 7-zip 9.11
  - 7-Zip now supports PPMd compression in .ZIP archives.
  - Speed optimizations in PPMd codec.
  - The support for archives in installers was improved.
  - Some bugs were fixed.
- update to version 9.10 (never published)
  * From Windows version of 7-zip 9.05 to 9.10
  - 7-Zip now can unpack Apple Partition Map (APM) disk images.
  - 7-Zip now can unpack MSLZ archives.
  - Partial parsing for EXE resources, SWF and FLV.
  - Some bugs were fixed.
  * p7zip can now use hugetlbfs on Linux (thank to Joachim Henke)
    Like with the Windows large pages, this gives a nice speedup,
    when running memory intensive operations.
  * p7zip now uses UTF8 (kCFStringNormalizationFormD) On MacOSX
    fixes  #2831266 "p7zip can't find NFC Unicode  filename in OSX Terminal"
    and    #2976169 "German Umlauts Failure"
- update to version 9.05 (never published)
  * p7zip now uses precompiled header with gcc 4
- remove obsolete patch (gcc_missing_include.patch)
- renew patch (install.patch)
* Thu Jun 18 2009 freespacer@gmx.de
- update to version 9.04
  * 7-Zip now can update solid .7z archives
  * 7-Zip now supports LZMA2 compression method
  * 7-Zip now supports XZ archives
  * 7-Zip now can unpack NTFS, FAT, VHD and MBR archives
  * 7-Zip now can unpack GZip, BZip2, LZMA, XZ and TAR archives from stdin
  * New -scrc switch to calculate total CRC-32 during extracting / testing
  * Some bugs were fixed
  * #2799966 " A newly created 7z archive (by p7zip 4.65) is broken and cannot be unpacked / listed / tested"
    Fixed: now "7za a -mx=9 archive.7z directory" creates a good archive even
    if there are a lot of executable files
  * Fixed: the RAM size was reported incorrectly on MacOSX 64bits (with 2Gb+ RAM)
  * #2798023 "segfault handling very large multivolume .7z file"
    p7zip now displays the following error "Error: Too many open files"
    if you don't have enough rights to open all the splitted files
    (on Linux: ulimit -n)
  - included update from 4.65
  * The bug in 7-Zip 4.63 was fixed: 7-Zip could not decrypt .ZIP archives encrypted with WinZip-AES method
  * 7-Zip now can unpack ZIP archives encrypted with PKWARE-AES
  * Some bugs were fixed
  * Fixed: the RAM size was reported incorrectly on MacOSX 64bits
  * Fixed: makefile.linux_amd64_asm_icc
  * DJGPP: makefile.djgpp becomes makefile.djgpp_old
  * DJGPP: makefile.djgpp_watt added (thank to Rugxulo)
  * you can now compile 7za with a cmake project (see README)
  - included update from 4.61
  * 7-Zip now supports LZMA compression for .ZIP archives
  * Ask for password twice when creating encrypted archive
  * 7zG added (read GUI/readme.txt)
  * p7zip didn't use the BCJ /BCJ2 filters for executables (:
  * makefile.linux_amd64_asm_icc added (tested with Intel Compiler 11 on Ubuntu 8.04 x64)
  * 7-Zip now can unpack UDF, XAR and DMG/HFS archives
  * It's allowed to use -t switch for "list" and "extract" commands
  * Bug: wrong timestamp for files extracted from .zip or .rar archives
* Mon Jun 30 2008 mkoenig@suse.de
- update to version 4.58
  * Some speed optimizations
  * 7-Zip now can unpack .lzma archives
  * Unicode (UTF-8) support for filenames in .ZIP archives
  * Now it's possible to store file creation time in 7z and
    ZIP archives (-mtc switch)
  * 7-Zip now can unpack multivolume RAR archives created with
    "old style volume names" scheme and names *.001, *.002, ...
  * Now it's possible to use -mSW- and -mSW+ switches instead of
  - mSW=off and -mSW=on
* Thu Feb 28 2008 mkoenig@suse.de
- update to version 4.57
  * some minor bugfixes
* Tue Aug  7 2007 crrodriguez@suse.de
- update to version 4.51
  - fix built of test_emul
  - contrib/gzip-like_CLI_wrapper_for_7z/p7zip now supports commands like :
    p7zip -- -name
    p7zip "file name"
    p7zip file1 file2 file3
    p7zip -d file1.7z file2.7z file3.7z
  - some code cleanup
- run make test in the rpm check section
* Mon Jul  9 2007 mkoenig@suse.de
- update to version 4.48
  * bugfixes
* Mon Feb  5 2007 mkoenig@suse.de
- update to version 4.44:
  * fixes in the help displayed by 7za/7z/7zr.
  * code cleanup: remove of mySetModuleFileNameA (and its memory
    leak), GetModuleFileName ...
  Bugfixes:
  * in the plugins of 7z, the "Utf16" state was always off.
  * support for directory names that are not encoded
    with the current locale.
  * p7zip can now restore a symbolic link from a Zip archive
  * small fix in the output of the script install.sh
  * Extracting large directories takes quadratic time
  * Client7z added.
* Thu Dec 14 2006 mkoenig@suse.de
- update to version 4.43:
  * 7-Zip now can use multi-threading mode for compressing to
    .ZIP archives.
  * ZIP format supporting was improved.
  * 7-Zip now supports WinZip-compatible AES-256 encryption for
    .ZIP archives.
  * 7-Zip now uses order list (list of extensions) for files
    sorting for compressing to .7z archives.
  * 7-Zip now restores modification time of folders during .7z
    archives extracting.
* Thu Jun 29 2006 kssingvo@suse.de
- fixed specfile (makefile part) (bugzilla#187320)
* Wed Jun 21 2006 kssingvo@suse.de
- update to version 4.42
* Tue Apr 11 2006 kssingvo@suse.de
- update to version 4.37
* Fri Mar  3 2006 kssingvo@suse.de
- initial version
