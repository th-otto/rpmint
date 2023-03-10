#!/bin/sh

me="$0"

export KEEP_PKGDIR=no
export KEEP_SRCDIR=no

for pkg in gemlib \
	cflib \
	gemma \
	pml \
	mintbin \
	mintlib \
	ldg \
	windom \
	windom1 \
	bzip2 \
	zlib \
	libpng \
	sdl \
	ncurses \
	readline \
	openssl \
	arc \
	arj \
	iconv \
	lha \
	unrar \
	xz \
	zip \
	unzip \
	zoo \
	gmp \
	mpfr \
	mpc \
	tar \
	libiconv \
	m4 \
	flex \
	bison \
	expat \
	libidn2 \
	libssh2 \
	nghttp2 \
	libxml2 \
	libmetalink \
	libunistring \
	libpsl \
	curl \
	jpeg \
	hermes \
	gzip \
	grep \
	ctris \
	dhcp \
	gawk \
	file \
	diffutils \
	coreutils \
	bash \
	make \
	patch \
	groff \
	git \
	ca-certificates \
	gdbm \
	db \
	perl \
	autoconf \
	autoconf-archive \
	automake \
	libbeecrypt6 \
	lua53 \
	popt \
	rhash \
	libarchive \
	elfutils \
	libuv \
	cmake \
	libsolv \
	python2 \
	python3 \
	libffi \
	libgpg-error \
	libassuan \
	gettext \
	libksba \
	libgcrypt \
; do
	script=${pkg}-build.sh
	ls -l $script
done

exit 0

todo: krb5 (needs shared libs)
openldap2
