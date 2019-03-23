Version:	1.5
Release:	1
Summary:	Data compression utility using LZMA with fast decompress
Name:		lzip
Source0:  http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
Patch0:		lzip-1.5-mint.patch
License:	GPL
Group:		System Environment/Libraries
URL:		http://www.nongnu.org/lzip/lzip.html
Packager:	Keith Scroggins <kws@radix.net>
Vendor:		Sparemint
BuildRoot:	/var/tmp/%{name}-%{version}-root

# For newer versions of RPM so native strip and debuginfo are not utilized
# when cross compiling
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}
%define is_sparemint %(test -e /etc/sparemint-release && echo 1 || echo 0)


%description
    Lzip is a lossless file compressor based on the LZMA
    (Lempel-Ziv-Markov chain-Algorithm) algorithm, designed by Igor
    Pavlov. The high compression of LZMA comes from combining two basic,
    well-proven compression ideas: sliding dictionaries (i.e. LZ77/78),
    and Markov models (i.e. the thing used by every compression
    algorithm that uses a range encoder or similar order-0 entropy coder
    as its last stage) with segregation of contexts according to what
    the bits are used for. Lzip has a user interface similar to the one
    of gzip(1) or bzip2(1).

%prep
%setup -q
%patch0 -p1
%build
./configure CFLAGS="-O2 -fomit-frame-pointer" CC=m68k-atari-mint-gcc \
        --prefix=/usr CXX=m68k-atari-mint-g++ \
	CXXFLAGS="-O2 -fomit-frame-pointer"
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT"
# I have no clue why this is not installed....
cp lziprecover $RPM_BUILD_ROOT/usr/bin
rm $RPM_BUILD_ROOT/usr/share/info/dir
gzip -9nf $RPM_BUILD_ROOT/usr/share/info/*
gzip -9nf $RPM_BUILD_ROOT/usr/share/man/man1/*

%if %is_sparemint
strip $RPM_BUILD_ROOT/usr/bin/lzip
strip $RPM_BUILD_ROOT/usr/bin/lziprecover
stack -S 256k $RPM_BUILD_ROOT/usr/bin/lzip
stack -S 256k $RPM_BUILD_ROOT/usr/bin/lziprecover
%else
m68k-atari-mint-strip $RPM_BUILD_ROOT/usr/bin/lzip
m68k-atari-mint-strip $RPM_BUILD_ROOT/usr/bin/lziprecover
m68k-atari-mint-stack -S 256k $RPM_BUILD_ROOT/usr/bin/lzip
m68k-atari-mint-stack -S 256k $RPM_BUILD_ROOT/usr/bin/lziprecover
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc AUTHORS COPYING NEWS README
%attr(0755,root,root) /usr/bin/lzip*
%attr(0644,root,root) /usr/share/info/*
%attr(0644,root,root) /usr/share/man/man1/*

%changelog
* Fri May 15 2009 Keith Scroggins <kws@radix.net>
- Initial build of lzip RPM using Cross Compilers!
