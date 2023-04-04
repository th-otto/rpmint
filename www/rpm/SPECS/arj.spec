%define pkgname arj

%rpmint_header

Summary:        Archiver for .arj files
Name:           %{crossmint}%{pkgname}
Version:        3.10.22
Release:        1
License:        GPL-2.0-or-later
Group:          Productivity/Archiving/Compression

URL:            http://arj.sourceforge.net/
Packager:       %{packager}

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc
BuildRoot:      %{_tmppath}/%{name}-root

Source0:        %{pkgname}-%{version}.tar.gz
Source1:        patches/automake/mintelf-config.sub

Patch0: patches/arj/arj-3.10.22-mint.patch
Patch1:         arj-3.10.22-missing-protos.patch
Patch2:         arj-3.10.22-custom-printf.patch
# Filed into upstream bugtracker as https://sourceforge.net/tracker/?func=detail&aid=2853421&group_id=49820&atid=457566
Patch3:         arj-3.10.22-quotes.patch
# PATCH-FIX-OPENSUSE -- make build reproducible
Patch4:         arj-3.10.22-reproducible.patch
# PATCH-FIX-UPSTREAM https://sourceforge.net/p/arj/git/merge-requests/1/
Patch5:         arj-3.10.22-fixstrcpy.patch
Patch6:         patches/arj/arj-001_arches_align.patch
Patch7:         patches/arj/arj-002_no_remove_static_const.patch
Patch8:         patches/arj/arj-003_64_bit_clean.patch
Patch9:         patches/arj/arj-004_parallel_build.patch
Patch10:        patches/arj/arj-doc_refer_robert_k_jung.patch
Patch11:        patches/arj/arj-strip.patch


%rpmint_essential
BuildRequires:  make

%rpmint_build_arch

%description
A portable version of the ARJ archiver, available for a growing number
of DOS-like and UNIX-like platforms on a variety of architectures.

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
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

cd gnu
autoreconf -fiv
rm -rf autom4te.cache
cp "%{S:1}" config.sub

autoconf

%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

COMMON_CFLAGS+=" -s -Wall"
STACKSIZE=-Wl,-stack,256k

CONFIGURE_FLAGS="--host=${TARGET} --prefix=%{_rpmint_target_prefix}"

build_dir=`pwd`
BASEDIR=mint

#
# there are no libraries in this package, so we
# have to build for the target CPU only
#
%if "%{buildtype}" == "cross"
for CPU in 000
%else
for CPU in %{buildtype}
%endif
do
#
# a native arj is needed by the makefiles
#
	cd "${build_dir}/gnu"
	./configure --enable-outdir=${BASEDIR}
	cd ..

	make prepare
	ARJ_DIR=${BASEDIR}/en/rs/arj
	export NATIVE_ARJ=${build_dir}/${ARJ_DIR}/arj
	make ${ARJ_DIR}/arj
	export NATIVE_ARJ=${build_dir}/native_arj
	mv ${ARJ_DIR}/arj ${NATIVE_ARJ}

#
# now for the real one
#
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}

	cd "$build_dir/gnu"
	CFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS" \
	./configure ${CONFIGURE_FLAGS} \
	--libdir='${exec_prefix}/lib'$multilibdir
	cd ..

	make prepare
	make clean

	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/msgbind
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/today
	#make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/make_key
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/postproc
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/join
	make CC=gcc COPT='-c -I$(BASEDIR) -I$(SRC_DIR) $(ALL_CFLAGS)' LDFLAGS='$(ADD_LDFLAGS)' ./${BASEDIR}/en/rs/tools/packager
	
	make || exit 1
	make DESTDIR="%{buildroot}%{_rpmint_sysroot}" install
	make clean

	install -Dpm 644 resource/rearj.cfg.example %{buildroot}%{_rpmint_sysconfdir}/rearj.cfg

	# remove the register remainders of arj's sharewares time
	rm -f %{buildroot}%{_rpmint_bindir}/arj-register
	rm -f %{buildroot}%{_rpmint_mandir}/man1/arj-register.1*

	# compress manpages
	%rpmint_gzip_docs
	# remove obsolete pkg config files
	%rpmint_remove_pkg_configs
	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	%rpmint_make_bin_archive $CPU
	%endif
done

%install

%if "%{buildtype}" != "cross"
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}%{_rpmint_sysroot}
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license doc/COPYING
%doc ChangeLog doc/*.txt
%config(noreplace) %{_isysroot}/etc/rearj.cfg
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/share


%changelog
* Mon Apr 03 2023 Thorsten Otto <admin@tho-otto.de>
- RPMint spec file
