#ifndef MEDICAL_OPS_H
#define MEDICAL_OPS_H

#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"

// IMPORTANT: Include this BEFORE the .h.inc file
#include "mlir/Bytecode/BytecodeOpInterface.h"

#define GET_OP_CLASSES
#include "Medical/MedicalOps.h.inc"

#endif // MEDICAL_OPS_H