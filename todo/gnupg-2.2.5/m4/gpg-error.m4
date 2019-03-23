# gpg-error.m4 - autoconf macro to detect libgpg-error.
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


dnl AM_PATH_GPG_ERROR([MINIMUM-VERSION,
dnl                   [ACTION-IF-FOUND [, ACTION-IF-NOT-FOUND ]]])
dnl
dnl Test for libgpg-error and define GPG_ERROR_CFLAGS, GPG_ERROR_LIBS,
dnl GPG_ERROR_MT_CFLAGS, and GPG_ERROR_MT_LIBS.  The _MT_ variants are
dnl used for programs requireing real multi thread support.
dnl
dnl If a prefix option is not used, the config script is first
dnl searched in $SYSROOT/bin and then along $PATH.  If the used
dnl config script does not match the host specification the script
dnl is added to the gpg_config_script_warn variable.
dnl
AC_DEFUN([AM_PATH_GPG_ERROR],
[ AC_REQUIRE([AC_CANONICAL_HOST])
  AC_REQUIRE([PKG_CHECK_EXISTS])
  min_gpg_error_version=ifelse([$1], ,0.0,$1)
  ok=no
  PKG_CHECK_MODULES(GPG_ERROR, [libgpg-error >= $min_gpg_error_version], [ok=yes])
  if test $ok = yes; then
    GPG_ERROR_MT_CFLAGS="$GPG_ERROR_CFLAGS"
    GPG_ERROR_MT_LIBS="$GPG_ERROR_LIBS"
    AC_CHECK_LIB(pthread, pthread_create, GPG_ERROR_MT_LIBS="$GPG_MT_ERROR_LIBS -lpthread")
    ifelse([$2], , :, [$2])
  else
    GPG_ERROR_CFLAGS=""
    GPG_ERROR_LIBS=""
    GPG_ERROR_MT_CFLAGS=""
    GPG_ERROR_MT_LIBS=""
    ifelse([$3], , :, [$3])
  fi
  AC_SUBST(GPG_ERROR_CFLAGS)
  AC_SUBST(GPG_ERROR_LIBS)
  AC_SUBST(GPG_ERROR_MT_CFLAGS)
  AC_SUBST(GPG_ERROR_MT_LIBS)
])
