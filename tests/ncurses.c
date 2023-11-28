#include <ncurses/ncurses.h>
#include <stdlib.h>
#define _NCURSES_BACKGROUND_COLOR COLOR_BLACK

int main(void)
{
    volatile unsigned char ch;
    
    #if defined(__atarist__)
    if (getenv("TERM") == NULL)
        putenv("TERM=st52");
    #endif
    initscr();   
    noecho();
    curs_set(0);
    start_color();
    cbreak();
    intrflush(stdscr, TRUE);
    init_pair(1, COLOR_YELLOW, _NCURSES_BACKGROUND_COLOR);
    init_pair(2, COLOR_CYAN, _NCURSES_BACKGROUND_COLOR);
    init_pair(3, COLOR_RED, _NCURSES_BACKGROUND_COLOR);
    init_pair(4, COLOR_GREEN, _NCURSES_BACKGROUND_COLOR);
    init_pair(5, COLOR_BLUE, _NCURSES_BACKGROUND_COLOR);
    init_pair(6, COLOR_WHITE, _NCURSES_BACKGROUND_COLOR);
    init_pair(7, COLOR_MAGENTA, _NCURSES_BACKGROUND_COLOR);
    init_pair(8, COLOR_BLACK, _NCURSES_BACKGROUND_COLOR);

    wbkgd(stdscr, COLOR_PAIR(1));   
    nodelay(stdscr,TRUE);    
    refresh();
 
    move(0,0);
    while(1)
    {
        ch = getch();      
        if(ch=='i' || ch=='k')
        {
            printw("%c", ch);
        }
        refresh();
        if (ch == 'q' || ch == 0x1b)
        	break;
    }
    endwin();
    return 0;
}

