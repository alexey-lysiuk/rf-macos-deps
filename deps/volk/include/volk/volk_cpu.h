

/* this file was generated by volk template utils, do not edit! */

/* -*- c++ -*- */
/*
 * Copyright 2011-2012 Free Software Foundation, Inc.
 *
 * This file is part of VOLK
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#ifndef INCLUDED_VOLK_CPU_H
#define INCLUDED_VOLK_CPU_H

#include <volk/volk_common.h>

__VOLK_DECL_BEGIN

struct VOLK_CPU {
    int (*has_generic) ();
    int (*has_softfp) ();
    int (*has_hardfp) ();
    int (*has_32) ();
    int (*has_64) ();
    int (*has_popcount) ();
    int (*has_mmx) ();
    int (*has_fma) ();
    int (*has_sse) ();
    int (*has_sse2) ();
    int (*has_orc) ();
    int (*has_norc) ();
    int (*has_neon) ();
    int (*has_neonv7) ();
    int (*has_neonv8) ();
    int (*has_sse3) ();
    int (*has_ssse3) ();
    int (*has_sse4_a) ();
    int (*has_sse4_1) ();
    int (*has_sse4_2) ();
    int (*has_avx) ();
    int (*has_avx2) ();
    int (*has_avx512f) ();
    int (*has_avx512cd) ();
    int (*has_riscv64) ();
    int (*has_rvv) ();
    int (*has_rvvseg) ();
};

extern struct VOLK_CPU volk_cpu;

void volk_cpu_init ();
unsigned int volk_get_lvarch ();

__VOLK_DECL_END

#endif /*INCLUDED_VOLK_CPU_H*/
