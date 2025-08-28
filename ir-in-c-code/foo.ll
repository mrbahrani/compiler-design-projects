; foo.ll
; Make sure the triple matches your machine (clang -v shows default)
target triple = "x86_64-pc-linux-gnu"           ; Linux example

; define a C-callable function: int add(int, int)
define i32 @add(i32 %a, i32 %b) #0 {
entry:
  %sum = add i32 %a, %b
  ret i32 %sum
}

attributes #0 = { nounwind readnone }
