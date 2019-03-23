Summary       : A GNU utility for secure communication and data storage.
Name          : gnupg
Version       : 1.0.4
Release       : 2
Copyright     : GPL
Group         : Applications/Cryptography

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnupg.org/

Provides      : gpg openpgp
#Conflicts     : gnupg-68000

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.gnupg.org/pub/gcrypt/gnupg/%{name}-%{version}.tar.gz
Patch0: gnupg-1.0.2-locale.patch
Patch1: gnupg-1.0.3-typos.patch
Patch2: gnupg-1.0.4-rijndael.patch
Patch3: gnupg-1.0.4-strlen.patch
Patch4: gnupg-1.0.4-mint.patch


%description
GnuPG (GNU Privacy Guard) is a GNU utility for encrypting data and
creating digital signatures. GnuPG has advanced key management
capabilities and is compliant with the proposed OpenPGP Internet
standard described in RFC2440. Since GnuPG doesn't use any patented
algorithm, it is not compatible with any version of PGP2 (PGP2.x uses
only IDEA for symmetric-key encryption, which is patented worldwide).

#==========================================================================
#This packages was compiled with -m68020. This means you need at least
#a machine with an 68020 CPU or better to use the programs herein.
#==========================================================================
#
#Install the gnupg-68000 package if you don't have an 68020 or better.


%prep
%setup -q
%patch1 -p1 -b .typos
%patch2 -p1 -b .rijndael
%patch3 -p1 -b .strlen
%patch4 -p1 -b .mint


%build
autoconf
CFLAGS="${RPM_OPT_FLAGS}" \
LIBS="-lintl" \
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_prefix}/share/man \
	--disable-asm
make


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	mandir=${RPM_BUILD_ROOT}%{_prefix}/share/man

sed 's^\.\./g[0-9\.]*/^^g' tools/lspgpot > lspgpot
install -m755 lspgpot ${RPM_BUILD_ROOT}%{_prefix}/bin/lspgpot

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:
stack --fix=96k ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


#%post
#cat <<EOF
#==========================================================================
#This packages was compiled with -m68020. This means you need at least
#a machine with an 68020 CPU use the programs herein.
#==========================================================================
#EOF


%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS PROJECTS README THANKS TODO
%doc doc/DETAILS doc/FAQ doc/HACKING doc/OpenPGP doc/faq.html
%doc g*/OPTIONS g*/pubring.asc

%{_prefix}/bin/gpg
%{_prefix}/bin/gpgv
%{_prefix}/bin/lspgpot
%{_prefix}/lib/gnupg
%{_prefix}/share/gnupg
%{_prefix}/share/locale/*/*/*
%{_prefix}/share/man/man1/gpg.*
%{_prefix}/share/man/man1/gpgv.*


%changelog
* Fri Feb 23 2001 Frank Naumann <fnaumann@freemint.de>
- recompiled against updated MiNTLib with static stdio initialization;
  should now work with rpm to signate rpm files

* Wed Jan 03 2001 Frank Naumann <fnaumann@freemint.de>
- first release for Sparemint
