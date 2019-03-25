<?php

error_reporting(E_ALL & ~E_WARNING);
ini_set("display_errors", 1);
date_default_timezone_set('UTC');

?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
          "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xml:lang="en" lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Math libraries for Atari</title>
<meta name="keywords" content="ORCS, CAT, GC, PBEM, PBM, GC-Ork, GCORK, ARAnyM, UDO, EmuTOS, GCC" />
<link rel="stylesheet" type="text/css" href="home.css" />
</head>

<?php
$imagedir = 'images/';
$manhref = 'http://man7.org/linux/man-pages/man3/';

$fdlibm = array(
	'trig_header' => array('header' => 'Trigonometric functions.'),
	'acos' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'acos', 'description' => 'Arc cosine of X.'),
	'asin' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'asin', 'description' => 'Arc sine of X.'),
	'atan' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'atan', 'description' => 'Arc tangent of X.'),
	'atan2' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'atan2', 'description' => 'Arc tangent of Y/X.'),
	'cos' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'cos', 'description' => 'Cosine of X.'),
	'sin' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'sin', 'description' => 'Sine of X.'),
	'tan' => array('d' => 2, 'f' => 0, 'l' => 0, 'man' => 'tan', 'description' => 'Tangent of X.'),
	'sincos' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'sincos', 'description' => 'Cosine and sine of X.'),

	'hyp_header' => array('header' => 'Hyperbolic functions.'),
	'cosh' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'cosh', 'description' => 'Hyperbolic cosine of X.'),
	'sinh' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'sinh', 'description' => 'Hyperbolic sine of X.'),
	'tanh' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'tanh', 'description' => 'Hyperbolic tangent of X.'),
	'acosh' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'acosh', 'description' => 'Hyperbolic arc cosine of X.'),
	'asinh' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'asinh', 'description' => 'Hyperbolic arc sine of X.'),
	'atanh' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'atanh', 'description' => 'Hyperbolic arc tangent of X.'),

	'log_header' => array('header' => 'Exponential and logarithmic functions.'),
	'exp' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'exp', 'description' => 'Exponential function of X.'),
	'frexp' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'frexp', 'description' => 'Break VALUE into a normalized fraction and an integral power of 2.'),
	'ldexp' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'ldexp', 'description' => 'X times (two to the EXP power).'),
	'log' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'log', 'description' => 'Natural logarithm of X.'),
	'log10' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'log10', 'description' => 'Base-ten logarithm of X.'),
	'modf' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'modf', 'description' => 'Break VALUE into integral and fractional parts.'),
	'exp10' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'exp10', 'description' => 'Compute exponent to base ten.', 'comments' => 'Same as pow10()'),
	'expm1' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'expm1', 'description' => 'Return exp(X) - 1.'),
	'log1p' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'log1p', 'description' => 'Return log(1 + X).'),
	'logb' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'logb', 'description' => 'Return the base 2 signed integral exponent of X.'),
	'exp2' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'exp2', 'description' => 'Compute base-2 exponential of X.'),
	'log2' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'log2', 'description' => 'Compute base-2 logarithm of X.'),

	'pow_header' => array('header' => 'Power functions.'),
	'pow' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'pow', 'description' => 'Return X to the Y power.'),
	'pow10' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'pow10', 'description' => 'Return the value of 10 raised to the power x', 'comments' => 'Same as exp10()'),
	'sqrt' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'sqrt', 'description' => 'Return the square root of X.'),
	'hypot' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'hypot', 'description' => 'Return sqrt(X*X + Y*Y).'),
	'cbrt' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'cbrt', 'description' => 'Return the cube root of X.'),

	'round_header' => array('header' => 'Nearest integer, absolute value, and remainder functions.'),
	'ceil' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'ceil', 'description' => 'Smallest integral value not less than X.'),
	'fabs' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'fabs', 'description' => 'Absolute value of X.'),
	'floor' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'floor', 'description' => 'Largest integer not greater than X.'),
	'fmod' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'fmod', 'description' => 'Floating-point modulo remainder of X/Y.'),
	'finite' => array('d' => 1, 'f' => 1, 'l' => 1, 'man' => 'finite', 'description' => 'Return nonzero if VALUE is finite and not NaN.', 'comments' => 'implemented in mintlib'),
	'drem' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'drem', 'description' => 'Return the remainder of X/Y.', 'comments' => 'Obsolete synonym for remainder'),
	'significand' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'significand', 'description' => 'Return the fractional part of X after dividing out `ilogb (X)&apos;.'),
	'copysign' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'copysign', 'description' => 'Return X with its signed changed to Y&apos;s.'),
	'nan' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'nan', 'description' => 'Return representation of qNaN for double type.'),

	'bessel_header' => array('header' => 'Bessel functions.'),
	'j0' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'j0', 'description' => 'Bessel function of the first kind of order 0'),
	'j1' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'j1', 'description' => 'Bessel function of the first kind of order 1'),
	'jn' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'jn', 'description' => 'Bessel function of the first kind of order n'),
	'y0' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'y0', 'description' => 'Bessel function of the second kind of order 0'),
	'y1' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'y1', 'description' => 'Bessel function of the second kind of order 1'),
	'yn' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'yn', 'description' => 'Bessel function of the second kind of order n'),

	'gamma_header' => array('header' => 'Error and gamma functions.'),
	'erf' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'erf', 'description' => 'error function'),
	'erfc' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'erfc', 'description' => 'complementary error function'),
	'lgamma' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'lgamma', 'description' => 'log gamma function'),
	'tgamma' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'tgamma', 'description' => 'true gamma function'),
	'gamma' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'gamma', 'description' => '(logarithm of the) gamma function'),
	'lgamma_r' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'lgamma_r', 'description' => 'reentrant version of lgamma'),

	'iso_header' => array('header' => 'ISO C99 rounding functions.'),
	'rint' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'rint', 'description' => 'Return the integer nearest X in the direction of the prevailing rounding mode.'),
	'nextafter' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'nextafter', 'description' => 'Return X + epsilon if X &lt; Y, X - epsilon if X > Y.'),
	'nexttoward' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'nexttoward', 'description' => 'Return X + epsilon if X &lt; Y, X - epsilon if X > Y.'),
	'nextdown' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'nextdown', 'description' => 'return next floating-point number toward negative infinity'),
	'nextup' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'nextup', 'description' => 'return next floating-point number toward positive infinity'),
	'remainder' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'remainer', 'description' => 'Return the remainder of integer divison X / Y with infinite precision.'),
	'scalb' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'scalb', 'description' => 'Return X times (2 to the Nth power).'),
	'scalbn' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'scalbn', 'description' => 'Return X times (2 to the Nth power).'),
	'ilogb' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'ilogb', 'description' => 'Return the binary exponent of X, which must be nonzero.'),
	'llogb' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'llogb', 'description' => 'Like ilogb, but returning long int.'),
	'scalbln' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'scalbln', 'description' => 'Return X times (2 to the Nth power).'),
	'nearbyint' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'nearbyint', 'description' => 'Round X to integral value in floating-point format using current rounding direction, but do not raise inexact exception.', 'comments' => 'Same as rint'),
	'round' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'round', 'description' => 'Round X to nearest integral value, rounding halfway cases away from zero.'),
	'trunc' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'trunc', 'description' => 'Round X to the integral value in floating-point format nearest but not larger in magnitude.'),
	'remquo' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'remquo', 'description' => 'Compute remainder of X and Y and put in *QUO a value with sign of x/y
