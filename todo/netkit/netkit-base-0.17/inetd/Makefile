all: inetd

include ../MCONFIG
include ../MRULES

OBJS=inetd.o servtab.o builtins.o sig.o daemon.o setproctitle.o mysleep.o

inetd: $(OBJS)
	$(CC) $(LDFLAGS) $^ $(LIBS) -o $@

$(OBJS): builtins.h daemon.h inetd.h mysleep.h pathnames.h servtab.h \
         setproctitle.h sig.h

include depend.mk
depend:
	$(CC) $(CFLAGS) -MM *.c > depend.mk

install: inetd
	install -m$(DAEMONMODE) inetd $(INSTALLROOT)$(SBINDIR)
	install -m$(MANMODE) inetd.8 $(INSTALLROOT)$(MANDIR)/man8

clean:
	rm -f *.o inetd
