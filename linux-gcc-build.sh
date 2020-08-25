$HOME/m68k-atari-mint-gcc/configure --prefix=/usr --libdir=/usr/lib64 --bindir=/usr/bin \
	'CFLAGS_FOR_BUILD=-O2 -fomit-frame-pointer' \
	'CFLAGS=-O2 -fomit-frame-pointer' \
	'CXXFLAGS_FOR_BUILD=-O2 -fomit-frame-pointer' \
	'CXXFLAGS=-O2 -fomit-frame-pointer' \
	'BOOT_CFLAGS=-O2 -fomit-frame-pointer' \
	'CFLAGS_FOR_TARGET=-O2 -fomit-frame-pointer' \
	'CXXFLAGS_FOR_TARGET=-O2 -fomit-frame-pointer' \
	'LDFLAGS_FOR_BUILD=' \
	'LDFLAGS=' \
	--disable-libvtv \
	--disable-libmpx \
	--disable-libcc1 \
	--disable-werror \
	--with-gxx-include-dir=/usr/include/c++/10 \
	--with-gcc-major-version-only \
	--with-gcc --with-gnu-as --with-gnu-ld \
	--with-system-zlib \
	--disable-libgomp \
	--without-newlib \
	--disable-libstdcxx-pch \
	--disable-win32-registry \
	--disable-lto \
	--enable-ssp --enable-libssp \
	--disable-plugin \
	--enable-languages=c,c++

# time make -j8 all-gcc
# time make -j8 all-target-libgcc
# time make -j8
