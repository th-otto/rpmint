#!/bin/sh
cd RPMS
createrepo .
gpg  --detach-sign --default-key CC2E22F1B6492FD3EACFF8BF3C9569A568969A28 --armor  --output - repodata/repomd.xml > repodata/repomd.xml.asc

