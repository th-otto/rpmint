/*
 * coreutils-8.28 also triggers this bug
 */
typedef struct __stdio_file FILE;
extern int sprintf (char *__restrict __s, const char *__restrict __format, ...);

typedef long long int __dev_t;
typedef unsigned int __mode_t;

struct stat {
  __dev_t st_dev;
  __dev_t st_rdev;
  __mode_t st_mode;
};

                                                                             ;
typedef unsigned long long int uintmax_t;

char *umaxtostr (uintmax_t, char *);

struct fileinfo
  {

    struct stat stat;

    int stat_ok;
  };

static int major_device_number_width;
static int minor_device_number_width;
static int file_size_width;

void
print_long_format (const struct fileinfo *f)
{
  char buf
    [((2 * 21 + 1) * 2 + 3) + 1
     + ((2 * 21 + 1) * 2 + 3) + 1
     + (21 + 1)
     + ((2 * 21 + 1) * 2 + 3) + 2
     + ((2 * 21 + 1) * 2 + 3) + 1
     ];
  char *p;



  p = buf;

  if (f->stat_ok
      && (((((f->stat.st_mode)) & 0170000) == (0020000)) || ((((f->stat.st_mode)) & 0170000) == (0060000))))
    {
      char majorbuf[21];
      char minorbuf[21];
      int blanks_width = (file_size_width
                          - (major_device_number_width + 2
                             + minor_device_number_width));
      sprintf (p, "%*s, %*s ",
               major_device_number_width + ((0 < blanks_width) ? (blanks_width) : (0)),
               umaxtostr (((long int)(((f->stat.st_rdev) >> 8) & 0xff)), majorbuf),
               minor_device_number_width,
               umaxtostr (((long int)((f->stat.st_rdev) & 0xff)), minorbuf));
    }
}
