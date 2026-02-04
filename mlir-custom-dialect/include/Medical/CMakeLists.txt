set(LLVM_TARGET_DEFINITIONS MedicalOps.td)

# Generate Dialect classes
mlir_tablegen(MedicalDialect.h.inc -gen-dialect-decls -dialect=medical)
mlir_tablegen(MedicalDialect.cpp.inc -gen-dialect-defs -dialect=medical)

# Generate Operation classes
mlir_tablegen(MedicalOps.h.inc -gen-op-decls)
mlir_tablegen(MedicalOps.cpp.inc -gen-op-defs)

add_public_tablegen_target(MedicalTableGenTarget)