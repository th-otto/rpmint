#!/bin/sh

cat << EOF
<?php
\$rpmtagtbl = array(
EOF

src="$1"
test "$src" = "" && src="$HOME/src/rpm/lib/rpmtag.h"

${AWK:-awk} -f gentagtbl.awk < $src | sort

cat << EOF
);
?>
EOF