and magnitude congruent `mod 2^n&apos; to the magnitude of the integral
quotient x/y, with n &gt;= 3.'),

	'conv_header' => array('header' => 'Conversion functions.'),
	'lrint' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'lrint', 'description' => 'Round X to nearest integral value according to current rounding direction.'),
	'llrint' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'llrint', 'description' => 'Like lrint, but returning long long int.'),
	'lround' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'lround', 'description' => 'Round X to nearest integral value, rounding halfway cases away from zero.'),
	'llround' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'llround', 'description' => 'Like lround, but returning long long int.'),
	'fdim' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'fdim', 'description' => 'Return positive difference between X and Y.'),
	'fmax' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'fmax', 'description' => 'Return maximum numeric value from X and Y.'),
	'fmin' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'fmin', 'description' => 'Return minimum numeric value from X and Y.'),
	'fma' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'fma', 'description' => 'Multiply-add function computed as a ternary operation.'),
	'roundeven' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'roundeven', 'description' => 'Round X to nearest integer value, rounding halfway cases to even.'),
	'fromfp' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'fromfp', 'description' => 'Round X to nearest signed integer value, not raising inexact, with control of rounding direction and width of result.'),
	'ufromfp' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'ufromfp', 'description' => 'Round X to nearest unsigned integer value, not raising inexact, with control of rounding direction and width of result.'),
	'fromfpx' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'fromfpx', 'description' => 'Round X to nearest signed integer value, raising inexact for
   non-integers, with control of rounding direction and width of
   result.'),
	'ufromfpx' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'ufromfpx', 'description' => 'Round X to nearest unsigned integer value, raising inexact for
   non-integers, with control of rounding direction and width of
   result.'),

	'class_header' => array('header' => 'Classification functions.'),
	'fpclassify' => array('d' => 1, 'f' => 0, 'l' => 0, 'man' => 'fpclassify', 'description' => 'Return number of classification appropriate for X.'),
	'signbit' => array('d' => 1, 'f' => 1, 'l' => 1, 'man' => 'signbit', 'description' => 'Return nonzero value if sign of X is negative.', 'comments' => 'implemented in mintlib'),
	'isfinite' => array('d' => 1, 'f' => 1, 'l' => 1, 'man' => 'isfinite', 'description' => 'Return nonzero value if X is not +-Inf or NaN.', 'comments' => 'implemented in mintlib'),
	'isnormal' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'isnormal', 'description' => 'Return nonzero value if X is neither zero, subnormal, Inf, nor NaN.'),
	'isnan' => array('d' => 1, 'f' => 1, 'l' => 1, 'man' => 'isnan', 'description' => 'Return nonzero if VALUE is not a number.', 'comments' => 'implemented in mintlib'),
	'isinf' => array('d' => 1, 'f' => 1, 'l' => 1, 'man' => 'isinf', 'description' => 'Return 0 if VALUE is finite or NaN, +1 if it is +Infinity, -1 if it is -Infinity.', 'comments' => 'implemented in mintlib'),
	'issignaling' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'issignaling', 'description' => 'Return nonzero value if X is a signaling NaN.'),
	'issubnormal' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'issubnormal', 'description' => 'Return nonzero value if X is subnormal.'),
	'iszero' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'iszero', 'description' => 'Return nonzero value if X is zero.'),
	'iscanonical' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'iscanonical', 'description' => 'Return nonzero value if X is canonical.'),

	'order_header' => array('header' => 'relational tests without exception for NaN.'),
	'isgreater' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'isgreater', 'description' => 'determines (x) &gt; (y) without an exception if x or y is NaN. '),
	'isgreaterequal' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'isgreatterequal', 'description' => 'determines (x) &gt;= (y) without an exception if x or y is NaN. '),
	'isless' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'isless', 'description' => 'determines (x) &lt; (y) without an exception if x or y is NaN. '),
	'islessequal' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'islesseqal', 'description' => 'determines (x) &lt;= (y) without an exception if x or y is NaN. '),
	'islessgreater' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'islessgreater', 'description' => 'determines (x) &lt; (y) || (x) &gt; (y) without an exception if x or y is NaN. This macro is not equivalent to x != y because that expression is true if x or y is NaN.'),
	'isunordered' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'isunordered', 'description' => 'determines whether its arguments are unordered, that is, whether at least one of the arguments is a NaN.'),
	'iseqsig' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'iseqsig', 'description' => 'Return X == Y but raising "invalid" and setting errno if X or Y is a NaN.'),

	'misc_header' => array('header' => 'Miscellaneous functions.'),
	'fmaxmag' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'fmaxmag', 'description' => 'Return value with maximum magnitude.'),
	'fminmag' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'fminmag', 'description' => 'Return value with minimum magnitude.'),
	'totalorder' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'totalorder', 'description' => 'Total order operation.'),
	'totalordermag' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'totalordermag', 'description' => 'Total order operation on absolute values.'),
	'canonicalize' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'canonicalize', 'description' => 'Canonicalize floating-point representation.'),
	'getpayload' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'getpayload', 'description' => 'Get NaN payload.'),
	'setpayload' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'setpayload', 'description' => 'Set quiet NaN payload.'),
	'setpayloadsig' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'setpayloadsig', 'description' => 'Set signaling NaN payload.'),
	'matherr' => array('a' => 1, 'man' => 'matherr', 'description' => 'SVID math library exception handling', 'comments' => 'Deprecated in favour of math_error'),
	'math_error' => array('a' => 0, 'man' => 'math_error', 'description' => 'detecting errors from mathematical functions'),

	'except_header' => array('header' => 'Exception handling.'),
	'feclearexcept' => array('a' => 0, 'man' => 'feclearexcept', 'description' => 'Clear the supported exceptions represented by EXCEPTS.'),
	'fegetexceptflag' => array('a' => 0, 'man' => 'fegetexceptflag', 'description' => 'Store implementation-defined representation of the exception flags
   indicated by EXCEPTS in the object pointed to by FLAGP.'),
	'feraiseexcept' => array('a' => 0, 'man' => 'feraiseexcept', 'description' => 'Raise the supported exceptions represented by EXCEPTS.'),
	'fesetexcept' => array('a' => 0, 'man' => 'fesetexcept', 'description' => 'Set the supported exception flags represented by EXCEPTS, without
   causing enabled traps to be taken.'),
	'fetestexcept' => array('a' => 0, 'man' => 'fetestexcept', 'description' => 'Determine which of subset of the exceptions specified by EXCEPTS are
   currently set.'),
	'fetestexceptflag' => array('a' => 0, 'man' => 'fetestexceptflagt', 'description' => 'Determine which of subset of the exceptions specified by EXCEPTS
   are set in *FLAGP.'),
	'feenableexcept' => array('a' => 0, 'man' => 'feenableexcept', 'description' => 'Enable individual exceptions.  Will not enable more exceptions than
   EXCEPTS specifies.  Returns the previous enabled exceptions if all
   exceptions are successfully set, otherwise returns -1.'),
	'fedisableexcept' => array('a' => 0, 'man' => 'fedisableexcept', 'description' => 'Disable individual exceptions.  Will not disable more exceptions than
   EXCEPTS specifies.  Returns the previous enabled exceptions if all
   exceptions are successfully disabled, otherwise returns -1.'),
	'fegetexcept' => array('a' => 0, 'man' => 'fegetexcept', 'description' => 'Return enabled exceptions.'),

	'rounding_header' => array('header' => 'Rounding control.'),
	'fegetround' => array('a' => 0, 'man' => 'fegetround', 'description' => 'Get current rounding direction.'),
	'fesetround' => array('a' => 0, 'man' => 'fesetround', 'description' => 'Establish the rounding direction represented by ROUND.'),

	'floating_header' => array('header' => 'Floating-point environment.'),
	'fegetenv' => array('a' => 0, 'man' => 'fegetenv', 'description' => 'Store the current floating-point environment in the object pointed
   to by ENVP.'),
	'feholdexcept' => array('a' => 0, 'man' => 'feholdexcept', 'description' => 'Save the current environment in the object pointed to by ENVP, clear
   exception flags and install a non-stop mode (if available) for all
   exceptions.'),
	'fesetenv' => array('a' => 0, 'man' => 'fesetenv', 'description' => 'Establish the floating-point environment represented by the object
   pointed to by ENVP.'),
	'feupdateenv' => array('a' => 0, 'man' => 'feupdateenv', 'description' => 'Save current exceptions in temporary storage, install environment
   represented by object pointed to by ENVP and raise exceptions
   according to saved exceptions.'),

	'control_header' => array('header' => 'Control modes.'),
	'fegetmode' => array('a' => 0, 'man' => 'fegetmode', 'description' => 'Store the current floating-point control modes in the object
   pointed to by MODEP.'),
	'fesetmode' => array('a' => 0, 'man' => 'fesetmode', 'description' => 'Establish the floating-point control modes represented by the
   object pointed to by MODEP.'),

	'complex_trig_header' => array('header' => 'Complex Trigonometric functions.'),
	'cacos' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cacos', 'description' => 'Arc cosine of X.'),
	'casin' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'casin', 'description' => 'Arc sine of X.'),
	'catan' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'catan', 'description' => 'Arc tangent of X.'),
	'ccos' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'ccos', 'description' => 'Cosine of X.'),
	'csin' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'csin', 'description' => 'Sine of X.'),
	'ctan' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'ctan', 'description' => 'Tangent of X.'),

	'complex_hyp_header' => array('header' => 'Complex Hyperbolic functions.'),
	'ccosh' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'ccosh', 'description' => 'Hyperbolic cosine of X.'),
	'csinh' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'csinh', 'description' => 'Hyperbolic sine of X.'),
	'ctanh' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'ctanh', 'description' => 'Hyperbolic tangent of X.'),
	'cacosh' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cacosh', 'description' => 'Hyperbolic arc cosine of X.'),
	'casinh' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'casinh', 'description' => 'Hyperbolic arc sine of X.'),
	'catanh' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'catanh', 'description' => 'Hyperbolic arc tangent of X.'),

	'complex_log_header' => array('header' => 'Complex Exponential and logarithmic functions.'),
	'cexp' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cexp', 'description' => 'Exponential function of X.'),
	'clog' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'clog', 'description' => 'Natural logarithm of X.'),
	'clog10' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'clog10', 'description' => 'Base-ten logarithm of X.'),

	'complex_pow_header' => array('header' => 'Complex Power functions.'),
	'cpow' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cpow', 'description' => 'Return X to the Y power.'),
	'csqrt' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'csqrt', 'description' => 'Return the square root of X.'),
	'crcp' => array('d' => 0, 'f' => 0, 'l' => 0, 'description' => 'complex reciprocal of z', 'comments' => 'Non-standard function'),

	'complex_prim_header' => array('header' => 'Absolute value, conjugates, and projection.'),
	'cabs' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cabs', 'description' => 'Absolute value of Z.'),
	'carg' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'carg', 'description' => 'Argument value of Z.'),
	'conj' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'conj', 'description' => 'Complex conjugate of Z.'),
	'cproj' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cproj', 'description' => 'Projection of Z onto the Riemann sphere.'),
	'cimag' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'cimag', 'description' => 'Imaginary part of Z.'),
	'creal' => array('d' => 0, 'f' => 0, 'l' => 0, 'man' => 'creal', 'description' => 'Real part of Z.'),
);


$pml = array(
	'acos' => array('d' => 1, 'f' => 0, 'l' => 0),
	'asin' => array('d' => 1, 'f' => 0, 'l' => 0),
	'atan' => array('d' => 1, 'f' => 0, 'l' => 0),
	'atan2' => array('d' => 1, 'f' => 0, 'l' => 0),
	'cos' => array('d' => 1, 'f' => 0, 'l' => 0),
	'sin' => array('d' => 1, 'f' => 0, 'l' => 0),
	'tan' => array('d' => 1, 'f' => 0, 'l' => 0),
	'sincos' => array('d' => 0, 'f' => 0, 'l' => 0),

	'cosh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'sinh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'tanh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'acosh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'asinh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'atanh' => array('d' => 1, 'f' => 0, 'l' => 0),

	'exp' => array('d' => 1, 'f' => 0, 'l' => 0, 'comments' => 'when using PML, you may get unresolved externals when using the softfloat function,
because ldexp and frexp are not implemented'),
	'frexp' => array('d' => 0, 'f' => 0, 'l' => 0),
	'ldexp' => array('d' => 0, 'f' => 0, 'l' => 0),
	'log' => array('d' => 1, 'f' => 0, 'l' => 0),
	'log10' => array('d' => 1, 'f' => 0, 'l' => 0),
	'modf' => array('d' => 0, 'f' => 0, 'l' => 0),
	'exp10' => array('d' => 1, 'f' => 0, 'l' => 0),
	'expm1' => array('d' => 0, 'f' => 0, 'l' => 0),
	'log1p' => array('d' => 0, 'f' => 0, 'l' => 0),
	'logb' => array('d' => 0, 'f' => 0, 'l' => 0),
	'log1p' => array('d' => 0, 'f' => 0, 'l' => 0),
	'exp2' => array('d' => 0, 'f' => 0, 'l' => 0),
	'log2' => array('d' => 0, 'f' => 0, 'l' => 0),

	'pow' => array('d' => 1, 'f' => 0, 'l' => 0),
	'pow10' => array('d' => 0, 'f' => 0, 'l' => 0),
	'sqrt' => array('d' => 1, 'f' => 0, 'l' => 0, 'comments' => 'when using PML, you may get unresolved externals when using the softfloat function,
because frexp is not implemented'),
	'hypot' => array('d' => 0, 'f' => 0, 'l' => 0),
	'cbrt' => array('d' => 0, 'f' => 0, 'l' => 0),

	'ceil' => array('d' => 1, 'f' => 0, 'l' => 0, 'comments' => 'when using PML, you may get unresolved externals when using the softfloat function,
because modf is not implemented'),
	'fabs' => array('d' => 1, 'f' => 0, 'l' => 0),
	'floor' => array('d' => 1, 'f' => 0, 'l' => 0, 'comments' => 'when using PML, you may get unresolved externals when using the softfloat function,
because modf is not implemented'),
	'fmod' => array('d' => 1, 'f' => 0, 'l' => 0),
	'finite' => array('d' => 0, 'f' => 0, 'l' => 0),
	'drem' => array('d' => 0, 'f' => 0, 'l' => 0),
	'significand' => array('d' => 0, 'f' => 0, 'l' => 0),
	'copysign' => array('d' => 1, 'f' => 0, 'l' => 0),
	'nan' => array('d' => 0, 'f' => 0, 'l' => 0),

	'j0' => array('d' => 0, 'f' => 0, 'l' => 0),
	'j1' => array('d' => 0, 'f' => 0, 'l' => 0),
	'jn' => array('d' => 0, 'f' => 0, 'l' => 0),
	'y0' => array('d' => 0, 'f' => 0, 'l' => 0),
	'y1' => array('d' => 0, 'f' => 0, 'l' => 0),
	'yn' => array('d' => 0, 'f' => 0, 'l' => 0),

	'erf' => array('d' => 0, 'f' => 0, 'l' => 0),
	'erfc' => array('d' => 0, 'f' => 0, 'l' => 0),
	'lgamma' => array('d' => 0, 'f' => 0, 'l' => 0),
	'tgamma' => array('d' => 0, 'f' => 0, 'l' => 0),
	'gamma' => array('d' => 0, 'f' => 0, 'l' => 0),
	'lgamma_r' => array('d' => 0, 'f' => 0, 'l' => 0),

	'rint' => array('d' => 1, 'f' => 0, 'l' => 0, 'comments' => 'when using PML, you may get unresolved externals when using the softfloat function,
because modf is not implemented'),
	'nextafter' => array('d' => 0, 'f' => 0, 'l' => 0),
	'nexttoward' => array('d' => 0, 'f' => 0, 'l' => 0),
	'nextdown' => array('d' => 0, 'f' => 0, 'l' => 0),
	'nextup' => array('d' => 0, 'f' => 0, 'l' => 0),
	'remainder' => array('d' => 0, 'f' => 0, 'l' => 0),
	'scalb' => array('d' => 0, 'f' => 0, 'l' => 0),
	'scalbn' => array('d' => 0, 'f' => 0, 'l' => 0),
	'ilogb' => array('d' => 0, 'f' => 0, 'l' => 0),
	'llogb' => array('d' => 0, 'f' => 0, 'l' => 0),
	'scalbln' => array('d' => 0, 'f' => 0, 'l' => 0),
	'nearbyint' => array('d' => 0, 'f' => 0, 'l' => 0),
	'round' => array('d' => 1, 'f' => 0, 'l' => 0),
	'trunc' => array('d' => 0, 'f' => 0, 'l' => 0),
	'remquo' => array('d' => 0, 'f' => 0, 'l' => 0),

	'lrint' => array('d' => 0, 'f' => 0, 'l' => 0),
	'llrint' => array('d' => 0, 'f' => 0, 'l' => 0),
	'lround' => array('d' => 0, 'f' => 0, 'l' => 0),
	'llround' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fdim' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fmax' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fmin' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fma' => array('d' => 0, 'f' => 0, 'l' => 0),
	'roundeven' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fromfp' => array('d' => 0, 'f' => 0, 'l' => 0),
	'ufromfp' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fromfpx' => array('d' => 0, 'f' => 0, 'l' => 0),
	'ufromfpx' => array('d' => 0, 'f' => 0, 'l' => 0),

	'fpclassify' => array('d' => 0, 'f' => 0, 'l' => 0),
	'signbit' => array('d' => 1, 'f' => 1, 'l' => 1),
	'isfinite' => array('d' => 1, 'f' => 1, 'l' => 1),
	'isnormal' => array('d' => 0, 'f' => 0, 'l' => 0),
	'isnan' => array('d' => 1, 'f' => 1, 'l' => 1),
	'isinf' => array('d' => 1, 'f' => 1, 'l' => 1),
	'issignaling' => array('d' => 0, 'f' => 0, 'l' => 0),
	'iszero' => array('d' => 0, 'f' => 0, 'l' => 0),
	'issubnormal' => array('d' => 0, 'f' => 0, 'l' => 0),
	'iscanonical' => array('d' => 0, 'f' => 0, 'l' => 0),

	'isgreater' => array('d' => 0, 'f' => 0, 'l' => 0),
	'isgreaterequal' => array('d' => 0, 'f' => 0, 'l' => 0),
	'isless' => array('d' => 0, 'f' => 0, 'l' => 0),
	'islessequal' => array('d' => 0, 'f' => 0, 'l' => 0),
	'islessgreater' => array('d' => 0, 'f' => 0, 'l' => 0),
	'isunordered' => array('d' => 0, 'f' => 0, 'l' => 0),
	'iseqsig' => array('d' => 0, 'f' => 0, 'l' => 0),

	'fmaxmag' => array('d' => 0, 'f' => 0, 'l' => 0),
	'fminmag' => array('d' => 0, 'f' => 0, 'l' => 0),
	'totalorder' => array('d' => 0, 'f' => 0, 'l' => 0),
	'totalordermag' => array('d' => 0, 'f' => 0, 'l' => 0),
	'canonicalize' => array('d' => 0, 'f' => 0, 'l' => 0),
	'getpayload' => array('d' => 0, 'f' => 0, 'l' => 0),
	'setpayload' => array('d' => 0, 'f' => 0, 'l' => 0),
	'setpayloadsig' => array('d' => 0, 'f' => 0, 'l' => 0),
	'matherr' => array('a' => 1),
	'math_error' => array('a' => 0),

	'feclearexcept' => array('a' => 0),
	'fegetexceptflag' => array('a' => 0),
	'feraiseexcept' => array('a' => 0),
	'fesetexcept' => array('a' => 0),
	'fetestexcept' => array('a' => 0),
	'fetestexceptflag' => array('a' => 0),
	'feenableexcept' => array('a' => 0),
	'fedisableexcept' => array('a' => 0),
	'fegetexcept' => array('a' => 0),
	'fegetround' => array('a' => 0),
	'fesetround' => array('a' => 0),
	'fegetenv' => array('a' => 0),
	'feholdexcept' => array('a' => 0),
	'fesetenv' => array('a' => 0),
	'feupdateenv' => array('a' => 0),
	'fegetmode' => array('a' => 0),
	'fesetmode' => array('a' => 0),

	'cacos' => array('d' => 1, 'f' => 0, 'l' => 0),
	'casin' => array('d' => 1, 'f' => 0, 'l' => 0),
	'catan' => array('d' => 1, 'f' => 0, 'l' => 0),
	'ccos' => array('d' => 1, 'f' => 0, 'l' => 0),
	'csin' => array('d' => 1, 'f' => 0, 'l' => 0),
	'ctan' => array('d' => 1, 'f' => 0, 'l' => 0),

	'ccosh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'csinh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'ctanh' => array('d' => 1, 'f' => 0, 'l' => 0),
	'cacosh' => array('d' => 0, 'f' => 0, 'l' => 0),
	'casinh' => array('d' => 0, 'f' => 0, 'l' => 0),
	'catanh' => array('d' => 0, 'f' => 0, 'l' => 0),

	'cexp' => array('d' => 1, 'f' => 0, 'l' => 0),
	'clog' => array('d' => 1, 'f' => 0, 'l' => 0),
	'clog10' => array('d' => 0, 'f' => 0, 'l' => 0),

	'cpow' => array('d' => 0, 'f' => 0, 'l' => 0),
	'csqrt' => array('d' => 1, 'f' => 0, 'l' => 0),
	'crcp' => array('d' => 1, 'f' => 0, 'l' => 0),

	'cabs' => array('d' => 1, 'f' => 0, 'l' => 0),
	'carg' => array('d' => 0, 'f' => 0, 'l' => 0),
	'conj' => array('d' => 0, 'f' => 0, 'l' => 0),
	'cproj' => array('d' => 0, 'f' => 0, 'l' => 0),
	'cimag' => array('d' => 0, 'f' => 0, 'l' => 0),
	'creal' => array('d' => 0, 'f' => 0, 'l' => 0),
);
?>

<body>

<div>

<h1>Math libraries for Atari</h1>

Currently, there are two free math libraries available for Atari ST, PML (<b>P</b>ortable <b>M</b>ath <b>L</b>ibrary),
and fdlibm. The following table should give a brief overview over which functions are available.

<p>&nbsp;</p>

<table border="1" cellpadding="2" cellspacing="0">
<tr>
<th></th><th colspan="3">PML</th><th colspan="3">fdlibm</th>
<th colspan="2"></th>
</tr>
<tr>
<th>Name</th>
<th>Double</th><th>Float</th><th>Long Double</th>
<th>Double</th><th>Float</th><th>Long Double</th>
<th>Description</th>
<th>Comments</th>
</tr>

<?php

function link_yesno($yes)
{
	global $imagedir;
	echo '<img width="32" height="32" src="' . $imagedir;
	echo $yes ? 'yes.png' : 'no.png';
	echo '" title="';
	echo $yes ? 'yes' : 'no';
	echo '" alt="';
	echo $yes ? 'yes' : 'no';
	echo '"></img>';
}

foreach ($fdlibm as $name => $func)
{
	echo '<tr>';
	$comments = '';
	$description = '';
	if (isset($func['header']))
	{
		echo '<td colspan="9">' . $func['header'] . '</td>';
	} else
	{
		echo '<td>';
		if (isset($func['man']))
		{
			echo '<a href="' . $manhref . $func['man'] . '.3.html">' . $name . '</a>';
		} else
		{
			echo $name;
		}
		echo '</td>';
		$func = $pml[$name];
		if (isset($func['a']))
		{
			echo '<td align="center" colspan="3">'; link_yesno($func['a']); echo '</td>';
		} else
		{
			echo '<td align="center">'; link_yesno($func['d']); echo '</td>';
			echo '<td align="center">'; link_yesno($func['f']); echo '</td>';
			echo '<td align="center">'; link_yesno($func['l']); echo '</td>';
		}
		if (isset($func['description'])) $description .= $func['description'];
		if (isset($func['comments'])) $comments .= $func['comments'];
		$func = $fdlibm[$name];
		if (isset($func['a']))
		{
			echo '<td align="center" colspan="3">'; link_yesno($func['a']); echo '</td>';
		} else
		{
			echo '<td align="center">'; link_yesno($func['d']); echo '</td>';
			echo '<td align="center">'; link_yesno($func['f']); echo '</td>';
			echo '<td align="center">'; link_yesno($func['l']); echo '</td>';
		}
		if (isset($func['description'])) $description .= $func['description'];
		if (isset($func['comments'])) $comments .= $func['comments'];
		echo '<td>' . $description . '</td>';
		echo '<td>' . $comments . '</td>';
	}
	echo "</tr>\n";
}

?>

</table>

<br/>

</div>

<!--
<div style="text-align:center">
<p>
<a href="https://validator.w3.org/check?uri=referer"><img
        src="images/valid-xhtml11.png" height="31" width="88"
        alt="Valid XHTML 1.1!" /></a>
</p>
<br/>
</div>
-->

<div style="text-align:center">
<p>
<a href="index.html"> <img src="images/home1.png" width="180" height="60" style="border:0" alt="Home" /></a>
</p>
</div>

</body>
</html>
