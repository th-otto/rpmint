%define  ver     2b29
%define  rel     2
%define  prefix  /usr

Summary:	Converts UNIX mailbox files into a set of HTML pages
Name:		hypermail
Version: 	%ver
Release: 	%rel
Copyright: 	GPL
Group: 		Applications/Mail
Patch0:		%{name}-mintcfg.patch
Patch1:		%{name}-mint.patch
Patch2:		%{name}-lang.patch
Source: 	%{name}-%{version}.tar.gz
Prefix: 	%prefix
BuildRoot: 	/var/tmp/%{name}-root
Distribution: 	Sparemint
Vendor: 	Sparemint
Packager: 	Edgar Aichinger <eaiching@t0.or.at>
Summary(de):	Konvertiert UNIX Mailbox-Dateien in HTML-Seiten

%description
Hypermail is a program that takes a file of mail messages in UNIX 
mailbox format and generates a set of cross-referenced HTML 
documents. Each file that is created represents a separate message in 
the mail archive and contains links to other articles, so that the 
entire archive can be browsed in a number of ways by following links. 
Archives generated by Hypermail can be incrementally updated, and 
Hypermail is set by default to only update archives when changes are 
detected.
In addition, Hypermail will convert references in each message to 
email addresses and URLs to hyperlinks so they can be selected. Email 
addresses can be converted to mailto: URLs or links to a CGI mail 
program. 
To complement each set of HTML messages, four index files are created 
which sort the articles by date received, thread, subject, and 
author. Each entry in these index files are links to the individual 
articles and provide a bird's-eye view of every archived message.

%description -l de
Hypermail ist ein Programm, das aus einer Datei mit Mail-Nachrichten
im UNIX mailbox-Format einen Satz von HTML-Dateien mit Querverweisen
erzeugt. Jede der erzeugten Dateien repr�sentiert eine separate
Nachricht im Mail-Archiv und enth�lt Hyperlinks auf andere Artikel,
so dass das ganze Archiv auf verschiedene Weise gelesen werden kann,
indem man den Links folgt. Von Hypermail erzeugte Archive k�nnen
inkrementell auf neuesten Stand gebracht werden, und Hypermail ist so
voreingestellt, dass es Archive nur erneuert, wenn �nderungen entdeckt
werden.
Ausserdem kann Hypermail die Referenzen auf Email-Adressen und URLs
in jeder Nachricht in Hyperlinks konvertieren, sodass sie angew�hlt 
werden k�nnen. Email-Adressen k�nnen in mailto: URLs oder Links auf
ein CGI Mail-Programm konvertiert werden. 
Zur Erg�nzung werden vier Indexdateien erzeugt, die die Artikel nach
Empfangsdatum, Threads, Betreff und Autor sortieren. Die Eintr�ge in
diesen Indexdateien sind Links auf die einzelnen Artikel und bieten
einen schnellen �berblick �ber alle archivierten Nachrichten.

%prep
%setup -q
%patch0 -p1 -b .mintcfg
%patch1 -p1 -b .mint
%patch2 -p1 -b .de

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%prefix --host=m68k-atari-mint
make

%install
make 	prefix=$RPM_BUILD_ROOT%prefix \
	exec_prefix=$RPM_BUILD_ROOT%prefix \
	htmldir=../html \
	install
strip $RPM_BUILD_ROOT%prefix/bin/%{name}
strip $RPM_BUILD_ROOT%prefix/bin/msg2archive
strip $RPM_BUILD_ROOT%prefix/bin/rdmsg
gzip -9nf $RPM_BUILD_ROOT%prefix/share/man/man1/%{name}.1
gzip -9nf $RPM_BUILD_ROOT%prefix/share/man/man4/hmrc.4
install -d $RPM_BUILD_ROOT%prefix/share/hypermail
install -c -m 0644 configs/* $RPM_BUILD_ROOT%prefix/share/hypermail

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%prefix/bin/*
%prefix/share/hypermail/*
%prefix/share/man/man1/*
%prefix/share/man/man4/*
%doc README TODO KNOWN_BUGS UPGRADE README.CVS COPYING Changelog html/* docs/attachments.txt

%changelog
* Fri Apr 21 2000 Edgar Aichinger <eaiching@t0.or.at>
- build against mintlibs 0.55.2

* Tue Feb 08 2000 Edgar Aichinger <eaiching@t0.or.at>
- first release for SpareMiNT (new package)
