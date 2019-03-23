dnl Autoconf macros for NTBTLS
dnl Copyright (C) 2002, 2004, 2011 Free Software Foundation, Inc.
dnl
dnl This file is free software; as a special exception the author gives
dnl unlimited permission to copy and/or distribute it, with or without
dnl modifications, as long as this notice is preserved.
dnl
dnl This file is distributed in the hope that it will be useful, but
dnl WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
dnl implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


dnl AM_PATH_NTBTLS([MINIMUM-VERSION,
dnl                   [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl
dnl Test for NTBTLS and define NTBTLS_CFLAGS and NTBTLS_LIBS.
dnl MINIMUM-VERSION is a string with the version number optionalliy prefixed
dnl with the API version to also check the API compatibility. Example:
dnl a MINIMUM-VERSION of 1:1.2.5 won't pass the test unless the installed
dnl version of ntbtls is at least 1.2.5 *and* the API number is 1.  Using
dnl this feature prevents building against newer versions of ntbtls
dnl with a changed API.
dnl
AC_DEFUN([AM_PATH_NTBTLS],
[ AC_REQUIRE([AC_CANONICAL_HOST])
 AC_REQUIRE([PKG_CHECK_EXISTS])
  tmp=ifelse([$1], ,1:1.0.0,$1)
  if echo "$tmp" | grep ':' >/dev/null 2>/dev/null ; then
     req_ntbtls_api=`echo "$tmp"     | sed 's/\(.*\):\(.*\)/\1/'`
     min_ntbtls_version=`echo "$tmp" | sed 's/\(.*\):\(.*\)/\2/'`
  else
     req_ntbtls_api=0
     min_ntbtls_version="$tmp"
  fi

  ok=no
  PKG_CHECK_MODULES(KSBA, [ntbtls >= $min_ntbtls_version], [ok=yes])
  if test $ok = yes; then
    ifelse([$2], , :, [$2])
  else
    NTBTLS_CFLAGS=""
    NTBTLS_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(NTBTLS_CFLAGS)
  AC_SUBST(NTBTLS_LIBS)
])
