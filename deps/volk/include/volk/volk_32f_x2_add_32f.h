/* -*- c++ -*- */
/*
 * Copyright 2012, 2014 Free Software Foundation, Inc.
 *
 * This file is part of VOLK
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

/*!
 * \page volk_32f_x2_add_32f
 *
 * \b Overview
 *
 * Adds two vectors together element by element:
 *
 * c[i] = a[i] + b[i]
 *
 * <b>Dispatcher Prototype</b>
 * \code
 * void volk_32f_x2_add_32f(float* cVector, const float* aVector, const float* bVector,
 * unsigned int num_points) \endcode
 *
 * \b Inputs
 * \li aVector: First vector of input points.
 * \li bVector: Second vector of input points.
 * \li num_points: The number of values in both input vector.
 *
 * \b Outputs
 * \li cVector: The output vector.
 *
 * \b Example
 *
 * The follow example adds the increasing and decreasing vectors such that the result of
 * every summation pair is 10
 *
 * \code
 *   int N = 10;
 *   unsigned int alignment = volk_get_alignment();
 *   float* increasing = (float*)volk_malloc(sizeof(float)*N, alignment);
 *   float* decreasing = (float*)volk_malloc(sizeof(float)*N, alignment);
 *   float* out = (float*)volk_malloc(sizeof(float)*N, alignment);
 *
 *   for(unsigned int ii = 0; ii < N; ++ii){
 *       increasing[ii] = (float)ii;
 *       decreasing[ii] = 10.f - (float)ii;
 *   }
 *
 *   volk_32f_x2_add_32f(out, increasing, decreasing, N);
 *
 *   for(unsigned int ii = 0; ii < N; ++ii){
 *       printf("out[%u] = %1.2f\n", ii, out[ii]);
 *   }
 *
 *   volk_free(increasing);
 *   volk_free(decreasing);
 *   volk_free(out);
 * \endcode
 */

#ifndef INCLUDED_volk_32f_x2_add_32f_u_H
#define INCLUDED_volk_32f_x2_add_32f_u_H

#include <inttypes.h>
#include <stdio.h>

#ifdef LV_HAVE_AVX512F
#include <immintrin.h>

static inline void volk_32f_x2_add_32f_u_avx512f(float* cVector,
                                                 const float* aVector,
                                                 const float* bVector,
                                                 unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int sixteenthPoints = num_points / 16;

    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;

    __m512 aVal, bVal, cVal;
    for (; number < sixteenthPoints; number++) {

        aVal = _mm512_loadu_ps(aPtr);
        bVal = _mm512_loadu_ps(bPtr);

        cVal = _mm512_add_ps(aVal, bVal);

        _mm512_storeu_ps(cPtr, cVal); // Store the results back into the C container

        aPtr += 16;
        bPtr += 16;
        cPtr += 16;
    }

    number = sixteenthPoints * 16;

    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}

#endif /* LV_HAVE_AVX512F */


#ifdef LV_HAVE_AVX
#include <immintrin.h>

static inline void volk_32f_x2_add_32f_u_avx(float* cVector,
                                             const float* aVector,
                                             const float* bVector,
                                             unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int eighthPoints = num_points / 8;
    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;
    __m256 aVal, bVal, cVal;
    for (; number < eighthPoints; number++) {

        aVal = _mm256_loadu_ps(aPtr);
        bVal = _mm256_loadu_ps(bPtr);

        cVal = _mm256_add_ps(aVal, bVal);

        _mm256_storeu_ps(cPtr, cVal); // Store the results back into the C container

        aPtr += 8;
        bPtr += 8;
        cPtr += 8;
    }

    number = eighthPoints * 8;

    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}
#endif /* LV_HAVE_AVX */


#ifdef LV_HAVE_SSE
#include <xmmintrin.h>

static inline void volk_32f_x2_add_32f_u_sse(float* cVector,
                                             const float* aVector,
                                             const float* bVector,
                                             unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int quarterPoints = num_points / 4;

    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;

    __m128 aVal, bVal, cVal;
    for (; number < quarterPoints; number++) {

        aVal = _mm_loadu_ps(aPtr);
        bVal = _mm_loadu_ps(bPtr);

        cVal = _mm_add_ps(aVal, bVal);

        _mm_storeu_ps(cPtr, cVal); // Store the results back into the C container

        aPtr += 4;
        bPtr += 4;
        cPtr += 4;
    }

    number = quarterPoints * 4;
    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}
#endif /* LV_HAVE_SSE */


#ifdef LV_HAVE_GENERIC

