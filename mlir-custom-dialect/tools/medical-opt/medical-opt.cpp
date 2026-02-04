//
// Created by abahrani on 2/4/2026.
//

#include "mlir/IR/DialectRegistry.h"
#include "mlir/Tools/mlir-opt/MlirOptMain.h"
#include "mlir/InitAllDialects.h"
#include "Medical/MedicalDialect.h"

int main(int argc, char **argv) {
    mlir::DialectRegistry registry;

    // 1. Register your custom dialect
    registry.insert<mlir::medical::MedicalDialect>();

    // 2. (Optional) Register standard dialects (like 'func' or 'arith')
    // This allows you to wrap your medical ops inside functions.
    mlir::registerAllDialects(registry);

    // 3. Launch the standard MLIR Opt Main loop
    return mlir::asMainReturnCode(
        mlir::MlirOptMain(argc, argv, "Medical Dialect Optimizer\n", registry)
    );
}