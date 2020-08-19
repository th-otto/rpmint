rpmbuild -bb bzip2.spec
rpmbuild --target m68k-atari-mint --define="buildtype 000" -bb bzip2.spec
rpmbuild --target m68020-atari-mint --define="buildtype 020" -bb bzip2.spec
rpmbuild --target m5475-atari-mint --define="buildtype v4e" -bb bzip2.spec
