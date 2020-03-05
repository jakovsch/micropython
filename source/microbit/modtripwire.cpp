//  "tripwire" - Dodatni C moduli i metode
//  Jakov Schramadei, 2.F, V.Gimnazija, Zagreb
//  Pogledajte license.md za legalne informacije.

#include <stdio.h>

extern "C" {

#include "py/obj.h"
#include "microbit/modmicrobit.h"

/*
    Declare objects - functions and __init__
*/

STATIC mp_obj_t this__init__(void) {
    STATIC const char *this_text =
"Tripwire C module initialized.\n";
    mp_printf(&mp_plat_print, "%s", this_text);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(this___init___obj, this__init__);

STATIC mp_obj_t this_test(void) {
    return mp_obj_new_int(1+1);
}
MP_DEFINE_CONST_FUN_OBJ_0(this_test_obj, this_test);

/*
    Map objects to global (Python) QSTRs
*/

STATIC const mp_map_elem_t this_module_globals_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_this) },
    { MP_OBJ_NEW_QSTR(MP_QSTR___init__), (mp_obj_t)&this___init___obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_test), (mp_obj_t)&this_test_obj },
};

STATIC MP_DEFINE_CONST_DICT(this_module_globals, this_module_globals_table);

const mp_obj_module_t this_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&this_module_globals,
};

// End extern
}
