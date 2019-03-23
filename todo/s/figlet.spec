Summary:  Frank, Ian & Glenn's Letters
Name: figlet        
Version: 2.2 
Release: 1
Group: Applications/Text
Prefix: /usr
Source: %{name}-%{version}.tar.gz
Copyright: public domain
Distribution: Sparemint
Vendor: Sparemint
URL: ftp://ftp.internexus.net/pub/figlet/program/figlet22.tar.gz
Packager: Jan Krupka <jkrupka@volny.cz>
BuildRoot: /var/tmp/figlet

%description
Figlet is a program that creates large characters out of ordinary screen
characters.  It can create characters in many different styles and can
kern and "smush" these characters together in various ways.  Figlet
output is generally reminiscent of the sort of "signatures" many people
like to put at the end of e-mail and Usenet messages.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS" all
strip figlet
strip chkfont

%install
make install PREFIX=$RPM_BUILD_ROOT
mkdir -p  $RPM_BUILD_ROOT/usr/games
mkdir -p  $RPM_BUILD_ROOT/usr/doc/figlet-%{version}
mkdir -p  $RPM_BUILD_ROOT/usr/man/man6
gzip  $RPM_BUILD_ROOT/usr/man/man6/%{name}.6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc FTP-NOTE README figfont.txt
/usr/games/chkfont
/usr/games/figlet
/usr/games/figlist
/usr/games/lib/figlet.dir/646-ca.flc
/usr/games/lib/figlet.dir/646-ca2.flc
/usr/games/lib/figlet.dir/646-cn.flc
/usr/games/lib/figlet.dir/646-cu.flc
/usr/games/lib/figlet.dir/646-de.flc
/usr/games/lib/figlet.dir/646-dk.flc
/usr/games/lib/figlet.dir/646-es.flc
/usr/games/lib/figlet.dir/646-es2.flc
/usr/games/lib/figlet.dir/646-fr.flc
/usr/games/lib/figlet.dir/646-gb.flc
/usr/games/lib/figlet.dir/646-hu.flc
/usr/games/lib/figlet.dir/646-irv.flc
/usr/games/lib/figlet.dir/646-it.flc
/usr/games/lib/figlet.dir/646-jp.flc
/usr/games/lib/figlet.dir/646-kr.flc
/usr/games/lib/figlet.dir/646-no.flc
/usr/games/lib/figlet.dir/646-no2.flc
/usr/games/lib/figlet.dir/646-pt.flc
/usr/games/lib/figlet.dir/646-pt2.flc
/usr/games/lib/figlet.dir/646-se.flc
/usr/games/lib/figlet.dir/646-se2.flc
/usr/games/lib/figlet.dir/646-yu.flc
/usr/games/lib/figlet.dir/8859-2.flc
/usr/games/lib/figlet.dir/8859-3.flc
/usr/games/lib/figlet.dir/8859-4.flc
/usr/games/lib/figlet.dir/8859-5.flc
/usr/games/lib/figlet.dir/8859-7.flc
/usr/games/lib/figlet.dir/8859-8.flc
/usr/games/lib/figlet.dir/8859-9.flc
/usr/games/lib/figlet.dir/banner.flf
/usr/games/lib/figlet.dir/big.flf
/usr/games/lib/figlet.dir/block.flf
/usr/games/lib/figlet.dir/bubble.flf
/usr/games/lib/figlet.dir/digital.flf
/usr/games/lib/figlet.dir/frango.flc
/usr/games/lib/figlet.dir/hz.flc
/usr/games/lib/figlet.dir/ilhebrew.flc
/usr/games/lib/figlet.dir/ivrit.flf
/usr/games/lib/figlet.dir/jis0201.flc
/usr/games/lib/figlet.dir/koi8r.flc
/usr/games/lib/figlet.dir/lean.flf
/usr/games/lib/figlet.dir/mini.flf
/usr/games/lib/figlet.dir/mnemonic.flf
/usr/games/lib/figlet.dir/moscow.flc
/usr/games/lib/figlet.dir/script.flf
/usr/games/lib/figlet.dir/shadow.flf
/usr/games/lib/figlet.dir/slant.flf
/usr/games/lib/figlet.dir/small.flf
/usr/games/lib/figlet.dir/smscript.flf
/usr/games/lib/figlet.dir/smshadow.flf
/usr/games/lib/figlet.dir/smslant.flf
/usr/games/lib/figlet.dir/standard.flf
/usr/games/lib/figlet.dir/term.flf
/usr/games/lib/figlet.dir/upper.flc
/usr/games/lib/figlet.dir/ushebrew.flc
/usr/games/lib/figlet.dir/uskata.flc
/usr/games/lib/figlet.dir/utf8.flc
/usr/games/showfigfonts
/usr/man/man6/figlet.6.gz

%changelog
* Thu Oct 29 2001 Jan Krupka <jkrupka@volny.cz>
- first release for SpareMiNT (new package)
