# libgcrypt.m4 - Autoconf macros to detect libgcrypt
# Copyright (C) 2002, 2003, 2004, 2011, 2014 g10 Code GmbH
#
# This file is free software; as a special exception the author gives
# unlimited permission to copy and/or distribute it, with or without
# modifications, as long as this notice is preserved.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY, to the extent permitted by law; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Last-changed: 2014-10-02


dnl AM_PATH_LIBGCRYPT([MINIMUM-VERSION,
dnl                   [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl Test for libgcrypt and define LIBGCRYPT_CFLAGS and LIBGCRYPT_LIBS.
dnl MINIMUM-VERSION is a string with the version number optionalliy prefixed
dnl with the API version to also check the API compatibility. Example:
dnl a MINIMUM-VERSION of 1:1.2.5 won't pass the test unless the installed
dnl version of libgcrypt is at least 1.2.5 *and* the API number is 1.  Using
dnl this feature prevents building against newer versions of libgcrypt
dnl with a changed API.
dnl
dnl If a prefix option is not used, the config script is first
dnl searched in $SYSROOT/bin and then along $PATH.  If the used
dnl config script does not match the host specification the script
dnl is added to the gpg_config_script_warn variable.
dnl
AC_DEFUN([AM_PATH_LIBGCRYPT],
[ AC_REQUIRE([AC_CANONICAL_HOST])
 AC_REQUIRE([PKG_CHECK_EXISTS])
  tmp=ifelse([$1], ,1:1.2.0,$1)
  if echo "$tmp" | grep ':' >/dev/null 2>/dev/null ; then
     req_libgcrypt_api=`echo "$tmp"     | sed 's/\(.*\):\(.*\)/\1/'`
     min_libgcrypt_version=`echo "$tmp" | sed 's/\(.*\):\(.*\)/\2/'`
  else
     req_libgcrypt_api=0
     min_libgcrypt_version="$tmp"
  fi

  ok=no
  PKG_CHECK_MODULES(LIBGRYCPT, [libgcrypt >= $min_libgcrypt_version], [ok=yes])
  if test $ok = yes; then
    ifelse([$2], , :, [$2])
  else
    LIBGCRYPT_CFLAGS=""
    LIBGCRYPT_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(LIBGCRYPT_CFLAGS)
  AC_SUBST(LIBGCRYPT_LIBS)
])
