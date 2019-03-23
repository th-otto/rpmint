/* sig.c */
void sig_init(void);
void sig_block(void);
void sig_unblock(void);
void sig_wait(void);
void sig_preexec(void);

/* signal handlers */
void config(int);     /* servtab.c */
void reapchild(int);  /* inetd.c */
void retry(int);      /* inetd.c */
void goaway(int);     /* inetd.c */
