from roll.interpreter import ASTPrinter, ASTInterpreter
from roll.lexer import scan
from roll.parser import Parser

word = "1d4"

tokens = scan(word)
tree = Parser(scan(word)).expr()
print(ASTPrinter().visitExpr(tree))
print(ASTInterpreter().visitExpr(tree))