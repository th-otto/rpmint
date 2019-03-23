Summary: The procmail mail processing program.
Name: procmail
Version: 3.13.1
Release: 1
Vendor: Sparemint
Packager: John Blakeley <johnnie@ligotage.demon.co.uk>
Copyright: distributable
Group: System Environment/Daemons
Source: ftp://ftp.procmail.org/pub/procmail/procmail-%{version}.tar.gz
Patch0: procmail-3.12-misc.patch
Patch1: procmail-3.10-000lock.patch
Patch2: procmail-3.10-lockf.patch
BuildRoot: /var/tmp/%{name}-root

%description
The procmail program can be used for delivering local mail,
for automatic filtering, presorting and other mail handling jobs.
Procmail is also the basis for the SmartList mailing list processor.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1
%patch2 -p1

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fomit-frame-pointer"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/{bin,man/man1,man/man5}

make BASENAME=$RPM_BUILD_ROOT/usr install.bin install.man

gzip -9nf $RPM_BUILD_ROOT/usr/man/*/*

strip $RPM_BUILD_ROOT/usr/bin/{procmail,lockfile,formail}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,wheel)
%attr(6755,root,mail)	/usr/bin/procmail
%attr(2755,root,mail)	/usr/bin/lockfile
/usr/bin/formail
/usr/bin/mailstat

/usr/man/man1/procmail.1.gz
/usr/man/man1/formail.1.gz
/usr/man/man1/lockfile.1.gz

/usr/man/man5/procmailrc.5.gz
/usr/man/man5/procmailsc.5.gz
/usr/man/man5/procmailex.5.gz

%changelog
* Sun Jun 04 2000 John Blakeley <johnnie@ligotage.demon.co.uk>
- First release for Sparemint.
