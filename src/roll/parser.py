from roll.lexer import TokenType
from roll.model import *


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.count = 0

    def expr(self):
        expr = Expr(self.term())
        while self.match({TokenType.PLUS, TokenType.MINUS}):
            if self.previous().type == TokenType.PLUS:
                expr = Expr(expr, '+', self.term())
            elif self.previous().type == TokenType.MINUS:
                expr = Expr(expr, '-', self.term())
        return expr

    def term(self):
        term = Term(self.factor())
        while self.match({TokenType.STAR, TokenType.SLASH}):
            if self.previous().type == TokenType.STAR:
                term = Term(term, '*', self.factor())
            elif self.previous().type == TokenType.SLASH:
                term = Term(term, '/', self.factor())
        return term

    def factor(self):
        if self.match({TokenType.LEFT_BRACKET}):
            expr = self.expr()
            self.consume(TokenType.RIGHT_BRACKET, "Missing ')' after '('")
            return Factor(True, expr)
        else:
            return Factor(False, self.atom())

    def atom(self):
        if self.match({TokenType.D}):
            numberOfDice = 1
            self.consume(TokenType.NUMBER, "Expected the number of sides of the die, like 'd6'")
            die = self.previous().literal
            return Atom(numberOfDice, die)
        self.consume(TokenType.NUMBER, "Expected a number or a die roll")
        if self.check(TokenType.D):
            numberOfDice = self.previous().literal
            self.match({TokenType.D})
            self.consume(TokenType.NUMBER, f"Expected the number of sides of the die, like '{numberOfDice}d6'")
            die = self.previous().literal
            return Atom(numberOfDice, die)
        else:
            return Atom(self.previous().literal)

    def peek(self):
        if (self.count >= len(self.tokens)):
            return None
        return self.tokens[self.count]

    def match(self, types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        else:
            if self.peek() is None:
                raise Exception(f"Missing token at end of formula: {message}")
            else:
                raise Exception(f"Unexpected token {self.peek().lexeme} at position {self.count}: {message}")

    def previous(self):
        return self.tokens[self.count - 1]

    def advance(self):
        self.count += 1
        return self.tokens[self.count - 1]

    def check(self, type):
        if self.count >= len(self.tokens):
            return False
        return self.tokens[self.count].type == type

