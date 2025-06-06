/* -*- c++ -*- */
/*
 * Copyright 2012, 2014 Free Software Foundation, Inc.
 *
 * This file is part of VOLK
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

/*!
 * \page volk_32u_popcnt
 *
 * \b Overview
 *
 * Computes the population count (popcnt), or Hamming distance of a
 * binary string. This kernel takes in a single unsigned 32-bit value
 * and returns the count of 1's that the value contains.
 *
 * <b>Dispatcher Prototype</b>
 * \code
 * void volk_32u_popcnt(uint32_t* ret, const uint32_t value)
 * \endcode
 *
 * \b Inputs
 * \li value: The input value.
 *
 * \b Outputs
 * \li ret: The return value containing the popcnt.
 *
 * \b Example
 * \code
    int N = 10;
    unsigned int alignment = volk_get_alignment();

    uint32_t bitstring = 0x55555555;
    uint32_t hamming_distance = 0;

    volk_32u_popcnt(&hamming_distance, bitstring);
    printf("hamming distance of %x = %i\n", bitstring, hamming_distance);
 * \endcode
 */

#ifndef INCLUDED_VOLK_32u_POPCNT_A16_H
#define INCLUDED_VOLK_32u_POPCNT_A16_H

#include <inttypes.h>
#include <stdio.h>

#ifdef LV_HAVE_GENERIC

static inline void volk_32u_popcnt_generic(uint32_t* ret, const uint32_t value)
{
    // This is faster than a lookup table
    uint32_t retVal = value;

    retVal = (retVal & 0x55555555) + (retVal >> 1 & 0x55555555);
    retVal = (retVal & 0x33333333) + (retVal >> 2 & 0x33333333);
    retVal = (retVal + (retVal >> 4)) & 0x0F0F0F0F;
    retVal = (retVal + (retVal >> 8));
    retVal = (retVal + (retVal >> 16)) & 0x0000003F;

    *ret = retVal;
}

#endif /*LV_HAVE_GENERIC*/


#ifdef LV_HAVE_SSE4_2

#include <nmmintrin.h>

static inline void volk_32u_popcnt_a_sse4_2(uint32_t* ret, const uint32_t value)
{
    *ret = _mm_popcnt_u32(value);
}

#endif /*LV_HAVE_SSE4_2*/

#ifdef LV_HAVE_RVV
#include <riscv_vector.h>

static inline void volk_32u_popcnt_rvv(uint32_t* ret, const uint32_t value)
{
    *ret = __riscv_vcpop(__riscv_vreinterpret_b4(__riscv_vmv_s_x_u64m1(value, 1)), 32);
}
#endif /*LV_HAVE_RVV*/

#ifdef LV_HAVE_RVA22V
#include <riscv_bitmanip.h>

static inline void volk_32u_popcnt_rva22(uint32_t* ret, const uint32_t value)
{
    *ret = __riscv_cpop_32(value);
}
#endif /*LV_HAVE_RVA22V*/

#endif /*INCLUDED_VOLK_32u_POPCNT_A16_H*/
