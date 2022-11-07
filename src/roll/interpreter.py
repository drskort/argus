import random
from datetime import time

from roll.parser import Parser


class ASTPrinter:

    def visitExpr(self, expr):
        if expr.expr is not None:
            expr.expr.accept(self)
            print(f" {expr.operator} ")
        expr.term.accept(self)

    def visitTerm(self, term):
        if term.term is not None:
            term.term.accept(self)
            print(f" {term.operator}")
        term.factor.accept(self)

    def visitFactor(self, factor):
        if factor.atom is not None:
            factor.atom.accept(self)
        else:
            print(f"(")
            factor.expr.accept(self)
            print(f")")

    def visitAtom(self, atom):
        if atom.numberOfDice is not None:
            print(f"{atom.numberOfDice}d{atom.die}")
        else:
            print(f"{atom.number}")


class ASTInterpreter:

    def interpret(self, word):
        random.seed(time.time_ns())
        return self.visitExpr(Parser(word).expr())

    def visitExpr(self, expr):
        if expr.expr is not None:
            if expr.operator == '+':
                left, ltxt = expr.expr.accept(self)
                right, rtxt = expr.term.accept(self)
                return left + right, f"{ltxt} + {rtxt}"
            elif expr.operator == '-':
                left, ltxt = expr.expr.accept(self)
                right, rtxt = expr.term.accept(self)
                return left - right, f"{ltxt} - {rtxt}"
        else:
            return expr.term.accept(self)

    def visitTerm(self, term):
        if term.term is not None:
            if term.operator == '*':
                left, ltxt = term.term.accept(self)
                right, rtxt = term.factor.accept(self)
                return left * right, f"{ltxt} * {rtxt}"
            elif term.operator == '/':
                left, ltxt = term.term.accept(self)
                right, rtxt = term.factor.accept(self)
                return left / right, f"{ltxt} / {rtxt}"
        else:
            return term.factor.accept(self)

    def visitFactor(self, factor):
        if factor.atom is not None:
            return factor.atom.accept(self)
        else:
            res, expr = factor.expr.accept(self)
            return res, f"({expr})"

    def visitAtom(self, atom):
        if atom.numberOfDice is not None:
            throws = 0
            s = 0
            txt = ""
            if atom.numberOfDice > 1:
                txt += "("
            while throws < atom.numberOfDice:
                r = random.randint(1, atom.die)
                s += r
                throws += 1
                txt += f"**{r}**"
                if throws <= atom.numberOfDice - 1:
                    txt += " + "
            if atom.numberOfDice > 1:
                txt += ")"
            return s, txt
        else:
            return atom.number, f"{atom.number}"
