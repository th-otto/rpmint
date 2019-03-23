Summary       : GNU Pth - The GNU Portable Threads
Name          : pth
Version       : 2.0.0
Release       : 1
Copyright     : GPL
Group         : System Environment/Libraries

Packager      : Keith Scroggins <kws@radix.net>
Vendor        : Sparemint
URL           : http://www.gnu.org/software/pth/

Prefix        : %{_prefix}
Docdir        : %{_prefix}/doc
BuildRoot     : %{_tmppath}/%{name}-root

Source: %{name}-%{version}.tar.gz
Patch0: pth-2.0.0-mint.patch


%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms which
provides non-preemptive priority-based scheduling for multiple threads of
execution (aka ``multithreading'') inside event-driven applications. All
threads run in the same address space of the server application, but each
thread has it's own individual program-counter, run-time stack, signal
mask and errno variable.

The thread scheduling itself is done in a cooperative way, i.e., the
threads are managed by a priority- and event-based non-preemptive
scheduler. The intention is that this way one can achieve better
portability and run-time performance than with preemptive scheduling. The
event facility allows threads to wait until various types of events occur,
including pending I/O on filedescriptors, asynchronous signals, elapsed
timers, pending I/O on message ports, thread and process termination, and
even customized callback functions.

Additionally Pth provides an optional emulation API for POSIX.1c threads
("Pthreads") which can be used for backward compatibility to existing
multithreaded applications.

%package devel
Summary       : GNU Pth development package
Group         : Development/Libraries
#Requires      : %{name} = %{version}

%description devel
Pth is a very portable POSIX/ANSI-C based library for Unix platforms which
provides non-preemptive priority-based scheduling for multiple threads of
execution (aka ``multithreading'') inside event-driven applications. All
threads run in the same address space of the server application, but each
thread has it's own individual program-counter, run-time stack, signal
mask and errno variable.

The thread scheduling itself is done in a cooperative way, i.e., the
threads are managed by a priority- and event-based non-preemptive
scheduler. The intention is that this way one can achieve better
portability and run-time performance than with preemptive scheduling. The
event facility allows threads to wait until various types of events occur,
including pending I/O on filedescriptors, asynchronous signals, elapsed
timers, pending I/O on message ports, thread and process termination, and
even customized callback functions.

Additionally Pth provides an optional emulation API for POSIX.1c threads
("Pthreads") which can be used for backward compatibility to existing
multithreaded applications.

Headers and Static Libraries.


%prep
%setup -q
%patch0 -p1

%build
autoconf
LIBS=-lsocket \
./configure \
	--prefix=%{_prefix} \
	--enable-pthread \
	--enable-syscall-soft
make
make test


%install
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}
make prefix=${RPM_BUILD_ROOT}%{_prefix} install

# compress manpages
gzip -9nf ${RPM_BUILD_ROOT}%{_prefix}/man/*/* ||:

# make q-funk happy
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/share
mv ${RPM_BUILD_ROOT}%{_prefix}/man ${RPM_BUILD_ROOT}%{_prefix}/share/


%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}


%files devel
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS COPYING ChangeLog HACKING HISTORY NEWS PORTING README
%doc SUPPORT TESTS THANKS USERS
%{_prefix}/bin/*
%{_prefix}/include/*.h
%{_prefix}/lib/libpth*.a
%{_prefix}/lib/libpth*.la
%{_prefix}/share/aclocal/*.m4
%{_prefix}/share/man/*/*


%changelog
* Mon Oct 30 2003 Keith Scroggins <kws@radix.net>
- Updated to 2.0.0 and fixed 1 patch to apply correctly

* Wed Jun 20 2001 Frank Naumann <fnaumann@freemint.de>
- recompiled with pthread interface and soft syscall mapping

* Thu May 29 2001 Frank Naumann <fnaumann@freemint.de>
- updated to 1.4

* Sat Mar 17 2001 Frank Naumann <fnaumann@freemint.de>
- initial revision for SpareMiNT
