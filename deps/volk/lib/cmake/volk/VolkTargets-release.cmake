#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Volk::volk" for configuration "Release"
set_property(TARGET Volk::volk APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Volk::volk PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libvolk.3.2.0.dylib"
  IMPORTED_SONAME_RELEASE "${CMAKE_CURRENT_LIST_DIR}/../../libvolk.3.2.dylib"
  )

list(APPEND _cmake_import_check_targets Volk::volk )
list(APPEND _cmake_import_check_files_for_Volk::volk "${_IMPORT_PREFIX}/lib/libvolk.3.2.0.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
