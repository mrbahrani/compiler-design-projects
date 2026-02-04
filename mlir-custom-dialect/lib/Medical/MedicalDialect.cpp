//
// Created by abahrani on 2/3/2026.
//

#include "mlir/IR/Builders.h"
#include "Medical/MedicalDialect.h"
#include "Medical/MedicalOps.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/Bytecode/BytecodeOpInterface.h" // Specifically for Op interface
#include "mlir/IR/DialectImplementation.h"     // For Dialect-level bytecode hooks

using namespace mlir;
using namespace mlir::medical;

// The TableGen generated logic is included here via headers
#include "Medical/MedicalDialect.cpp.inc"

#define GET_OP_CLASSES
#include "Medical/MedicalOps.cpp.inc"

void MedicalDialect::initialize() {
    addOperations<
  #define GET_OP_LIST
  #include "Medical/MedicalOps.cpp.inc"
    >();
}