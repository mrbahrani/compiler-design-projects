#!/usr/bin/env python3
"""
Tiny expression → LLVM IR compiler.

- Input: a text file containing a single arithmetic expression using integers,
  +, -, *, /, unary +/-, and parentheses.
- Output: LLVM IR (.ll) that defines a `main` which prints the result.

Usage:
  python3 tiny_compiler.py expr.txt -o out.ll
  # then either run with LLVM's interpreter:
  lli out.ll
  # or compile a native executable:
  llc -filetype=obj out.ll -o out.o
  clang out.o -o expr && ./expr

Examples of valid expressions:
  1+2*3
  -(3 + 4) / 2
  (10 - 3) * (7 - 5) + 42
"""
import argparse
import sys

# ---------- Lexer ----------
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current = text[0] if text else None

    def advance(self):
        self.pos += 1
        self.current = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_ws(self):
        while self.current is not None and self.current.isspace():
            self.advance()

    def integer(self):
        s = ""
        while self.current is not None and self.current.isdigit():
            s += self.current
            self.advance()
        return int(s)

    def get_next_token(self):
        self.skip_ws()
        c = self.current
        if c is None:
            return Token('EOF')
        if c.isdigit():
            return Token('NUMBER', self.integer())
        if c == '+':
            self.advance(); return Token('PLUS')
        if c == '-':
            self.advance(); return Token('MINUS')
        if c == '*':
            self.advance(); return Token('MUL')
        if c == '/':
            self.advance(); return Token('DIV')
        if c == '(':
            self.advance(); return Token('LPAREN')
        if c == ')':
            self.advance(); return Token('RPAREN')
        raise SyntaxError(f"Unexpected character: {c}")

# ---------- AST ----------
class AST: pass
class Number(AST):
    def __init__(self, value): self.value = value
class BinOp(AST):
    def __init__(self, op, left, right): self.op, self.left, self.right = op, left, right
class UnaryOp(AST):
    def __init__(self, op, expr): self.op, self.expr = op, expr

# ---------- Parser (recursive descent) ----------
class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.current = self.lexer.get_next_token()

    def eat(self, t):
        if self.current.type == t:
            self.current = self.lexer.get_next_token()
        else:
            raise SyntaxError(f"Expected token {t}, got {self.current}")

    def parse(self):
        node = self.expr()
        if self.current.type != 'EOF':
            raise SyntaxError("Trailing input after expression")
        return node

    # expr := term (('+'|'-') term)*
    def expr(self):
        node = self.term()
        while self.current.type in ('PLUS', 'MINUS'):
            op = self.current.type
            self.eat(op)
            node = BinOp(op, node, self.term())
        return node

    # term := factor (('*'|'/') factor)*
    def term(self):
        node = self.factor()
        while self.current.type in ('MUL', 'DIV'):
            op = self.current.type
            self.eat(op)
            node = BinOp(op, node, self.factor())
        return node

    # factor := NUMBER | '(' expr ')' | ('+'|'-') factor
    def factor(self):
        tok = self.current
        if tok.type == 'PLUS':
            self.eat('PLUS')
            return UnaryOp('PLUS', self.factor())
        if tok.type == 'MINUS':
            self.eat('MINUS')
            return UnaryOp('MINUS', self.factor())
        if tok.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(tok.value)
        if tok.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        raise SyntaxError(f"Unexpected token: {tok}")

# ---------- LLVM IR generator (textual) ----------
class IRGen:
    def __init__(self, print_result=True):
        self.lines = []
        self.reg = 0
        self.print_result = print_result

    def newreg(self):
        self.reg += 1
        return f"%t{self.reg}"

    def emit_bin(self, op, a, b):
        r = self.newreg()
        self.lines.append(f"  {r} = {op} i64 {a}, {b}")
        return r

    def gen(self, node):
        if isinstance(node, Number):
            return str(node.value)
        if isinstance(node, UnaryOp):
            v = self.gen(node.expr)
            if node.op == 'PLUS':
                return v
            if node.op == 'MINUS':
                # If immediate, fold; otherwise 0 - v
                if v.lstrip('-').isdigit():
                    return str(-int(v))
                return self.emit_bin('sub', '0', v)
            raise ValueError("Unknown unary op")
        if isinstance(node, BinOp):
            a = self.gen(node.left)
            b = self.gen(node.right)
            opmap = {'PLUS':'add','MINUS':'sub','MUL':'mul','DIV':'sdiv'}
            return self.emit_bin(opmap[node.op], a, b)
        raise ValueError("Unknown AST node")

    def build_module(self, expr_ast):
        result_val = self.gen(expr_ast)

        out = []
        out.append("; ModuleID = 'tinyexpr'")
        if self.print_result:
            out.append('declare i32 @printf(i8*, ...)\n')
            out.append('@.fmt = private unnamed_addr constant [6 x i8] c"%lld\\0A\\00"\n')

        out.append('define i32 @main() {')
        out.append('entry:')
        out.extend(self.lines)

        if self.print_result:
            out.append('  %fmtptr = getelementptr inbounds [6 x i8], [6 x i8]* @.fmt, i64 0, i64 0')
            out.append(f'  call i32 (i8*, ...) @printf(i8* %fmtptr, i64 {result_val})')
            out.append('  ret i32 0')
        else:
            # Return the (truncated) result as process exit code
            if result_val.lstrip('-').isdigit():
                val = int(result_val)
                if val < -2**31 or val >= 2**31:
                    r64 = self.newreg()
                    out.append(f'  {r64} = add i64 0, {val}')
                    r32 = self.newreg()
                    out.append(f'  {r32} = trunc i64 {r64} to i32')
                    out.append(f'  ret i32 {r32}')
                else:
                    out.append(f'  ret i32 {val}')
            else:
                r32 = self.newreg()
                out.append(f'  {r32} = trunc i64 {result_val} to i32')
                out.append(f'  ret i32 {r32}')
        out.append('}')
        return '\n'.join(out)

def compile_to_ir(expr_text: str, print_result: bool = True) -> str:
    ast = Parser(expr_text).parse()
    return IRGen(print_result=print_result).build_module(ast)

def main():
    ap = argparse.ArgumentParser(description="Tiny expression -> LLVM IR compiler")
    ap.add_argument("input", help="Path to file containing a single arithmetic expression")
    ap.add_argument("-o", "--output", default="out.ll", help="Output .ll path (default: out.ll)")
    ap.add_argument("--retcode", action="store_true",
                    help="Instead of printing, return result (truncated to 32-bit) as process exit code")
    args = ap.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            expr = f.read()
    except OSError as e:
        print(f"error: failed to read {args.input}: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        ir = compile_to_ir(expr, print_result=not args.retcode)
    except SyntaxError as e:
        print(f"syntax error: {e}", file=sys.stderr)
        sys.exit(3)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ir + "\n")
    except OSError as e:
        print(f"error: failed to write {args.output}: {e}", file=sys.stderr)
        sys.exit(4)

    print(f"Wrote LLVM IR to {args.output}")

if __name__ == "__main__":
    main()
