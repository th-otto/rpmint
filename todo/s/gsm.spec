Summary       : gsm
Name          : gsm
Version       : 1.0.10
Release       : 1
Copyright     : distributable
Group         : Applications/Multimedia

Packager      : Marc-Anton Kehr <m.kehr@ndh.net>
Vendor        : Sparemint

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: gsm-%{version}.tar.gz
Patch0: gsm-1.0.10-mint.patch


%description
GSM 06.10 compresses frames of 160 13-bit samples (8 kHz sampling
rate, i.e. a frame rate of 50 Hz) into 260 bits; for compatibility
with typical UNIX applications, our implementation turns frames of 160
16-bit linear samples into 33-byte frames (1650 Bytes/s).
The quality of the algorithm is good enough for reliable speaker
recognition; even music often survives transcoding in recognizable 
form (given the bandwidth limitations of 8 kHz sampling rate).


%prep
%setup -q
%patch0 -p1


%build
make CC="gcc ${RPM_OPT_FLAGS}"


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/{bin,include,lib,share/man/{man1,man3}}
install bin/tcat 		${RPM_BUILD_ROOT}%{_prefix}/bin/tcat
install bin/toast 		${RPM_BUILD_ROOT}%{_prefix}/bin/toast
install bin/untoast 		${RPM_BUILD_ROOT}%{_prefix}/bin/untoast
install inc/gsm.h 		${RPM_BUILD_ROOT}%{_prefix}/include/gsm.h
install lib/libgsm.a 		${RPM_BUILD_ROOT}%{_prefix}/lib/libgsm.a
install man/bitter.1 		${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/bitter.1
install man/toast.1 		${RPM_BUILD_ROOT}%{_prefix}/share/man/man1/toast.1
install man/gsm.3 		${RPM_BUILD_ROOT}%{_prefix}/share/man/man3/gsm.3
install man/gsm_explode.3 	${RPM_BUILD_ROOT}%{_prefix}/share/man/man3/gsm_explode.3
install man/gsm_option.3	${RPM_BUILD_ROOT}%{_prefix}/share/man/man3/gsm_option.3
install man/gsm_print.3		${RPM_BUILD_ROOT}%{_prefix}/share/man/man3/gsm_print.3

gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/share/man/*/*
strip ${RPM_BUILD_ROOT}%{_prefix}/bin/* ||:


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files
%doc README COPYRIGHT MACHINES
%attr(0755,root,root)	%{_prefix}/bin/tcat
%attr(0755,root,root)	%{_prefix}/bin/toast
%attr(0755,root,root)	%{_prefix}/bin/untoast
%attr(0644,root,root)	%{_prefix}/include/gsm.h
%attr(0644,root,root)	%{_prefix}/lib/libgsm.a
%attr(0644,root,root)	%{_prefix}/share/man/man1/bitter.1.gz
%attr(0644,root,root)	%{_prefix}/share/man/man3/gsm.3.gz
%attr(0644,root,root)	%{_prefix}/share/man/man3/gsm_explode.3.gz
%attr(0644,root,root)	%{_prefix}/share/man/man3/gsm_option.3.gz
%attr(0644,root,root)	%{_prefix}/share/man/man3/gsm_print.3.gz
%attr(0644,root,root)	%{_prefix}/share/man/man1/toast.1.gz


%changelog
* Sun Feb 18 2001 Marc-Anton Kehr <m.kehr@ndh.net>
- build against MiNTLib 0.56
