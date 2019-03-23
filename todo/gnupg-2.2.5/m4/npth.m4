# npth.m4 - autoconf macro to detect NPTH.
# Copyright (C) 2002, 2003, 2004, 2011 g10 Code GmbH
#
# This file is free software; as a special exception the author gives
# unlimited permission to copy and/or distribute it, with or without
# modifications, as long as this notice is preserved.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

dnl AM_PATH_NPTH([MINIMUM-VERSION,
dnl               [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test for libnpth and define NPTH_CFLAGS and NPTH_LIBS.
dnl
AC_DEFUN([AM_PATH_NPTH],
[ dnl
  tmp=ifelse([$1], ,1:0.91,$1)
  if echo "$tmp" | grep ':' >/dev/null 2>/dev/null ; then
     req_npth_api=`echo "$tmp"     | sed 's/\(.*\):\(.*\)/\1/'`
     min_npth_version=`echo "$tmp" | sed 's/\(.*\):\(.*\)/\2/'`
  else
     req_npth_api=1
     min_npth_version="$tmp"
  fi

  ok=no
  AC_CHECK_HEADER(npth.h,[
    AC_CHECK_LIB(npth, npth_init, [ok=yes])
  ])
  AC_MSG_CHECKING(for NPTH)
  if test $ok = yes; then
    AC_MSG_RESULT([yes])
  else
    AC_MSG_RESULT(no)
  fi
  if test $ok = yes; then
    NPTH_CFLAGS=
    NPTH_LIBS=-lnpth
    ifelse([$2], , :, [$2])
  else
    NPTH_CFLAGS=""
    NPTH_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(NPTH_CFLAGS)
  AC_SUBST(NPTH_LIBS)
])
