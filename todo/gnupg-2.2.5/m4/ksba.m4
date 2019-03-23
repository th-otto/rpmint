# ksba.m4 - autoconf macro to detect ksba
#       Copyright (C) 2002 g10 Code GmbH
#
# This file is free software; as a special exception the author gives
# unlimited permission to copy and/or distribute it, with or without
# modifications, as long as this notice is preserved.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


dnl AM_PATH_KSBA([MINIMUM-VERSION,
dnl              [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test for libksba and define KSBA_CFLAGS and KSBA_LIBS
dnl MINIMUM-VERSION is a string with the version number optionalliy prefixed
dnl with the API version to also check the API compatibility. Example:
dnl a MINIMUM-VERSION of 1:1.0.7 won't pass the test unless the installed
dnl version of libksba is at least 1.0.7 *and* the API number is 1.  Using
dnl this feature prevents building against newer versions of libksba
dnl with a changed API.
dnl
AC_DEFUN([AM_PATH_KSBA],
[AC_REQUIRE([AC_CANONICAL_HOST])
 AC_REQUIRE([PKG_CHECK_EXISTS])
  tmp=ifelse([$1], ,1:1.0.0,$1)
  if echo "$tmp" | grep ':' >/dev/null 2>/dev/null ; then
     req_ksba_api=`echo "$tmp"     | sed 's/\(.*\):\(.*\)/\1/'`
     min_ksba_version=`echo "$tmp" | sed 's/\(.*\):\(.*\)/\2/'`
  else
     req_ksba_api=0
     min_ksba_version="$tmp"
  fi

  ok=no
  PKG_CHECK_MODULES(KSBA, [libksba >= $min_ksba_version], [ok=yes])
  if test $ok = yes; then
    ifelse([$2], , :, [$2])
  else
    KSBA_CFLAGS=""
    KSBA_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(KSBA_CFLAGS)
  AC_SUBST(KSBA_LIBS)
])
