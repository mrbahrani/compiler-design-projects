add_mlir_tool(medical-opt
        medical-opt.cpp
)

target_link_libraries(medical-opt
        PRIVATE
        MLIRMedicalDialect   # Your library from Project 1
        MLIRIR               # Core IR classes
        MLIRParser           # To read .mlir files
        MLIRSupport          # Basic utilities
        MLIROptLib       # The 'Main' logic we called in C++
#        MLIRInitAllDialects  # If you included registerAllDialects
        MLIRRegisterAllDialects
        MLIRSupport
)