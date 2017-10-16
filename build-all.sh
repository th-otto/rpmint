#!/bin/sh

me="$0"

export KEEP_PKGDIR=no
export KEEP_SRCDIR=no

for pkg in gemlib \
	cflib \
	gemma \
	pml \
	mintlib \
	ldg \
	windom \
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
	zoo
; do
	script=build-${pkg}.sh
	ls -l $script
done
