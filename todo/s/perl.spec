Summary       : The Perl programming language.
Name          : perl
Version       : 5.6.0
Release       : 3
Group         : Development/Languages
Copyright     : GPL

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.perl.com/pub/

Provides      : /usr/bin/perl
Requires      : gdbm >= 1.8.0

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.perl.org/pub/perl/CPAN/src/perl-%{version}.tar.gz
Source1: ftp://ftp.perl.org/pub/CPAN/modules/by-module/MD5/MD5-1.7.tar.gz
Source2: find-provides
Source3: find-requires
Patch0:  perl5.005_02-buildsys.patch
Patch1:  perl-5.6.0-installman.patch
Patch2:  perl5.005_03-db1.patch
Patch3:  perl-5.6.0-nodb.patch
Patch4:  perl-5.6.0-prereq.patch
Patch5:  perl-5.6.0-mint.patch

%define system  m68k-atari-mint

# ----- Perl module dependencies.
#
# Provide perl-specific find-{provides,requires} until rpm-3.0.4 catches up.
%define	__find_provides	%{SOURCE2}
%define	__find_requires	%{SOURCE3}


%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the perl
package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your
system to handle Perl scripts.


%prep
%setup -q
mkdir modules
tar xzf %{SOURCE1} -C modules
%patch0 -p1 -b .buildsys
%patch1 -p1 -b .instman
# Perl does not have a single entry point to define what db library to use
# so the patch below is mostly broken...
#%patch2 -p1
%patch3 -p1 -b .nodb
%patch4 -p1 -b .prereq
%patch5 -p1 -b .mint

find . -name \*.orig -exec rm -fv {} \;


%build

cat > config.over <<EOF
installprefix=${RPM_BUILD_ROOT}%{_prefix}
test -d \$installprefix/bin || mkdir -p \$installprefix/bin
installarchlib=\`echo \$installarchlib | sed "s!\$prefix!\$installprefix!"\`
installbin=\`echo \$installbin | sed "s!\$prefix!\$installprefix!"\`
installman1dir=\`echo \$installman1dir | sed "s!\$prefix!\$installprefix!"\`
installman3dir=\`echo \$installman3dir | sed "s!\$prefix!\$installprefix!"\`
installprivlib=\`echo \$installprivlib | sed "s!\$prefix!\$installprefix!"\`
installscript=\`echo \$installscript | sed "s!\$prefix!\$installprefix!"\`
installsitelib=\`echo \$installsitelib | sed "s!\$prefix!\$installprefix!"\`
installsitearch=\`echo \$installsitearch | sed "s!\$prefix!\$installprefix!"\`
EOF

sh Configure -des -Doptimize="${RPM_OPT_FLAGS}" \
	-Dprefix=%{_prefix} \
	-Dosname=mint \
	-Darchname=%{system} \
	-Dcf_email="fnaumann@freemint.de" \
	-Di_db \
	-Di_gdbm \
	-Dman1dir=%{_prefix}/share/man/man1 \
	-Dman3dir=%{_prefix}/lib/perl5/man/man3 

make

# Build the modules we have
MainDir=$(pwd)
cd modules
for module in * ; do 
    cd $module
    $MainDir/perl -I$MainDir/lib Makefile.PL
    make
    cd ..
done
cd $MainDir


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}
make install
install -m 755 utils/pl2pm ${RPM_BUILD_ROOT}%{_prefix}/bin/pl2pm

# Now pay attention to the extra modules
MainDir=$(pwd)
cd modules
for module in * ; do 
    make -C $module install \
	INSTALLMAN3DIR=${RPM_BUILD_ROOT}%{_prefix}/lib/perl5/man/man3
done
cd $MainDir

# fix the rest of the stuff
find ${RPM_BUILD_ROOT}%{_prefix}/lib/perl5 -name .packlist -o -name perllocal.pod | \
    while read packlist ; do    
	./perl -i -p -e "s|${RPM_BUILD_ROOT}||g;" $packlist
    done

./perl -i -p -e "s|${RPM_BUILD_ROOT}||g;" \
	${RPM_BUILD_ROOT}%{_prefix}/lib/perl5/%{version}/%{system}/Config.pm

# strip down group/other write flag
chmod -R go-w ${RPM_BUILD_ROOT}/* ||:
# just to be sure strip all executables
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# shit, B:: files are interpreted as drive B: :-(
# how to handle this?
# the good thing is that rm can handle this
# the bad thing is that only rm work correct
for i in `ls ${RPM_BUILD_ROOT}%{_prefix}/lib/perl5/man/man3/B::*` ; do rm -f "$i" ; done

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/lib/perl5/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/lib/perl5
%{_prefix}/share/man/man1/*


%changelog
* Thu Dec 26 2000 Frank Naumann <fnaumann@freemint.de>
- recompiled against gdbm lib 1.8.0 and updated db libs

* Fri Dec 08 2000 Frank Naumann <fnaumann@freemint.de>
- moved manpages to %{_prefix}/share
- fixed memory management

* Thu Nov 24 2000 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
