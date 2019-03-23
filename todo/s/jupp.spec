# norootforbuild

Name:			jupp
Version:		3.1jupp18
Release:		1.14
Summary:		Wordstar compatible Text Editor which sucks less
License:		GPL v1
Group:			Productivity/Editors/Other
URL:			http://mirbsd.de/jupp
Source:			http://www.mirbsd.org/MirOS/dist/jupp/joe-%{version}.cpio.gz
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%ifnos FreeMiNT
BuildRequires:		cpio gcc glibc-devel ncurses-devel
%endif
Conflicts:		joe
AutoReqProv:		on

%description
“Joe is world-famous Wordstar like text editor.”
		-- Sourcefrog

joe is the professional freeware ASCII text screen editor for
UNIX®. It makes full use of the power and versatility of UNIX,
but lacks the steep learning curve and basic nonsense you have
to deal with in every other UNIX editor. jupp has the feel of
most IBM PC text editors: The key sequences are reminiscent of
WordStar and Turbo C. However, joe is much more powerful than
those editors. joe has all of the features a UNIX user should
expect: full use of termcap/terminfo, excellent screen update
optimizations (joe is fully usable at 2400 baud), simple in‐
stallation, and all of the UNIX-integration features of vi. A
number of reference cards are always available as online help
in an intuitive, simple, and well thought-out user interface,
with deferred screen update to handle typeahead, not bypassed
by tty buffering. SELinux context copying is supported (needs
the development headers installed, which we cannot do in this
portable SRPM).

joe has a great screen update optimization algorithm, multiple
windows (through/between which you can scroll) and lacks the
confusing notion of named buffers. It has command history, tab
expansion in file selection menus, undo and redo functions,
(un)indenting and paragraph formatting, filtering highlighted
blocks through any external Unix command, editing a pipe into
or out of a command, and block move, copy, delete or filter; a
rectangle selection and a picture drawing mode, and a mode to
display whitespace as printable characters.

jupp is a customisation of joe which provides easy conversion
for former PC users as well as powerfulness for programmers,
while not doing annoying things “automagically” (word wrap,
for example). It can also double as hex editor and comes with
a character map (ASCII / 8-bit) plus Unicode support.

This is joe-3.x-jupp<y>, a GNU GPL version 1 licenced fork
of the current state-of-the-art JOE editor from Sourceforge,
with Joe H. Allen himself starting development again after
over eight years. The MirOS fork has added UTF-8 Support for
non-LOCALE-aware operating systems (such as OpenBSD and older
versions of MirOS), the "jupp" flavour, not doing tab comple‐
tion in the search and replace dialogues, as well as -Wall
-Werror fixes, numerous bug and security fixes. It also con‐
tains an extension to visibly display tabs and spaces, and
has a cleaned up, extended and beautified options menu, and
more CUA style keybindings.

Unix integration features: a marked block of text can be
filtered through a UNIX command, and wherever jupp accepts
a filename parameter, the following can also be used:
	!command	: to redirect from or to another command
	>>filename	: to append onto an existing file
	fn,start,size	: to edit a part of a file or device
	-		: to use standard input/output

Authors:
	Joseph “Joe” H. Allen <jhallen@world.std.com>
	Marek “Marx” Grac <xgrac@fi.muni.cz>
	Thorsten “mirabilos” Glaser <tg@mirbsd.org>

%prep
%setup -q -T -c "jupp-%{version}"
%__gzip -dc "%{SOURCE0}" | cpio -mid

%build
cd jupp
CC="%__cc" CFLAGS="%{optflags}" sh configure \
    --prefix=%{_prefix} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir} \
    --docdir=%{_defaultdocdir}/%name \
    --disable-termidx \
    --disable-dependency-tracking
make sysconfjoesubdir=/jupp
cd .. #jupp

%install
cd jupp
make DESTDIR=$RPM_BUILD_ROOT install sysconfjoesubdir=/jupp
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}
cp COPYING HINTS INFO LIST NEWS README TODO docs/help-system.html \
    $RPM_BUILD_ROOT%{_docdir}/%{name}/
cd .. #jupp

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/jupp
%dir %{_sysconfdir}/jupp/charmaps
%dir %{_sysconfdir}/jupp/syntax
%config %{_sysconfdir}/jupp/*rc*
%config %{_sysconfdir}/jupp/charmaps/*
%config %{_sysconfdir}/jupp/syntax/*
%{_bindir}/*
%{_docdir}/%{name}
%doc %{_mandir}/man1/*

%changelog
* Wed Oct  5 2011 Thorsten Glaser <tg@mirbsd.org> 3.1jupp18-1
- new upstream version; changelog: https://www.mirbsd.org/jupp.htm#r3_1j18
* Wed Aug  3 2011 Thorsten Glaser <tg@mirbsd.org> 3.1jupp17-1
- new upstream version; changelog: https://www.mirbsd.org/jupp.htm#r3_1j17
* Sat Jul 16 2011 Thorsten Glaser <tg@mirbsd.org> 3.1jupp16-1
- new upstream version; changelog: https://www.mirbsd.org/jupp.htm#r3_1j16
* Sat Jul  2 2011 Thorsten Glaser <tg@mirbsd.org> 3.1jupp15-1
- new upstream version; changelog: https://www.mirbsd.org/jupp.htm#r3_1j15
* Tue Mar 22 2011 Thorsten Glaser <t.glaser@tarent.de> 3.1jupp14-3
- conflict with joe (reported by gecko2@mirbsd, fix confirmed by rsc@fedora)
* Tue Apr  8 2010 Thorsten Glaser <tg@mirbsd.org> 3.1jupp14-2
- mitigate some compiler warnings
* Tue Apr  8 2010 Thorsten Glaser <tg@mirbsd.org> 3.1jupp14-1
- new upstream; changelog: https://www.mirbsd.org/jupp.htm#r3_1j14
* Sun Oct 18 2009 Thorsten Glaser <tg@mirbsd.org> 3.1jupp12-1
- new upstream; changelog: https://www.mirbsd.org/jupp.htm#r3_1j12
* Mon Aug  3 2009 Thorsten Glaser <tg@mirbsd.org> 3.1jupp11-12
- initial package
