/* -*- C -*- */
/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of VOLK
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#ifndef INCLUDED_VOLK_VERSION_H
#define INCLUDED_VOLK_VERSION_H

#include <volk/volk_common.h>

__VOLK_DECL_BEGIN

/*
 * define macros for the Volk version, which can then be used by any
 * project that #include's this header, e.g., to determine whether
 * some specific API is present and functional.
 */

#define VOLK_VERSION_MAJOR 3
#define VOLK_VERSION_MINOR 2
#define VOLK_VERSION_MAINT 0

/*
 * VOLK_VERSION % 100 is the MAINT version
 * (VOLK_VERSION / 100) % 100 is the MINOR version
 * (VOLK_VERSION / 100) / 100 is the MAJOR version
 */

#define VOLK_VERSION 30200

__VOLK_DECL_END

#endif /* INCLUDED_VOLK_VERSION_H */
