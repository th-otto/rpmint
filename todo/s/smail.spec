Summary: smail mail transport agent
Name: smail
Version: 3.2.0.101
Release: 1
Copyright: GPL-like
Group: Daemons
Source: ftp://ftp.uu.net/networking/mail/smail/smail-%{version}.tar.gz
Source1: smail-batching.tgz
Source2: smail.cron
Source3: smail.log
Source4: smail-configs.tgz
#Source5: smail-init.tgz
Source6: smail-mintdoc.tgz
Patch0: smail-mint.patch
Patch1: smail-mintcnf.patch
Packager: Guido Flohr <gufl0000@stud.uni-sb.de>
Vendor: Sparemint
Requires: gzip
Conflicts: qmail
Conflicts: sendmail
Provides: smtpdaemon
BuildRoot: /var/tmp/smail-root
Summary(de): Smail Mail-Transport-Agent (MTA)

%description
smail is an alternative mail transport agent, easy to configure and
with flexible routing especially in uucp networks.

%description -l de
Smail is ein alternativer Mail-Transport-Agent (MTA), leicht zu
konfigurieren, mit flexiblem Routing, besonders in uucp-Netzwerken.

%prep
rm -rf $RPM_BUILD_ROOT
%setup
tar -xvzf $RPM_SOURCE_DIR/smail-batching.tgz -C $RPM_BUILD_DIR/smail-%{version}
%patch0 -p1 -b .mint
%patch1 -p1 -b .mintcnf

%build
make YACC='bison -y' everything
chmod 777 src/smail
stack --fix=64k src/smail

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
install -m 4555 -s src/smail $RPM_BUILD_ROOT/usr/sbin/smail
for i in mailq pathto rsmtp rmail runq smtpd uupath sendmail; do
  ln -s smail $RPM_BUILD_ROOT/usr/sbin/$i
done
# Other places where these programs are also often expected
mkdir -p $RPM_BUILD_ROOT/usr/lib
ln -s /usr/sbin/smail $RPM_BUILD_ROOT/usr/lib/sendmail
mkdir -p $RPM_BUILD_ROOT/bin
ln -s /usr/sbin/smail $RPM_BUILD_ROOT/bin/rmail

for i in checkerr dcasehost mkaliases mkdbm mksort; do
  install -m 0777 util/$i $RPM_BUILD_ROOT/usr/sbin/$i
done

mkdir -p $RPM_BUILD_ROOT/usr/lib/smail{,/lists,/methods}
mkdir -p $RPM_BUILD_ROOT/var/smail
install -m 0755 rcsmtp $RPM_BUILD_ROOT/usr/sbin/rcsmtp
install -m 0755 batchcsmtp $RPM_BUILD_ROOT/usr/sbin/batchcsmtp

mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man5
mkdir -p $RPM_BUILD_ROOT/usr/man/man8

for i in pathto uupath; do
  install -m 0644 man/man1/$i.1 $RPM_BUILD_ROOT/usr/man/man1/$i.1
done

for i in smail smailconf smaildrct smailmeth smailqual smailrtrs smailrtry \
  smailtrns; do
  install -m 0644 man/man5/$i.5 $RPM_BUILD_ROOT/usr/man/man5/$i.5
done

for i in checkerr mailq mkaliases mkdbm mksort pathalias rmail rsmtp runq \
  sendmail smail smtpd; do
  install -m 0644 man/man8/$i.8 $RPM_BUILD_ROOT/usr/man/man8/$i.8
done

# This is lazyness.  Probably most programs are happy with their default
# stack but I don't want to test them all.
stack --fix=64k $RPM_BUILD_ROOT/usr/sbin/* $RPM_BUILD_ROOT/bin/* 2>/dev/null || :

mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 0644 $RPM_SOURCE_DIR/smail.log $RPM_BUILD_ROOT/etc/logrotate.d/smail
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
install -m 0755 $RPM_SOURCE_DIR/smail.cron $RPM_BUILD_ROOT/etc/cron.daily/smail
mkdir -p $RPM_BUILD_ROOT/usr/lib/smail
tar -xvzf $RPM_SOURCE_DIR/smail-configs.tgz -C $RPM_BUILD_ROOT/usr/lib/smail

#mkdir -p $RPM_BUILD_ROOT/etc/rc.d
#tar -xvzf $RPM_SOURCE_DIR/smail-init.tgz -C $RPM_BUILD_ROOT/etc/rc.d
mkdir -p $RPM_BUILD_ROOT/var/spool/smail
chmod 755 $RPM_BUILD_ROOT/var/spool/smail

# We have to be smart for compressed manpages.
set +x
for file in $RPM_BUILD_ROOT/usr/man/man*/*; do
	exec <$file || exit 1
	read # One line of garbage.
	read SO WHAT GARBAGE
	read dummy && continue # This is better than test `wc -l` = 1 *
	test "$SO$GARBAGE" = ".so" || continue
	echo ".so $WHAT.gz" >$file || exit 1
	echo "Made manpage $file include gzipped $WHAT."
done 
set -x
gzip -9nf $RPM_BUILD_ROOT/usr/man/man*/*
tar -xvzf $RPM_SOURCE_DIR/smail-mintdoc.tgz -C $RPM_BUILD_DIR/smail-%{version}

%post
VERSION=%{version} cat <<EOF
Please read the file /usr/doc/smail-$VERSION/README-MiNT before you start
using smail.
EOF

# Currently don't clean because we have to check the symlinks.
%clean
# rm -rf $RPM_BUILD_ROOT

%files
%doc COPYING NOTES PROJECTS README guide samples README-MiNT
/var/spool/smail
/usr/lib/sendmail
/usr/man
/usr/sbin
/bin/*
/etc/logrotate.d
/etc/cron.daily
%config /usr/lib/smail/config
%config /usr/lib/smail/directors
%config /usr/lib/smail/paths
%config /usr/lib/smail/routers
%config /usr/lib/smail/transports
%config /usr/lib/smail/methods/uucp
/usr/lib/smail/lists
