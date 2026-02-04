 cmake_minimum_required(VERSION 3.22)

 project(MedicalDialect VERSION 0.1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_BUILD_TYPE Debug)

find_package(MLIR REQUIRED CONFIG)
find_package(LLVM REQUIRED CONFIG)

list(APPEND CMAKE_MODULE_PATH "${MLIR_CMAKE_DIR}")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")

include(TableGen)
include(AddLLVM)
include(AddMLIR)
include(HandleLLVMOptions)

include_directories(${LLVM_INCLUDE_DIRS})
include_directories(${MLIR_INCLUDE_DIRS})
include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_BINARY_DIR}/include) # For generated .inc files

link_directories(${LLVM_LIBRARY_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_subdirectory(include/Medical)
add_subdirectory(lib/Medical)
# add_subdirectory(tools/medical-opt) (will be added later)

add_subdirectory(tools/medical-opt)

set_target_properties(MLIRMedicalDialect PROPERTIES
         C_VISIBILITY_PRESET default
         CXX_VISIBILITY_PRESET default
         VISIBILITY_INLINES_HIDDEN OFF
 )