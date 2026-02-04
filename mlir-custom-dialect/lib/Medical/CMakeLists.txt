

add_mlir_library(MLIRMedicalDialect
        MedicalDialect.cpp

        # 1. FORCE THE ORDER: Don't compile .cpp until TableGen is done
        DEPENDS
        MedicalTableGenTarget

        # 2. LINK THE LIBS: Standard MLIR libraries required for dialects
        LINK_LIBS
        MLIRIR
        MLIRSideEffectInterfaces
)

