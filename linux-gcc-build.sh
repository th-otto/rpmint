srcdir=$HOME/m68k-atari-mint-gcc
BASE_VER=$(cat $srcdir/gcc/BASE-VER)
gcc_dir_version=$(echo $BASE_VER | cut -d '.' -f 1)

CFLAGS="-O2 -fomit-frame-pointer"

$srcdir/configure --prefix=/usr --libdir=/usr/lib64 --libexecdir=/usr/lib64 --bindir=/usr/bin \
	CFLAGS_FOR_BUILD="$CFLAGS" \
	CFLAGS="$CFLAGS" \
	CXXFLAGS_FOR_BUILD="$CFLAGS" \
	CXXFLAGS="$CFLAGS" \
	BOOT_CFLAGS="$CFLAGS" \
	CFLAGS_FOR_TARGET="$CFLAGS" \
	CXXFLAGS_FOR_TARGET="$CFLAGS" \
	'LDFLAGS_FOR_BUILD=' \
	'LDFLAGS=' \
	--disable-libvtv \
	--disable-libmpx \
	--disable-libcc1 \
	--disable-werror \
	--with-gxx-include-dir=/usr/include/c++/$gcc_dir_version \
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
	--enable-languages=c,c++,ada,fortran,m2

# time make -j8 all-gcc
# time make -j8 all-target-libgcc
# time make -j8
