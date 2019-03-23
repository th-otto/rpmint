Summary		: GCC C Compiler for the m56000 DSP series
Name		: gcc-56k
Version		: 1.37
Release		: 1
Source		: gcc-56k.tar.bz2
Patch0		: gcc56k-mint.patch
URL		: http://gcc.gnu.org
License		: GPL
Group		: Development/Languages
Packager	: Keith Scroggins <kws@radix.net>
Vendor		: Sparemint
BuildRoot	: /var/tmp/%{name}-%{version}-root
Prefix		: %{_prefix}

%define __defattr %defattr(-,root,root)

%description
This is GCC 1.37 which was patched by Motorola to compile code for the 56000
series DSP, like the 56001 DSP found in the Atari Falcon.  This code has been
further patched to compile and run under FreeMiNT.  More work needs to be done
for getting the assembler side functioning as the original Motorola assembler
release for the Falcon does not behave with this package.

%prep
%setup -q -n gcc-56k
%patch0 -p1 -b .warn

%build
./config.gcc dsp56k-atari
make dsp

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/local/bin
install -m755 gccnew ${RPM_BUILD_ROOT}%{_prefix}/local/bin/g56k
install -m755 cc1 ${RPM_BUILD_ROOT}%{_prefix}/local/bin/g56-cc1
install -m755 cpp ${RPM_BUILD_ROOT}%{_prefix}/local/bin/mcpp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{__defattr}
%{_prefix}/local/bin/g56k
%{_prefix}/local/bin/g56-cc1
%{_prefix}/local/bin/mcpp

%changelog
* Fri Nov 12 2010 Keith Scroggins <kws@radix.net>
- Initial release of gcc-56k for SpareMiNT
