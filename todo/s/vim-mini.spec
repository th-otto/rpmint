Summary       : The VIM editor.
Name          : vim
Version       : 6.0
Release       : 1
Copyright     : freeware
Group         : Applications/Editors

Packager      : Marc-Anton Kehr <m.kehr@ndh.net>
Vendor        : Sparemint
URL           : http://www.vim.org/

%ifarch m68kmint
Buildrequires : mintbin sed
%else
Buildrequires : sed
%endif

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source0: ftp://ftp.oce.nl/pub/vim/unix/vim-%{version}.tar.gz
Source1: vimrc
Patch0: vim-5.5-include.patch
Patch1: vim-6.0-typeahead.patch

Obsoletes:  vim-minimal

%description
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, visual block operations, syntax highlightning and more.

Note: This package installs two versions of vim: /bin/vi is as small as
possible (most features disabled), while /usr/bin/vim has almost all
features enabled (and is therefore almost twice as big).

%package minimal
Summary: A minimal version of the VIM editor.
Group: Applications/Editors
Obsoletes:  vim

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the
vi editor.  Vi was the first real screen-based editor for UNIX, and is
still very popular.  VIM improves on vi by adding new features:
multiple windows, multi-level undo, block highlighting and more. The
vim-minimal package includes a minimal version of VIM, which is
installed into /bin/vi for use when only the root partition is
present.

%prep
%setup -q -n vim60
%patch0 -p1 -b .include
%patch1 -p1 -b .typeahead


%build
cd src

CFLAGS="-O -fomit-frame-pointer -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--prefix=%{_prefix} \
	--with-features=normal \
	--disable-pythoninterp \
	--disable-perlinterp \
	--disable-tclinterp \
	--with-x=no \
	--enable-gui=no
make vim
%ifarch m68kmint
stack --fix=128k vim
%endif
cp vim normal-vim
make clean

CFLAGS="-O -fomit-frame-pointer -D_GNU_SOURCE" \
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=/ \
	--with-features=tiny \
	--disable-pythoninterp \
	--disable-perlinterp \
	--disable-tclinterp \
	--with-x=no \
	--enable-gui=no
make
%ifarch m68kmint
stack --fix=128k vim
%endif


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

cd src
make install \
	prefix=${RPM_BUILD_ROOT}%{_prefix} \
	exec_prefix=${RPM_BUILD_ROOT}/ \
	MANDIR=${RPM_BUILD_ROOT}%{_prefix}/share/man

make installmacros \
	DEST=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
install -m755 normal-vim ${RPM_BUILD_ROOT}%{_prefix}/bin/vim

mv -f ${RPM_BUILD_ROOT}/bin/vim ${RPM_BUILD_ROOT}/bin/vi
mv -f ${RPM_BUILD_ROOT}/bin/xxd   ${RPM_BUILD_ROOT}%{_prefix}/bin

rm -f ${RPM_BUILD_ROOT}/bin/rvim

ln -sf vi ${RPM_BUILD_ROOT}/bin/view
ln -sf vi ${RPM_BUILD_ROOT}/bin/ex
ln -sf vi ${RPM_BUILD_ROOT}/bin/rvi
ln -sf vi ${RPM_BUILD_ROOT}/bin/rview
ln -sf vim ${RPM_BUILD_ROOT}%{_prefix}/bin/vi
ln -sf vim ${RPM_BUILD_ROOT}%{_prefix}/bin/ex

for i in ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/vim.1 \
  ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/vimtutor.1
do
  mv $i $i.orig
  sed -e "s,${RPM_BUILD_ROOT},," < $i.orig > $i
  rm -f $i.orig
done
rm -f ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/rvim.1
ln -sf vim.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/vi.1
ln -sf vim.1 ${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/rvi.1

install -m644 $RPM_SOURCE_DIR/vimrc ${RPM_BUILD_ROOT}%{_prefix}/share/vim/

# strip anything
strip ${RPM_BUILD_ROOT}/bin/* ||:
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/man*/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
%doc README*.txt runtime/macros/README.txt runtime/tools/README.txt
%doc runtime/doc runtime/syntax runtime/termcap runtime/tutor
%doc runtime/*.vim
/bin/*
%{_prefix}/bin/*
%{_prefix}/share/man/man*/*
%{_prefix}/share/vim


%files minimal
%defattr(-,root,root)
/bin/ex
/bin/vi
/bin/view
/bin/rvi
/bin/rview


%changelog
* Fri Mar 7 2003 Standa Opichal <opichals@seznam.cz>
- minimal package created.

* Thu Oct 04 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 6.0

* Thu Oct 28 1999 Thomas Binder <gryf@hrzpub.tu-darmstadt.de>
- initial revision for SpareMiNT, without gvim, without interpreters, without
  different packages; also fixes some flaws in Red Hat's original spec file,
  which was installing vimrc with `install -s' (and into the wrong
  location), as if it was a binary, and completely ignoring the ctags
  and etags binaries, even though they (and xxd) got compiled for all
  three packages

%changelog tiny

