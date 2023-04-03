%define pkgname Xaw3d

%rpmint_header

Summary       : A version of the MIT Athena widget set for X.
Summary(de)   : 3D-Version des MIT Athena-Widgetsatzes fuer X
%if "%{buildtype}" == "cross"
Name:           cross-mint-%{pkgname}
%else
Name:           %{pkgname}
%endif
Version       : 1.5
Release       : 3
License       : MIT
Group         : Development/Libraries

Packager      : Thorsten Otto <admin@tho-otto.de>
URL           : ftp://ftp.x.org/contrib/widgets/Xaw3d/

%if "%{buildtype}" == "cross"
BuildRequires : cross-mint-XFree86-devel
Requires      : cross-mint-XFree86
%else
BuildRequires : XFree86-devel
Requires      : XFree86
Prereq        : fileutils
%endif

Prefix        : %{_rpmint_target_prefix}
Docdir        : %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.x.org/contrib/widgets/Xaw3d/R6.3/%{pkgname}-%{version}.tar.gz
Patch0: patches/Xaw3d/Xaw3d-1.1-shlib.patch
Patch1: patches/Xaw3d/Xaw3d-1.3-glibc.patch
Patch2: patches/Xaw3d/Xaw3d.patch
Patch3: patches/Xaw3d/Xaw3d-1.3-static.patch
Patch4: patches/Xaw3d/Xaw3d-ia64.patch

%rpmint_build_arch


%description
Xaw3d is an enhanced version of the MIT Athena Widget set for
the X Window System.  Xaw3d adds a three-dimensional look to applications
with minimal or no source code changes.

You should install Xaw3d-devel if you are going to develop applications
using the Xaw3d widget set.

%description -l de
Xaw3d ist eine verbesserte Version des MIT Athena-Widgetsatzes für X.
Xaw3d gibt Programmen einen 3D-Look, ohne, daß der Source verändert werden
muß.

Sie sollten Xaw3d-devel installieren, falls Sie Xaw3d-Anwendungen
entwickeln wollen.


%prep
[ "%{buildroot}" == "/" -o "%{buildroot}" == "" ] && exit 1
%setup -q -c
cd xc/lib/Xaw3d
%patch0 -p1
ln -s .. X11
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

cd xc/lib/Xaw3d
build_dir=`pwd`

for CPU in ${ALL_CPUS}; do
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}

	%{_rpmint_target}-xmkmf -DCpuOption="${CPU_CFLAGS}"
	
	make DESTDIR=%{buildroot} install install.man

	#
	# install symlinks in <prefix>/lib
	#
	mkdir -p %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib${multilibdir}
	cd %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/X11R6/lib
          if test "${multilibdir}" != ""; then
              subdir="${multilibdir#/}"
              mkdir "$subdir"
              mv *.a "$subdir"
              cd "$subdir"
              subdir=../
          else
              subdir=
          fi
	  for i in *.a; do
	    ln -s ../${subdir}X11R6/lib${multilibdir}/$i ../../${subdir}lib${multilibdir}/$i;
	  done
	cd "$build_dir"
	
	make clean
done


%install

cd xc/lib/Xaw3d

%if "%{buildtype}" != "cross"
cp -pr %{buildroot}%{_rpmint_sysroot}/. %{buildroot}
rm -rf %{buildroot}%{_rpmint_sysroot}
%endif


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%if "%{buildtype}" != "cross"
%post
if [ ! -d %{_rpmint_target_prefix}/X11R6/include/X11/Xaw3d ] ; then
	rm -f %{_rpmint_target__prefix}/X11R6/include/X11/Xaw3d
	ln -sf ../Xaw3d %{_rpmint_target__prefix}/X11R6/include/X11
fi
%endif


%files
%defattr(-,root,root)
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/X11R6/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*.a
%{_isysroot}%{_rpmint_target_prefix}/lib/*/*.a
%{_isysroot}%{_rpmint_target_prefix}/X11R6/include/X11/Xaw3d


%changelog
* Wed Mar 29 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file

* Mon Dec 18 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
