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

#include <Python.h>
#include "skcurses.h"

/* modulename = skcurses */
static PyObject * wrap_skcur_init(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_write_info(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_write_score(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_draw_point(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_erase_point(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_refresh(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_getch(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_get_scr_width(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_get_scr_height(PyObject * self,PyObject * args);
static PyObject * wrap_skcur_end(PyObject * self,PyObject * args);

/* Methods Entry define here */
static PyMethodDef _Methods[] = {
    {"skcur_init"           , wrap_skcur_init           , METH_NOARGS   , "skcur()"},
    {"skcur_write_info"     , wrap_skcur_write_info     , METH_VARARGS  , "skcur_write_info(info)"},
    {"skcur_write_score"    , wrap_skcur_write_score    , METH_VARARGS  , "skcur_write_score(score)"},
    {"skcur_draw_point"     , wrap_skcur_draw_point     , METH_VARARGS  , "skcur_draw_point(y,x,color)"},
    {"skcur_erase_point"    , wrap_skcur_erase_point    , METH_VARARGS  , "skcur_erase_point(y,x)"},
    {"skcur_refresh"        , wrap_skcur_refresh        , METH_NOARGS   , "skcur_refersh()"},
    {"skcur_getch"          , wrap_skcur_getch          , METH_NOARGS   , "skcur_getch()"},
    {"skcur_get_scr_width"  , wrap_skcur_get_scr_width  , METH_NOARGS   , "skcur_get_scr_width()"},
    {"skcur_get_scr_height" , wrap_skcur_get_scr_height , METH_NOARGS   , "skcur_get_scr_height()"},
    {"skcur_end"            , wrap_skcur_end            , METH_NOARGS   , "skcur_end()"},
    {NULL,NULL},
};

/* PyModule Entry */
void initskcurses(void)
{
    PyObject * m = Py_InitModule("skcurses",_Methods);
    PyModule_AddIntMacro(m,SKCUR_COLOR_WHITE);
    PyModule_AddIntMacro(m,SKCUR_COLOR_RED);
    PyModule_AddIntMacro(m,SKCUR_COLOR_BLUE);
    PyModule_AddIntMacro(m,SKCUR_COLOR_INFO);
    PyModule_AddIntMacro(m,SKCUR_COLOR_SCORE);
    PyModule_AddIntMacro(m,MAX_INFO_LENGTH);
}

#include <string.h>
#define _raise_exc(s) { \
        PyErr_SetString(PyExc_RuntimeError,s); \
        return NULL;\
    }

PyObject * wrap_skcur_init(PyObject * self,PyObject * args)
{
    int errid = skcur_init();
    if(errid == SKCUR_ERR_COLOR_INIT_FAIL) {
        _raise_exc("Initializing color for terminal failed!");
    } else if(errid == SKCUR_ERR_INIT_FAIL) {
        _raise_exc("Terminal initializing failed!");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * wrap_skcur_write_info(PyObject * self,PyObject * args)
{
    static char str_buffer[MAX_INFO_LENGTH + 1];
    char * str_buf;
    if(!PyArg_ParseTuple(args,"s",&str_buf))
        return NULL;
    strcpy(str_buffer,str_buf);
    int errid = skcur_write_info(str_buffer);
    if(errid == SKCUR_ERR_INFO_TOO_LONG) {
        _raise_exc("The length of infomation must belong MAX_INFO_LENGTH!");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * wrap_skcur_write_score(PyObject * self,PyObject * args)
{
    int score;
    if(!PyArg_ParseTuple(args,"i",&score))
        return NULL;
    int errid = skcur_write_score(score);
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * wrap_skcur_draw_point(PyObject * self,PyObject * args)
{
    int y,x;
    short int color;
    if(!PyArg_ParseTuple(args,"iih",&y,&x,&color))
        return NULL;
    int errid = skcur_draw_point(y,x,color);
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * wrap_skcur_erase_point(PyObject * self,PyObject * args)
{
    int y,x;
    if(!PyArg_ParseTuple(args,"ii",&y,&x))
        return NULL;
    int errid = skcur_erase_point(y,x);
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * wrap_skcur_refresh(PyObject * self,PyObject * args)
{
    int errid = skcur_refresh();
    if(errid == SKCUR_ERR_REFRESH_FAIL) {
        _raise_exc("Refresh failed!");
    }
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject * wrap_skcur_getch(PyObject * self,PyObject * args)
{
    int ch;
    int errid = skcur_getch(&ch);
    return Py_BuildValue("i",ch);
}

PyObject * wrap_skcur_get_scr_width(PyObject * self,PyObject * args)
{
    int ret;
    int errid = skcur_get_scr_width(&ret);
    return Py_BuildValue("i",ret);
}

PyObject * wrap_skcur_get_scr_height(PyObject * self,PyObject * args)
{
    int ret;
    int errid = skcur_get_scr_height(&ret);
    return Py_BuildValue("i",ret);
}

PyObject * wrap_skcur_end(PyObject * self,PyObject * args)
{
    int errid = skcur_end();
    Py_INCREF(Py_None);
    return Py_None;
}
#undef _raise_exc
