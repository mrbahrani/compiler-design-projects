#ifndef MEDICAL_MEDICALOPS_H
#define MEDICAL_MEDICALOPS_H

#include "mlir/IR/BuiltinTypes.h"
#include "mlir/IR/OpDefinition.h"
#include "mlir/Interfaces/SideEffectInterfaces.h"
#include "Medical/MedicalDialect.h"

// Include the generated operation declarations
#define GET_OP_CLASSES
#include "Medical/MedicalOps.h.inc"

#endif // MEDICAL_MEDICALOPS_H