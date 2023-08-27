%define pkgname file

%rpmint_header

Summary:        A Tool to Determine File Types
Name:           %{crossmint}%{pkgname}
Version:        5.45
Release:        2
License:        BSD-2-Clause
Group:          Productivity/File utilities

Packager:       %{packager}
URL:            http://www.darwinsys.com/file/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: ftp://ftp.astron.com/pub/%{pkgname}/%{pkgname}-%{version}.tar.gz
Source1: patches/automake/mintelf-config.sub
Source2: patches/file/file-zisofs.magic

Patch0:  patches/file/file-5.19-misc.dif
Patch1:  patches/file/file-4.24-autoconf.dif
Patch2:  patches/file/file-5.14-tex.dif
Patch3:  patches/file/file-4.20-ssd.dif
Patch4:  patches/file/file-4.20-xen.dif
Patch5:  patches/file/file-5.22-elf.dif
Patch6:  patches/file/file-5.19-printf.dif
#Patch7:  patches/file/file-5.12-zip.dif
#Patch8:  patches/file/file-5.17-option.dif
Patch9:  patches/file/file-4.21-scribus.dif
Patch10:  patches/file/file-4.21-xcursor.dif
Patch11:  patches/file/file-5.19-cromfs.dif
#Patch12:  patches/file/file-5.18-javacheck.dif
Patch13:  patches/file/file-5.19-solv.dif
Patch14:  patches/file/file-5.19-zip2.0.dif
#Patch15:  patches/file/file-5.19-biorad.dif
Patch16:  patches/file/file-5.19-clicfs.dif
Patch17:  patches/file/file-5.45-endian.patch
#Patch18:  patches/file/file-5.24-nitpick.dif
Patch19:  patches/file/file-5.45-clear-invalid.patch
Patch20:  patches/file/file-secure_getenv.patch
#Patch21:  patches/file/file-5.28-btrfs-image.dif
Patch22:  patches/file/file-5.45-mint.patch
#Patch23:  patches/file/file-5.32.dif

%rpmint_essential
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  make
Provides:       %{crossmint}file-devel

%rpmint_build_arch

%description
With the file command, you can obtain information on the file type of a
specified file. File type recognition is controlled by the file
/etc/magic, which contains the classification criteria. This command is
used by apsfilter to permit automatic printing of different file types.

%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch13 -p1
%patch14 -p1
%patch16 -p1
%patch17 -p1
%patch19 -p1
%patch20 -p1
%patch22 -p1

rm -f Magdir/*,v Magdir/*~
rm -f ltcf-c.sh ltconfig ltmain.sh
autoreconf -fiv
rm -rf autom4te.cache config.h.in.orig

cp %{S:1} config.sub

cat %{S:2} >> magic/Localstuff

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix} ${CONFIGURE_FLAGS_AMIGAOS}
	--sysconfdir=/etc
	--disable-nls
	--disable-shared
	--enable-fsect-man5
	--config-cache
"
STACKSIZE="-Wl,-stack,128k"

create_config_cache()
{
cat <<EOF >config.cache
ac_cv_header_pthread_h=no
gl_have_pthread_h=no
EOF
	%rpmint_append_gnulib_cache
}

mkdir -p %{buildroot}%{_rpmint_sysroot}/etc
cat << EOF > %{buildroot}%{_rpmint_sysroot}/etc/magic
# Localstuff: file(1) magic(5) for locally observed files
#     global magic file is %{_rpmint_target_prefix}/share/misc/magic(.mgc)
EOF

#
# compile a version for the host first, which is needed to compile the magic file
#
./configure --disable-shared --disable-nls
make %{?_smp_mflags}
mv src/file src/file.host
mv magic/Localstuff magic/Localstuff.orig
make distclean
mv magic/Localstuff.orig magic/Localstuff


for CPU in ${ALL_CPUS}
do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	create_config_cache

	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS ${STACKSIZE} -s" \
	"./configure" ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir

	make V=1 FILE_COMPILE='$(top_builddir)/src/file.host' %{?_smp_mflags}
	make DESTDIR=%{buildroot}%{_rpmint_sysroot} install

	# remove obsolete pkg config files for multilibs
	%rpmint_remove_pkg_configs

	# compress manpages
	%rpmint_gzip_docs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif

	mv magic/Localstuff magic/Localstuff.orig
	make clean >/dev/null
	mv magic/Localstuff.orig magic/Localstuff
done


%install

%rpmint_cflags

%rpmint_strip_archives

%if "%{buildtype}" == "cross"
configured_prefix="%{_rpmint_target_prefix}"
%rpmint_copy_pkg_configs
%else
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
rmdir %{buildroot}%{_rpmint_installdir} || :
rmdir %{buildroot}%{_prefix} 2>/dev/null || :
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS NEWS README TODO MAINT ChangeLog
%config(noreplace) %{_isysroot}/etc/magic
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/include/*
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}%{_rpmint_target_prefix}/share/misc/magic*


%changelog
* Thu Apr 06 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 5.32

* Thu Sep 13 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 3.36

* Fri Apr 21 2000 Edgar Aichinger <eaiching@t0.or.at>
- build against mintlibs 0.55.2

* Tue Apr 4 2000 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT 
- compressed man pages
