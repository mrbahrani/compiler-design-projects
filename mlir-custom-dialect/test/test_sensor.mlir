// Use the 'medical' prefix we defined in MedicalDialect.td
module {
  func.func @process_sensor_data(%input: tensor<4xf32>) -> tensor<4xf32> {
    // 1. Define a scale factor attribute (e.g., 0.5)
    // 2. Call our custom NormalizeOp
    // The syntax follows the assemblyFormat we wrote: $input attr-dict `:` type($input)
    %result = medical.normalize %input {scale_factor = 0.5 : f32} : tensor<4xf32>

    return %result : tensor<4xf32>
  }
}