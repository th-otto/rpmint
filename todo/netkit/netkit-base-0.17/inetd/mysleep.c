#include <sys/types.h>
#include <sys/time.h>  /* posix location for select */
#include "mysleep.h"

char mysleep_rcsid[] = 
  "$Id: mysleep.c,v 1.1 2000/07/22 20:20:50 dholland Exp $";

#ifdef USE_MYSLEEP

char mysleep_in_use[] = "$Info: mysleep is in use $";

void mysleep(int secs) {
   struct timeval tv;
   tv.tv_sec = secs;
   tv.tv_usec = 0;
   select(0, NULL, NULL, NULL, &tv);
}

#endif
