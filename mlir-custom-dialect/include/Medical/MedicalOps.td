include "mlir/IR/OpBase.td"
include "mlir/Interfaces/SideEffectInterfaces.td"
//include "mlir/IR/CommonTypeConstraints.td"

include "MedicalDialect.td"


// Base class for ops in this dialect to save typing
class Medical_Op<string mnemonic, list<Trait> traits = []> :
    Op<Medical_Dialect, mnemonic, traits>;

def NormalizeOp : Medical_Op<"normalize", [
    Pure,
    AllTypesMatch<["input", "output"]>
  ]> {
  let summary = "Normalizes sensor input.";
  let arguments = (ins F32Tensor:$input, F32Attr:$scale_factor);
  let results = (outs F32Tensor:$output);

  // We add 'type($output)' to the format to make it explicit
  let assemblyFormat = "$input attr-dict `:` type($input)";
}