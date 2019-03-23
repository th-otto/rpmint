Summary       : GNU patch Utilities
Summary(de)   : GNU-Patch-Utilities
Summary(fr)   : Utilitaires patch de GNU
Summary(tr)   : GNU yama yardýmcý programlarý
Name          : patch
Version       : 2.5.4
Release       : 2
Copyright     : GPL
Group         : Utilities/Text

Packager      : Frank Naumann <fnaumann@freemint.de>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/patch/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: ftp://ftp.gnu.org/pub/gnu/patch/patch-%{version}.tar.gz


%description
Patch is a program to aid in patching programs.  :-)
You can use it to apply 'diff's.  Basically, you can use
diff to note the changes in a file, send the changes to
someone who has the original file, and they can use 'patch'
to combine your changes to their original.

%description -l de
Patch ist ein Programm zum Patchen von Programmen.  :-)
Benutzen Sie zunächst das Diff-Programm, um die Änderungen
an der Datei zu ermitteln und senden Sie diese an die Leute
mit der Originaldatei. Diese können dann mit Hilfe von PATCH
ihre Dateien auf den neuesten Stand bringen.

%description -l fr
patch est un programme aidant à patcher des programmes. :-)
Vous pouvez l'utiliser pour appliquer des « diffs ». On utilise diff pour noter
les changements dans un fichier, on envoie ces changements à celui qui a le
fichier original et qui peut utiliser « patch » pour combiner nos modifications
avec son original.

%description -l tr
Bu programý 'diff' komutunu uygulamak için kullanabilirsiniz. diff, bir dosya
içindeki deðiþikliklerý belirtir; 'patch' komutu deðiþiklikleri asýllarý ile
birleþtirir.


%prep
%setup -q


%build
CFLAGS="${RPM_OPT_FLAGS}" \
./configure \
	--prefix=%{_prefix}

make "CFLAGS=$RPM_OPT_FLAGS -Dbase_name=basename"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix}

strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_prefix}/bin/*
%{_prefix}/share/man/*/*


%changelog
* Thu Sep 06 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 2.5.4

* Thu Aug 12 1999 Guido Flohr <gufl0000@stud.uni-sb.de>
- Changed vendor to Sparemint
- Edited German translation
