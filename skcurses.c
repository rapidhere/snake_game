/** 
 Copyright (C) 2013 rapidhere

 Author:     rapidhere <rapidhere@gmail.com>
 Maintainer: rapidhere <rapidhere@gmail.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


#include <curses.h>
#include "skcurses.h"
#include <string.h>

const int SKCUR_COLORS[][3] = {
    {SKCUR_COLOR_WHITE,COLOR_WHITE,COLOR_WHITE},
    {SKCUR_COLOR_RED,COLOR_RED,COLOR_WHITE},
    {SKCUR_COLOR_BLUE,COLOR_BLUE,COLOR_WHITE},
    {-1,-1,-1}
};

static WINDOW * workwin = NULL;

int skcur_init(void)
{
    int i;
    if(!initscr()) {
        return SKCUR_ERR_INIT_FAIL;
    }
    noecho();
    cbreak();

    if((!has_colors()) || (start_color() != OK)) {
        endwin();
        return SKCUR_ERR_COLOR_INIT_FAIL;
    }
    
    int col_nm,col_fg,col_bg;
    for(i = 0;;i ++) {
        col_nm = SKCUR_COLORS[i][0];
        col_fg = SKCUR_COLORS[i][1];
        col_bg = SKCUR_COLORS[i][2];
        if(col_nm == -1 && col_fg == -1 && col_bg == -1)
            break;
        init_pair(col_nm,col_fg,col_bg);
    }
    
    workwin = subwin(stdscr,LINES - 1,COLS,1,0);
    if(!workwin) {
        return SKCUR_ERR_INIT_FAIL;
    }
    box(workwin,ACS_VLINE,ACS_HLINE);
    return SKCUR_SUCCESS;
}

int skcur_write_info(const char * info)
{
    static int last_len = 0;
    int len = strlen(info);
    if(len > MAX_INFO_LENGTH)
        return SKCUR_ERR_INFO_TOO_LONG;
    int i;
    for(i = 0;i < last_len;i ++)
        mvprintw(0,INFO_POS + i," ");
    attron(COLOR_PAIR(SKCUR_COLOR_INFO));
    //mvaddstr(0,INFO_POS,info);
    mvprintw(0,INFO_POS,"%s",info);
    attroff(COLOR_PAIR(SKCUR_COLOR_INFO));
    last_len = len;
    return SKCUR_SUCCESS;
}

int skcur_write_score(int score)
{
    attron(COLOR_PAIR(SKCUR_COLOR_SCORE));
    mvprintw(0,SCO_POS,"%d",score);
    attroff(COLOR_PAIR(SKCUR_COLOR_SCORE));
    return SKCUR_SUCCESS;
}

int skcur_draw_point(int y,int x,short int color)
{
    attron(COLOR_PAIR(color));
    mvwprintw(workwin,y + 1,x + 1,"%c",POINT_CHR);
    attroff(COLOR_PAIR(color));
    return SKCUR_SUCCESS;
}

int skcur_erase_point(int y,int x)
{
    mvwprintw(workwin,y + 1,x + 1," ");
    return SKCUR_SUCCESS;
}

int skcur_refresh(void)
{
    if(touchwin(stdscr) != OK)
        return SKCUR_ERR_REFRESH_FAIL;
    if(move(0,0) != OK)
        return SKCUR_ERR_REFRESH_FAIL;
    if(refresh() != OK)
        return SKCUR_ERR_REFRESH_FAIL;
    return SKCUR_SUCCESS;
}

int skcur_getch(int * ch)
{
    *ch = getch();
    return SKCUR_SUCCESS;
}
int skcur_get_scr_width(int * ret)
{
    *ret = getmaxx(workwin) - 2;
    return SKCUR_SUCCESS;
}

int skcur_get_scr_height(int * ret)
{
    *ret = getmaxy(workwin) - 2;
    return SKCUR_SUCCESS;
}

int skcur_end(void)
{
    endwin();
    return SKCUR_SUCCESS;
}
