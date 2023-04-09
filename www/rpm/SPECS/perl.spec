%define pkgname perl

%rpmint_header

Summary:        The Perl interpreter
Name:           %{crossmint}%{pkgname}
Version:        5.26.1
Release:        1
License:        Artistic-1.0 or GPL-2.0-or-later
Group:          Development/Languages/Perl

Packager:       %{packager}
URL:            http://www.perl.org/

Prefix:         %{_rpmint_target_prefix}
Docdir:         %{_isysroot}%{_rpmint_target_prefix}/share/doc/packages
BuildRoot:      %{_tmppath}/%{name}-root

Source0: http://www.cpan.org/src/5.0/perl-%{version}.tar.xz
Source1: patches/perl/perl-cross-mint.tar.gz
#Source2: patches/perl/perl-find-provides
#Source3: patches/perl/perl-find-requires

Patch0: patches/perl/perl-5.26.0.patch
Patch1: patches/perl/perl-regexp-refoverflow.patch
Patch2: patches/perl/perl-nroff.patch
Patch3: patches/perl/perl-netcmdutf8.patch
Patch4: patches/perl/perl-HiRes.t-timeout.patch
Patch5: patches/perl/perl-saverecontext.patch
Patch6: patches/perl/perl-skip_time_hires.patch
Patch7: patches/perl/perl-incfix.patch
Patch8: patches/perl/perl-5.18.2-overflow.patch
Patch9: patches/perl/perl-reproducible.patch
Patch10: patches/perl/perl-skip_flaky_tests_powerpc.patch
Patch11: patches/perl/perl-posix-sigaction.patch
Patch12: patches/perl/perl-rpm-macros.patch
Patch13: patches/perl/perl-mint-hints.patch
Patch14: patches/perl/perl-mint-inet6.patch
Patch15: patches/perl/perl-cpan-db-file.patch
Patch16: patches/perl/perl-fp-classify.patch
Patch17: patches/perl/perl-gdbm-compat-link-order.patch
Patch18: patches/perl/perl-cross-use-correct-strip.patch

%rpmint_essential
BuildRequires:  make
BuildRequires:  %{crossmint}gdbm >= 1.8.0


%rpmint_build_arch

%description
perl - Practical Extraction and Report Language

Perl is optimized for scanning arbitrary text files, extracting
information from those text files, and printing reports based on that
information.  It is also good for many system management tasks. Perl is
intended to be practical (easy to use, efficient, and complete) rather
than beautiful (tiny, elegant, and minimal).

Some of the modules available on CPAN can be found in the "perl"
series.


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
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

tar --strip-components=1 -xf "%{S:1}"


%build

%rpmint_cflags

[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

CONFIGURE_FLAGS="
	--target=${TARGET}
	--prefix=%{_rpmint_target_prefix}
	-Dvendorprefix=%{_rpmint_target_prefix}
	-Dosname=mint
	-Dman1dir=%{_rpmint_target_prefix}/share/man/man1
	-Dman3dir=%{_rpmint_target_prefix}/lib/perl5/man/man3
"
COMMON_CFLAGS="\
	-Wall -Wno-unused-function \
	-fno-strict-aliasing \
	-D_GNU_SOURCE \
	-DPERL_USE_SAFE_PUTENV \
	-D_LARGEFILE_SOURCE \
	-D_FILE_OFFSET_BITS=64"
OPT_CFLAGS="-O2 -fomit-frame-pointer -fwrapv"


#
# installperl already takes care of that;
# also the files are made read-only so we can't use the tools
#
NO_STRIP=true
NO_RANLIB=true


CPU_ARCHNAME_000=-000
CPU_ARCHNAME_020=-020
CPU_ARCHNAME_v4e=-v4e

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
	eval CPU_CFLAGS=\${CPU_CFLAGS_$CPU}
	eval multilibdir=\${CPU_LIBDIR_$CPU}
	eval multilibexecdir=\${CPU_LIBEXECDIR_$CPU}
	eval archname=\${CPU_ARCHNAME_$CPU}

	case $CPU in
		v4e) longdblsize=8; longdblkind=0 ;;
		*) longdblsize=12; longdblkind=4 ;;
	esac

	case $TARGET in
		*-*-mintelf*) lddlflags="-r -Wl,--oformat,elf32-m68k" ;;
		*) lddlflags="-r" ;;
	esac

	LDFLAGS="$CPU_CFLAGS $COMMON_CFLAGS $STACKSIZE" \
	sh ./configure \
		${CONFIGURE_FLAGS} \
		-Dcc="%{_rpmint_target_gcc} $CPU_CFLAGS" \
		-Dccflags="$OPT_CFLAGS $COMMON_CFLAGS" \
		-Dcppflags="$COMMON_CFLAGS" \
		-Doptimize="$OPT_CFLAGS" \
		-Darchname=${TARGET}${archname} \
		-Dlongdblsize=${longdblsize} \
		-Dlongdblkind=${longdblkind} \
		-Dlddlflags="$lddlflags" \
		-Dcccdlflags="-Wno-unused-function" \
		-Dso='none'

	make
	
	# this is sometimes not build???
	make pod/perlmodlib.pod

	buildroot="%{buildroot}%{_rpmint_sysroot}"
	make DESTDIR="${buildroot}" install

	install -d -m 755 ${buildroot}%{_rpmint_target_prefix}/lib/perl5/vendor_perl/%{version}/${TARGET}${archname}
	install -d -m 755 ${buildroot}%{_rpmint_target_prefix}/lib/perl5/site_perl/%{version}/${TARGET}${archname}
	gzip -9 -f ${buildroot}%{_rpmint_target_prefix}/lib/perl5/man/man3/*.3

	# change a hardlink to a symlink
	rm -f ${buildroot}%{_rpmint_target_prefix}/share/man/man1/perlthanks.1
	$LN_S perlbug.1 ${buildroot}%{_rpmint_target_prefix}/share/man/man1/perlthanks.1

	# shit, B:: files are interpreted as drive B: :-(
	# how to handle this?
	# the good thing is that rm can handle this
	# the bad thing is that only rm work correct
	rm -vf %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/perl5/man/man3/B::*

	# install macros.perl file
	install -D -m 644 macros.perl ${buildroot}/etc/rpm/macros.perl

	make clean >/dev/null

	# compress manpages
	%rpmint_gzip_docs
	gzip -9 %{buildroot}%{_rpmint_sysroot}%{_rpmint_target_prefix}/lib/perl5/man/man3/*

	rm -f %{buildroot}%{_rpmint_libdir}$multilibdir/charset.alias

	%if "%{buildtype}" != "cross"
	if test "%{buildtype}" != "$CPU"; then
		rm -f %{buildroot}%{_rpmint_bindir}/*
	fi
	%rpmint_make_bin_archive $CPU
	%endif
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
%license Artistic Copying AUTHORS Changes README*
%{_isysroot}%{_rpmint_target_prefix}/bin/*
%{_isysroot}%{_rpmint_target_prefix}/lib/perl5
%{_isysroot}%{_rpmint_target_prefix}/share/man/*/*
%{_isysroot}/etc/rpm/macros.perl


%changelog
* Sun Apr 09 2023 Thorsten Otto <admin@tho-otto.de>
- Rewritten as RPMint spec file
- Update to version 5.26.1

* Tue Dec 26 2000 Frank Naumann <fnaumann@freemint.de>
- recompiled against gdbm lib 1.8.0 and updated db libs

* Fri Dec 08 2000 Frank Naumann <fnaumann@freemint.de>
- moved manpages to %{_prefix}/share
- fixed memory management

* Fri Nov 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
