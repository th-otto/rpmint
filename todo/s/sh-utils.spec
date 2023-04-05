Summary       : A set of GNU utilities commonly used in shell scripts.
Summary(de)   : GNU-Shell-Utilities
Summary(fr)   : Utilitaires shell de GNU
Summary(pl)   : Narzêdzia shell-a (GNU)
Summary(tr)   : GNU kabuk araçlarý
Name          : sh-utils
Version       : 2.0.11
Release       : 1
Copyright     : GPL
Group         : System Environment/Shells

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/shellutils/

Prereq        : /sbin/install-info

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.gnu.org/gnu/sh-utils/sh-utils-%{version}.tar.gz
Source2: help2man
Patch1:  sh-utils-paths.patch
Patch2:  sh-utils-info.patch
Patch3:  sh-utils-pl_manpages.patch
Patch4:  sh-utils-human.patch
Patch5:  sh-utils-2.0-getgid.patch
Patch6:  sh-utils-rfc822.patch
Patch7:  sh-utils-dateman.patch
Patch8:  sh-utils-utmp.patch
Patch9:  sh-utils-2.0-mint.patch
Patch10: sh-utils-2.0.11-getopt.patch


%description
The GNU shell utilities are a set of useful system utilities which are
often used in shell scripts. The sh-utils package includes:
- basename (to remove the path prefix from a specified pathname),
- chroot (to change the root directory),
- date (to print/set the system time and date),
- dirname (to remove the last level or the filename from a given
  path),
- echo (to print a line of text),
- env (to display/modify the environment),
- expr (to evaluate expressions),
- factor (to print prime factors),
- false (to return an unsuccessful exit status),
- groups (to print the groups a specified user is a member of),
- id (to print the real/effective uid/gid),
- logname (to print the current login name),
- nice (to modify a scheduling priority),
- nohup (to allow a command to continue running after logging out),
- pathchk (to check a file name's portability),
- printenv (to print environment variables),
- printf (to format and print data),
- pwd (to print the current directory),
- seq (to print numeric sequences),
- sleep (to suspend execution for a specified time),
- stty (to print/change terminal settings),
- su (to become another user or the superuser),
- tee (to send output to multiple files),
- test (to evaluate an expression),
- true (to return a successful exit status),
- tty (to print the terminal name),
- uname (to print system information),
- users (to print current users' names),
- who (to print a list of the users who are currently logged in),
- whoami (to print the effective user id), and yes (to print a string
  indefinitely).

%description -l de
Die GNU-Shell-Utilities stellen viele der grundlegenden gemeinsamen
Befehle zur Verfügung, die unter anderem für die Shell- Programmierung
benutzt werden, woher sich der Name ableitet. Fast alle Shell-Skripts
benutzen wenigstens eines dieser Programme.

%description -l fr
Les utilitaires shell de GNU offrent la plupart des commandes de base
utilisées (entre autres) pour la programmation en shell, d'où le nom.
Presque tous les scripts shell utilisent au moins l'un de ces
programmes.

%description -l pl
Narzêdzia shell-a (GNU) zawieraj± wiele podstawowych komend u¿ywanych
(po¶ród innych rzeczy) w skryptach shell-a, st±d nazwa pakietu. Niemal
wszystkie skrypty shell-a u¿ywaj± co najmniej jednego z tych
programów.

%description -l tr
GNU kabuk araçlarý kabuk programlamada da kullanýlan pek çok ana
komutu saðlar. Hemen hemen tüm kabuk programlarý bu programlarýn en
azýndan birini kullanýr.


%prep
%setup -q
%patch1  -p1
%patch2  -p1
%patch3  -p1
%patch4  -p1
%patch5  -p1
%patch6  -p1
%patch7  -p1
%patch8  -p1
%patch9  -p1 -b .mint
%patch10 -p1 -b .getopt
find . -name \*.orig -exec rm -fv {} \;

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
perl -pi -e 's,/etc/utmp,/var/run/utmp,g' doc/sh-utils.texi man/logname.1 man/users.1 man/who.1
perl -pi -e 's,/etc/wtmp,/var/run/wtmp,g' doc/sh-utils.texi man/logname.1 man/users.1 man/who.1
rm -f doc/sh-utils.info

cp %{SOURCE2} man/help2man


%build
CFLAGS="${RPM_OPT_FLAGS} -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--disable-largefile \

make all info
make -C src getgid


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/{bin,usr/sbin}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

install -m 755 src/getgid ${RPM_BUILD_ROOT}%{_prefix}/bin/

# move some things to /bin
for i in date echo false hostname nice pwd sleep stty su true uname ; do
    install -m 755 -s ${RPM_BUILD_ROOT}%{_prefix}/bin/$i ${RPM_BUILD_ROOT}/bin/$i
    rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/$i
done

# copy some things to /bin
for i in basename test uptime; do
    install -m 755 -s ${RPM_BUILD_ROOT}%{_prefix}/bin/$i ${RPM_BUILD_ROOT}/bin/$i
done

chmod 4755 ${RPM_BUILD_ROOT}/bin/su

# don't supply chroot under MiNT
rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/chroot

# add symbolic links for the test
rm -f ${RPM_BUILD_ROOT}/bin/[
rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/[
ln ${RPM_BUILD_ROOT}/bin/test ${RPM_BUILD_ROOT}/bin/[
ln ${RPM_BUILD_ROOT}%{_prefix}/bin/test ${RPM_BUILD_ROOT}%{_prefix}/bin/[

# rename hostname so it don't conflict with the hostname rpm
mv ${RPM_BUILD_ROOT}/bin/hostname ${RPM_BUILD_ROOT}/bin/hostname.gnu
mv ${RPM_BUILD_ROOT}%{_prefix}/man/man1/hostname.1 ${RPM_BUILD_ROOT}%{_prefix}/man/man1/hostname.gnu.1

# don't ship su; it's in shadow-utils
rm ${RPM_BUILD_ROOT}/bin/su
rm ${RPM_BUILD_ROOT}%{_prefix}/man/man1/su.1

strip ${RPM_BUILD_ROOT}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/info/sh-utils* ||:
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%post
/sbin/install-info %{_prefix}/info/sh-utils.info.gz %{_prefix}/info/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_prefix}/info/sh-utils.info.gz %{_prefix}/info/dir
fi


%files
%defattr(-,root,root)
%doc NEWS README TODO
/bin/*
%{_prefix}/bin/*
%{_prefix}/info/sh-utils*
%{_prefix}/share/man/*/*
%{_prefix}/share/locale/*/*/*


%changelog
* Mon Sep 10 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.0.11

* Wed Aug 25 1999 Frank Naumann <fnaumann@cs.uni-magdeburg.de>
- compressed manpages
- correct Packager and Vendor
