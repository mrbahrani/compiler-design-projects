add_mlir_library(MLIRMedicalDialect
        MedicalDialect.cpp

        # Ensure TableGen runs before compiling these C++ files
        DEPENDS
        MedicalTableGenTarget

        LINK_LIBS
        MLIRIR
        MLIRSideEffectInterfaces
)