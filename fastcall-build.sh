#!/bin/sh

me="$0"

TARGET=${1:-m68k-atari-mint}

export KEEP_PKGDIR=no
export KEEP_SRCDIR=no

failed=""

for pkg in \
	gemlib \
	fdlibm \
	mintlib \
	cflib \
	a52dec \
	bzip2 \
	faad2 \
	flac \
	freetype2 \
	fribidi \
	giflib \
	jpeg \
	ldg \
	libmikmod \
	libiconv \
	libmad \
	libogg \
	libpng \
	libtheora \
	libvorbis \
	libvpx \
	libxmp \
	libxmp-lite \
	mpg123 \
	pth \
	sdl \
	sdl_gfx \
	sdl_image \
	sdl_mixer \
	sdl_net \
	sdl_sound \
	sdl_ttf \
	tiff \
	xz \
	zlib \
	zstd \
; do
	script=${pkg}-build.sh
	ls -l $script
	echo -ne "\033]2;$pkg\007"
	time ./$script ${TARGET} >/dev/null
	if test $? != 0; then
		failed="$failed $pkg"
	fi
done

echo -ne "\033]2;\007"

if test "$failed" != ""; then
	echo "failed: $failed" >&2
	exit 1
fi

exit 0

todo: krb5 (needs shared libs)
openldap2
