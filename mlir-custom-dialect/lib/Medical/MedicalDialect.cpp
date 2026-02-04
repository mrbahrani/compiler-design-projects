//
// Created by abahrani on 2/3/2026.
//

#include "Medical/MedicalDialect.h"
#include "Medical/MedicalOps.h"

using namespace mlir;
using namespace mlir::medical;

// The TableGen generated logic is included here via headers
#include "Medical/MedicalDialect.cpp.inc"

void MedicalDialect::initialize() {
    addOperations<
  #define GET_OP_LIST
  #include "Medical/MedicalOps.cpp.inc"
    >();
}