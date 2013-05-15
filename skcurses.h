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

#ifndef _SKCURSES_H
#define _SKCURSES_H 1

#define SKCUR_COLOR_WHITE   0
#define SKCUR_COLOR_RED     1
#define SKCUR_COLOR_BLUE    2
#define SKCUR_COLOR_INFO (SKCUR_COLOR_BLUE)
#define SKCUR_COLOR_SCORE (SKCUR_COLOR_RED)

#define SKCUR_SUCCESS 1
#define SKCUR_ERR_COLOR_INIT_FAIL -1
#define SKCUR_ERR_INIT_FAIL -2
#define SKCUR_ERR_INFO_TOO_LONG -3
#define SKCUR_ERR_REFRESH_FAIL -4

#define MAX_INFO_LENGTH 15
#define INFO_POS 20
#define SCO_POS 3

#define POINT_CHR '#'

int skcur_init(void);
int skcur_write_info(const char * info);
int skcur_write_score(int score);
int skcur_draw_point(int y,int x,short int color);
int skcur_erase_point(int y,int x);
int skcur_refresh(void);
int skcur_getch(int * ch);
int skcur_get_scr_width(int * ret);
int skcur_get_scr_height(int * ret);
int skcur_end(void);

#endif
