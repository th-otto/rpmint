Name: 		bluemoon
Summary: 	Blue Moon solitaire (curses interface)
Version: 	2.9
Release: 	1
Packager:	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
URL: 		http://www.catb.org/~esr/bluemoon/
Source0: 	%{name}-%{version}.tar.gz
License: 	GPL
Group: 		Games
BuildRoot: 	%{_tmppath}/%{name}-root

%description
   This 52-card solitaire starts with  the entire deck shuffled and dealt
out in four rows.  The aces are then moved to the left end of the layout,
making 4 initial free spaces.  You may move to a space only the card that
matches the left neighbor in suit, and is one greater in rank.  Kings are
high, so no cards may be placed to their right (they create dead spaces).
  When no moves can be made,  cards still out of sequence are  reshuffled
and dealt face up after the ends of the partial sequences, leaving a card
space after each sequence, so that each row looks like a partial sequence
followed by a space, followed by enough cards to make a row of 14.
  A moment's reflection will show that this game cannot take more than 13
deals. A good score is 1-3 deals, 4-7 is average, 8 or more is poor.

%prep
%setup -q

%build
make bluemoon bluemoon.6

%install
[ "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"%{_bindir}
mkdir -p "$RPM_BUILD_ROOT"%{_mandir}/man6/
cp bluemoon "$RPM_BUILD_ROOT"%{_bindir}
cp bluemoon.6 "$RPM_BUILD_ROOT"%{_mandir}/man6/

%clean
[ "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf "$RPM_BUILD_ROOT"
%files
%defattr(-,root,root,-)
%{_mandir}/man6/bluemoon.6*
%{_bindir}/bluemoon
%doc README COPYING

%changelog
* Wed Feb 3 2004 Keith Scroggins <kws@radix.net>
- Initial build of bluemoon for MiNT.
