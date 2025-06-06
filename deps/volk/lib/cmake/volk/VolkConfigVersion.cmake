# Copyright 2014, 2015, 2018, 2020 Free Software Foundation, Inc.
#
# This file is part of VOLK.
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#

set(MAJOR_VERSION 3)
set(MINOR_VERSION 2)
set(MAINT_VERSION 0)

set(PACKAGE_VERSION ${MAJOR_VERSION}.${MINOR_VERSION}.${MAINT_VERSION})

if(${PACKAGE_FIND_VERSION_MAJOR} EQUAL ${MAJOR_VERSION})
    if(${PACKAGE_FIND_VERSION_MINOR} EQUAL ${MINOR_VERSION})
        if(NOT ${PACKAGE_FIND_VERSION_PATCH} GREATER ${MAINT_VERSION})
            set(PACKAGE_VERSION_EXACT 1) # exact match for API version
            set(PACKAGE_VERSION_COMPATIBLE 1) # compat for minor/patch version
        endif()
    endif()
endif()
