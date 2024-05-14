#!/bin/sh

me="$0"

TARGET=${1:-m68k-atari-mint}

export KEEP_PKGDIR=no
export KEEP_SRCDIR=no

failed=""

for pkg in \
	a52dec \
	asap \
	bzip2 \
	c-ares \
	cairo \
	cflib \
	curl \
	db \
	expat \
	faad2 \
	fdk-aac \
	fdlibm \
	ffmpeg \
	file \
	flac \
	freetype2 \
	fribidi \
	gdbm \
	gemlib \
	gemma \
	giflib \
	gmp \
	graphite2 \
	hermes \
	jpeg \
	ldg \
	libaacplus \
	libaom \
	libarchive \
	libass \
	libassuan \
	libbeecrypt \
	libde265 \
	libedit \
	libexif \
	libffi \
	libgcrypt \
	libgpg-error \
	libheif \
	libiconv \
	libidn2 \
	libksba \
	libmad \
	libmetalink \
	libmikmod \
	libogg \
	libpng \
	libpsl \
	libsndfile \
	libsolv \
	libssh2 \
	libtheora \
	libunistring \
	libuv \
	libvorbis \
	libwebp \
	libxml2 \
	libxmp \
	libyuv \
	lua51 \
	lua53 \
	mintlib \
	mp4v2 \
	mpc \
	mpfr \
	mpg123 \
	ncurses \
	netpbm \
	nghttp2 \
	openh264 \
	openssl \
	opus \
	physfs \
	pixman \
	popt \
	pth \
	readline \
	rhash \
	sdl \
	sdl_gfx \
	sdl_image \
	sdl_mixer \
	sdl_net \
	sdl_sound \
	sdl_ttf \
	smpeg \
	sqlite3 \
	tiff \
	windom \
	windom1 \
	wolfssl \
	x264 \
	x265 \
	xz \
	yaml-cpp \
	zita-resampler \
	zlib \
	zstd \
; do
	script=${pkg}-build.sh
	ls -l $script
	echo -ne "\033]2;$pkg\007"
	time ./$script ${TARGET}
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
