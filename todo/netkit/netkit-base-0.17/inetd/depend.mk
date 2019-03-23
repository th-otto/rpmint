builtins.o: builtins.c servtab.h builtins.h setproctitle.h
daemon.o: daemon.c daemon.h
inetd.o: inetd.c ../version.h pathnames.h inetd.h servtab.h sig.h \
 daemon.h setproctitle.h
servtab.o: servtab.c inetd.h servtab.h builtins.h sig.h
setproctitle.o: setproctitle.c setproctitle.h inetd.h
sig.o: sig.c sig.h
