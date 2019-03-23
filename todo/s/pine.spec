Summary       : A commonly used, MIME compliant mail and news reader.
Name          : pine
Version       : 4.31
Release       : 1
Group         : Applications/Internet
Copyright     : Freely Distributable

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.washington.edu/pine

BuildPrereq   : perl openssl-devel

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
Buildroot     : %{_tmppath}/%{name}-root

%define pgpver 0.14.0

Source0: ftp://ftp.cac.washington.edu/pine/pine%{version}.tar.gz
Source1: http://www.megaloman.com/~hany/_data/pinepgp/pinepgp-%{pgpver}.tar.gz
Source2: pine.conf
Patch0:  pine-4.30-redhat.patch
Patch1:  pine-4.02-filter.patch
Patch2:  pine-4.04-noflock.patch
Patch3:  pine-4.21-fixhome.patch
Patch4:  pine-4.21-passwd.patch
Patch5:  pine-4.30-ldap.patch
Patch6:  pine-4.31-openssl.patch
Patch7:  pine-4.30-boguswarning.patch
Patch8:  pine-4.30-mint.patch


%description
Pine is a very popular, easy to use, full-featured email user agent
which includes a simple text editor called pico. Pine supports MIME
extensions and can also be used to read news.  Pine also supports
IMAP, mail and MH style folders.

Pine should be installed because Pine is a very commonly used email
user agent.


%prep
%setup -q -n pine%{version} -a 1 
%patch0  -p1 
%patch1  -p1 
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch8  -p1

# this wants /usr/local/bin/perl
chmod 644 contrib/utils/pwd2pine
perl -pi -e "s|/usr/local/bin/perl|/usr/bin/perl|" contrib/utils/pwd2pine


%build
./build \
	DEBUG="" \
	OPTIMIZE="$RPM_OPT_FLAGS" \
	mnt

#	CC="gcc -m68020-60 -m68881"
#	SPECIALAUTHENTICATORS="ssl"

cd pinepgp-%{pgpver}
make


%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/doc
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib
install -m 644 doc/mime.types ${RPM_BUILD_ROOT}%{_prefix}/lib/mime.types
for n in pine pico pilot; do
    install -m 755 -s bin/$n ${RPM_BUILD_ROOT}%{_prefix}/bin/$n
done

cd pinepgp-%{pgpver}
make install-gpg prefix=${RPM_BUILD_ROOT}%{_prefix}
cd ..

cd doc
for n in pine.1 pico.1 pilot.1; do
    install -m 644 $n ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1
done
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/*

mkdir -p ${RPM_BUILD_ROOT}/etc
cp %{SOURCE2} ${RPM_BUILD_ROOT}/etc/pine.conf
cat <<EOF > ${RPM_BUILD_ROOT}/etc/pine.conf.fixed
#
# Pine system-wide enforced configuration file - customize as needed
#
# This file holds the system-wide enforced values for pine configuration
# settings. Any values set in it will override values set in the
# system-wide default configuration file (/etc/pine.conf) and
# the user's own configuration file (~/.pinerc).
# For more information on the format of this file, read the
# comments at the top of /usr/lib/pine.conf

EOF


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README CPYRIGHT doc/*.txt doc/pine-ports doc/tech-notes doc/mailcap.unx imap/docs/bugs.txt
%{_prefix}/bin/pine
%{_prefix}/bin/pico
%{_prefix}/bin/pilot
%{_prefix}/bin/gpg-check
%{_prefix}/bin/gpg-sign
%{_prefix}/bin/gpg-encrypt
%{_prefix}/bin/gpg-sign+encrypt
%{_prefix}/bin/pinegpg
%{_prefix}/share/man/man1/pico.1*
%{_prefix}/share/man/man1/pine.1*
%{_prefix}/share/man/man1/pilot.1*
%attr(0644,root,root) %config %{_prefix}/lib/mime.types
%attr(0644,root,root) %config /etc/pine.conf
%attr(0644,root,root) %config /etc/pine.conf.fixed


%changelog
* Thu Dec 12 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 4.31

* Fri Dec 08 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 4.30
- moved manpages to /usr/share

* Fri Mar 03 2000 Frank Naumann <fnaumann@freemint.de>
- updated to 4.21
- integrated all redhat changes

* Wed Aug 25 1999 Frank Naumann <fnaumann@freemint.de>
- compressed manpages
- correct Packager and Vendor
