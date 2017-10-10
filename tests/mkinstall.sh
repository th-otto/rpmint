#!/bin/sh

TARGET=${1-m68k-atari-mint}
PREFIX=/usr
PKG_DIR=`pwd`/binary-package

sudo cp -pvr $PKG_DIR$PREFIX/bin/$TARGET-* $PREFIX/bin
sudo cp -pvr $PKG_DIR$PREFIX/$TARGET/. $PREFIX/$TARGET/
sudo cp -pvr $PKG_DIR$PREFIX/lib64/gcc/$TARGET/. $PREFIX/lib64/gcc/$TARGET/
