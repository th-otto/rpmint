dnl Autoconf macros for libassuan
dnl       Copyright (C) 2002, 2003 Free Software Foundation, Inc.
dnl
dnl This file is free software; as a special exception the author gives
dnl unlimited permission to copy and/or distribute it, with or without
dnl modifications, as long as this notice is preserved.
dnl
dnl This file is distributed in the hope that it will be useful, but
dnl WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
dnl implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

dnl
dnl Common code used for libassuan detection [internal]
dnl Returns ok set to yes or no.
dnl
AC_DEFUN([_AM_PATH_LIBASSUAN_COMMON],
[
  AC_REQUIRE([PKG_CHECK_EXISTS])
  tmp=ifelse([$1], ,1:0.9.2,$1)
  if echo "$tmp" | grep ':' >/dev/null 2>/dev/null ; then
    req_libassuan_api=`echo "$tmp"     | sed 's/\(.*\):\(.*\)/\1/'`
    min_libassuan_version=`echo "$tmp" | sed 's/\(.*\):\(.*\)/\2/'`
  else
    req_libassuan_api=0
    min_libassuan_version="$tmp"
  fi

  ok=no
  PKG_CHECK_MODULES(LIBASSUAN, [libassuan >= $min_libassuan_version], [ok=yes])
])

dnl AM_CHECK_LIBASSUAN([MINIMUM-VERSION,
dnl                    [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test whether libassuan has at least MINIMUM-VERSION. This is
dnl used to test for features only available in newer versions.
dnl
AC_DEFUN([AM_CHECK_LIBASSUAN],
[ _AM_PATH_LIBASSUAN_COMMON($1)
  if test $ok = yes; then
    ifelse([$2], , :, [$2])
  else
    ifelse([$3], , :, [$3])
  fi
])




dnl AM_PATH_LIBASSUAN([MINIMUM-VERSION,
dnl                   [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test for libassuan and define LIBASSUAN_CFLAGS and LIBASSUAN_LIBS
dnl
AC_DEFUN([AM_PATH_LIBASSUAN],
[ _AM_PATH_LIBASSUAN_COMMON($1)
  if test $ok = yes; then
    ifelse([$2], , :, [$2])
  else
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(LIBASSUAN_CFLAGS)
  AC_SUBST(LIBASSUAN_LIBS)
])


dnl AM_PATH_LIBASSUAN_PTH([MINIMUM-VERSION,
dnl                      [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test for libassuan and define LIBASSUAN_PTH_CFLAGS and LIBASSUAN_PTH_LIBS
dnl
AC_DEFUN([AM_PATH_LIBASSUAN_PTH],
[ _AM_PATH_LIBASSUAN_COMMON($1,pth)
  if test $ok = yes; then
    LIBASSUAN_PTH_CFLAGS="$LIBASSUAN_CFLAGS"
    LIBASSUAN_PTH_LIBS="$LIBASSUAN_LIBS"
    ifelse([$2], , :, [$2])
  else
    LIBASSUAN_PTH_CFLAGS=""
    LIBASSUAN_PTH_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(LIBASSUAN_PTH_CFLAGS)
  AC_SUBST(LIBASSUAN_PTH_LIBS)
])


dnl AM_PATH_LIBASSUAN_PTHREAD([MINIMUM-VERSION,
dnl                           [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test for libassuan and define LIBASSUAN_PTHREAD_CFLAGS 
dnl                           and LIBASSUAN_PTHREAD_LIBS
dnl
AC_DEFUN([AM_PATH_LIBASSUAN_PTHREAD],
[ _AM_PATH_LIBASSUAN_COMMON($1,pthread)
  if test $ok = yes; then
    LIBASSUAN_PTHREAD_CFLAGS="$LIBASSUAN_CFLAGS"
    LIBASSUAN_PTHREAD_LIBS="$LIBASSUAN_LIBS"
    ifelse([$2], , :, [$2])
  else
    LIBASSUAN_PTHREAD_CFLAGS=""
    LIBASSUAN_PTHREAD_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(LIBASSUAN_PTHREAD_CFLAGS)
  AC_SUBST(LIBASSUAN_PTHREAD_LIBS)
])

