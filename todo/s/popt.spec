%prep
%setup -q
%patch0 -p1 -b .mint

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --disable-shared
make

%install
make DESTDIR=$RPM_BUILD_ROOT install
gzip -9nf $RPM_BUILD_ROOT/%{_prefix}/man/man3/popt.3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/lib/libpopt.a
%{_prefix}/include/popt.h
%{_prefix}/man/man3/popt.3.gz

%changelog