static inline void volk_32f_x2_add_32f_generic(float* cVector,
                                               const float* aVector,
                                               const float* bVector,
                                               unsigned int num_points)
{
    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;
    unsigned int number = 0;

    for (number = 0; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}
#endif /* LV_HAVE_GENERIC */


#endif /* INCLUDED_volk_32f_x2_add_32f_u_H */
#ifndef INCLUDED_volk_32f_x2_add_32f_a_H
#define INCLUDED_volk_32f_x2_add_32f_a_H

#include <inttypes.h>
#include <stdio.h>

#ifdef LV_HAVE_AVX512F
#include <immintrin.h>

static inline void volk_32f_x2_add_32f_a_avx512f(float* cVector,
                                                 const float* aVector,
                                                 const float* bVector,
                                                 unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int sixteenthPoints = num_points / 16;

    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;

    __m512 aVal, bVal, cVal;
    for (; number < sixteenthPoints; number++) {

        aVal = _mm512_load_ps(aPtr);
        bVal = _mm512_load_ps(bPtr);

        cVal = _mm512_add_ps(aVal, bVal);

        _mm512_store_ps(cPtr, cVal); // Store the results back into the C container

        aPtr += 16;
        bPtr += 16;
        cPtr += 16;
    }

    number = sixteenthPoints * 16;

    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}

#endif /* LV_HAVE_AVX512F */


#ifdef LV_HAVE_AVX
#include <immintrin.h>

static inline void volk_32f_x2_add_32f_a_avx(float* cVector,
                                             const float* aVector,
                                             const float* bVector,
                                             unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int eighthPoints = num_points / 8;

    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;

    __m256 aVal, bVal, cVal;
    for (; number < eighthPoints; number++) {

        aVal = _mm256_load_ps(aPtr);
        bVal = _mm256_load_ps(bPtr);

        cVal = _mm256_add_ps(aVal, bVal);

        _mm256_store_ps(cPtr, cVal); // Store the results back into the C container

        aPtr += 8;
        bPtr += 8;
        cPtr += 8;
    }

    number = eighthPoints * 8;
    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}
#endif /* LV_HAVE_AVX */

#ifdef LV_HAVE_SSE
#include <xmmintrin.h>

static inline void volk_32f_x2_add_32f_a_sse(float* cVector,
                                             const float* aVector,
                                             const float* bVector,
                                             unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int quarterPoints = num_points / 4;

    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;

    __m128 aVal, bVal, cVal;
    for (; number < quarterPoints; number++) {
        aVal = _mm_load_ps(aPtr);
        bVal = _mm_load_ps(bPtr);

        cVal = _mm_add_ps(aVal, bVal);

        _mm_store_ps(cPtr, cVal); // Store the results back into the C container

        aPtr += 4;
        bPtr += 4;
        cPtr += 4;
    }

    number = quarterPoints * 4;
    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}
#endif /* LV_HAVE_SSE */


#ifdef LV_HAVE_NEON
#include <arm_neon.h>

static inline void volk_32f_x2_add_32f_u_neon(float* cVector,
                                              const float* aVector,
                                              const float* bVector,
                                              unsigned int num_points)
{
    unsigned int number = 0;
    const unsigned int quarterPoints = num_points / 4;

    float* cPtr = cVector;
    const float* aPtr = aVector;
    const float* bPtr = bVector;
    float32x4_t aVal, bVal, cVal;
    for (number = 0; number < quarterPoints; number++) {
        // Load in to NEON registers
        aVal = vld1q_f32(aPtr);
        bVal = vld1q_f32(bPtr);
        __VOLK_PREFETCH(aPtr + 4);
        __VOLK_PREFETCH(bPtr + 4);

        // vector add
        cVal = vaddq_f32(aVal, bVal);
        // Store the results back into the C container
        vst1q_f32(cPtr, cVal);

        aPtr += 4; // q uses quadwords, 4 floats per vadd
        bPtr += 4;
        cPtr += 4;
    }

    number = quarterPoints * 4; // should be = num_points
    for (; number < num_points; number++) {
        *cPtr++ = (*aPtr++) + (*bPtr++);
    }
}

#endif /* LV_HAVE_NEON */

#ifdef LV_HAVE_NEONV7
extern void volk_32f_x2_add_32f_a_neonasm(float* cVector,
                                          const float* aVector,
                                          const float* bVector,
                                          unsigned int num_points);
#endif /* LV_HAVE_NEONV7 */

#ifdef LV_HAVE_NEONV7
extern void volk_32f_x2_add_32f_a_neonpipeline(float* cVector,
                                               const float* aVector,
                                               const float* bVector,
                                               unsigned int num_points);
#endif /* LV_HAVE_NEONV7 */


#ifdef LV_HAVE_ORC

extern void volk_32f_x2_add_32f_a_orc_impl(float* cVector,
                                           const float* aVector,
                                           const float* bVector,
                                           int num_points);

static inline void volk_32f_x2_add_32f_u_orc(float* cVector,
                                             const float* aVector,
                                             const float* bVector,
                                             unsigned int num_points)
{
    volk_32f_x2_add_32f_a_orc_impl(cVector, aVector, bVector, num_points);
}

#endif /* LV_HAVE_ORC */

#ifdef LV_HAVE_RVV
#include <riscv_vector.h>

static inline void volk_32f_x2_add_32f_rvv(float* cVector,
                                           const float* aVector,
                                           const float* bVector,
                                           unsigned int num_points)
{
    size_t n = num_points;
    for (size_t vl; n > 0; n -= vl, aVector += vl, bVector += vl, cVector += vl) {
        vl = __riscv_vsetvl_e32m8(n);
        vfloat32m8_t va = __riscv_vle32_v_f32m8(aVector, vl);
        vfloat32m8_t vb = __riscv_vle32_v_f32m8(bVector, vl);
        __riscv_vse32(cVector, __riscv_vfadd(va, vb, vl), vl);
    }
}
#endif /*LV_HAVE_RVV*/

#endif /* INCLUDED_volk_32f_x2_add_32f_a_H */
