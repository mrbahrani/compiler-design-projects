//===- MedicalDialect.td - //ToDo: breif ---------------*- tablegent -*-===//
// Author: Ali Bahrani
//===-----------------------------------------------===//

include "mlir/IR/OpBase.td"
include "mlir/Bytecode/BytecodeOpInterface.td"


def Medical_Dialect : Dialect {
  let name = "medical";
  let summary = "A dialect for medical sensor data processing.";
  let description = [{
    This dialect provides operations to ingest, filter, and
    normalize data from medical devices.
  }];

  let cppNamespace = "::mlir::medical";
  let extraClassDeclaration = [{
      // This allows the dialect to use the new Bytecode format
//      void initialize();
    }];

//    let hasBytecodeInterface = 1;
}