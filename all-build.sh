#!/bin/sh

me="$0"

TARGET=${1:-m68k-atari-mint}

export KEEP_PKGDIR=no
export KEEP_SRCDIR=no

for pkg in \
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
	libarchive \
	libassuan \
	libbeecrypt \
	libde265 \
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
	libsolv \
	libssh2 \
	libtheora \
	libunistring \
	libuv \
	libwebp \
	libxml2 \
	libxmp \
	libyuv \
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
	p7zip \
	patch \
	perl \
	physfs \
	pml \
	pngtools \
	popt \
	python2 \
	python3 \
	readline \
	rhash \
	rpm \
	sdl \
	sdl_image \
	sdl_mixer \
	sdl_net \
	sdl_ttf \
	sed \
	smpeg \
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
	libx265 \
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
	: time ./$script ${TARGET}
done

echo -ne "\033]2;\007"

exit 0

todo: krb5 (needs shared libs)
openldap2
