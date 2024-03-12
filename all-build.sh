#!/bin/sh

me="$0"

TARGET=${1:-m68k-atari-mint}

export KEEP_PKGDIR=no
export KEEP_SRCDIR=no

failed=""

for pkg in \
	a52dec \
	arc \
	arj \
	asap \
	autoconf \
	autoconf-archive \
	automake \
	bash \
	bison \
	bzip2 \
	c-ares \
	ca-certificates \
	cairo \
	cflib \
	cmake \
	coreutils \
	cpio \
	ctris \
	curl \
	db \
	dhcp \
	diffutils \
	dosfstools \
	elfutils \
	expat \
	fdk-aac \
	fdlibm \
	file \
	findutils \
	flac \
	flex \
	freetype2 \
	fribidi \
	gawk \
	gdbm \
	gemlib \
	gemma \
	gettext \
	giflib \
	git \
	gmp \
	grep \
	groff \
	gzip \
	help2man \
	hermes \
	jpeg \
	krb5 \
	ldg \
	lha \
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
	m4 \
	make \
	man \
	mintbin \
	mintlib \
	mksh \
	mp4v2 \
	mpc \
	mpfr \
	mpg123 \
	mtm \
	ncurses \
	netpbm \
	nghttp2 \
	openh264 \
	openssl \
	opus \
	p7zip \
	patch \
	perl \
	physfs \
	ping \
	pixman \
	pml \
	pngtools \
	popt \
	pth \
	python2 \
	python3 \
	readline \
	rhash \
	rpm \
	sdl \
	sdl_gfx \
	sdl_image \
	sdl_mixer \
	sdl_net \
	sdl_sound \
	sdl_ttf \
	sed \
	smpeg \
	sqlite3 \
	tar \
	tiff \
	traceroute \
	tree \
	unrar \
	unzip \
	vorbis-tools \
	wget \
	windom \
	windom1 \
	wolfssl \
	x264 \
	x265 \
	xz \
	zip \
	zita-resampler \
	zlib \
	zoo \
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
