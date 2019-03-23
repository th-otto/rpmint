Summary		: MAD (libmad) is a high-quality MPEG audio decoder
Name		: libmad
Version		: 0.15.1b
Release		: 1
Source		: ftp://ftp.mars.org/pub/mpeg/%{name}-%{version}.tar.gz
URL		: http://www.underbit.com/pruducts/mad/
License		: GPL
Group		: Development/Libraries
Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
BuildRoot	: /var/tmp/%{name}-%{version}-root
Prefix		: %{_prefix}

%define __defattr %defattr(-,root,root)

%description
  MAD (libmad) is a high-quality MPEG audio decoder. It currently supports
  MPEG-1 and the MPEG-2 extension to Lower Sampling Frequencies, as well as
  the so-called MPEG 2.5 format. All three audio layers (Layer I, Layer II,
  and Layer III a.k.a. MP3) are fully implemented.

  MAD does not yet support MPEG-2 multichannel audio (although it should be
  backward compatible with such streams) nor does it currently support AAC.

%prep
%setup -q 

%build
CFLAGS="-mcpu=5475 -O3" ./configure \
	--host=m68k-atari-mint \
	--prefix=%{prefix}
make

mkdir savlibs
mv .libs/libmad.a savlibs/libmadCF.a
mv .libs/libmad.lai savlibs/libmadCF.la
make clean

CFLAGS="-m68020-60 -O3" ./configure \
	--prefix=%{prefix} 
make
mv .libs/libmad.a savlibs/libmad020-60.a
mv .libs/libmad.lai savlibs/libmad020-60.la
make clean

CFLAGS="-O3" ./configure \
	--prefix=%{prefix} 
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{prefix}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475

install -m644 savlibs/libmadCF.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libmad.a
install -m644 savlibs/libmadCF.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libmad.la
sed "s#/usr/lib#/usr/lib/m5475#" ${RPM_BUILD_ROOT}%{_prefix}/lib/libmad.la > ${RPM_BUILD_ROOT}%{_prefix}/lib/m5475/libmad.la

install -m644 savlibs/libmad020-60.a ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libmad.a
install -m644 savlibs/libmad020-60.la ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libmad.la
sed "s#/usr/lib#/usr/lib/m68020-60#" ${RPM_BUILD_ROOT}%{_prefix}/lib/libmad.la > ${RPM_BUILD_ROOT}%{_prefix}/lib/m68020-60/libmad.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{__defattr}
%doc CHANGES COPYRIGHT COPYING CREDITS INSTALL README TODO VERSION
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/m5475/lib*.a
%{_libdir}/m5475/lib*.la
%{_libdir}/m68020-60/lib*.a
%{_libdir}/m68020-60/lib*.la
%{_includedir}/mad.h

%changelog
* Tue Oct 12 2010 Keith Scroggins <kws@radix.net>
- Initial build of libmad for SpareMiNT
