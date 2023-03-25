#!/bin/sh
set -e

topdir=`rpm --eval '%{_topdir}'`
cd "$topdir/RPMS"

createrepo .
gpg  --detach-sign --default-key CC2E22F1B6492FD3EACFF8BF3C9569A568969A28 --armor  --output - repodata/repomd.xml > repodata/repomd.xml.asc

# rsync -vv -rlptD --delete-during --info=progress . web196@server43.webgo24.de:~/www/download/rpm/RPMS

