include "mlir/Interfaces/SideEffectInterfaces.td"

// Base class for ops in this dialect to save typing
class Medical_Op<string mnemonic, list<Trait> traits = []> :
    Op<Medical_Dialect, mnemonic, traits>;

def NormalizeOp : Medical_Op<"normalize", [NoSideEffect, SameOperandsAndResultType]> {
  let summary = "Normalizes sensor input within a [0, 1] range.";

  // Arguments can be Operands (values in the IR) or Attributes (compile-time constants)
  let arguments = (ins F32Tensor:$input, F32Attr:$scale_factor);

  let results = (outs F32Tensor:$output);

  // This tells MLIR to generate a standard assembly format so we can read/write it
  let assemblyFormat = "$input attr-dict `:` type($input)";
}