from enum import Enum


class TokenType(Enum):
    NUMBER = 1,
    D = 2,
    W = 3,
    PLUS = 4,
    MINUS = 5,
    STAR = 6,
    SLASH = 7,
    LEFT_BRACKET = 8,
    RIGHT_BRACKET = 9


class Token:
    def __init__(self, type, lexeme, literal):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal


def advance(word, count):
    if count >= len(word):
        return None, count + 1
    count += 1
    return word[count - 1], count


def scan(word):
    count = 0
    tokens = []
    while count < len(word):
        c, count = advance(word, count)
        if c == ' ' or c == '\t' or c == '\n':
            pass
        elif c == 'd' or c == 'w':
            tokens.append(Token(TokenType.D, 'd', None))
        elif c == '+':
            tokens.append(Token(TokenType.PLUS, '+', None))
        elif c == '-':
            tokens.append(Token(TokenType.MINUS, '-', None))
        elif c == '*':
            tokens.append(Token(TokenType.STAR, '*', None))
        elif c == '/':
            tokens.append(Token(TokenType.SLASH, '/', None))
        elif c == '(':
            tokens.append(Token(TokenType.LEFT_BRACKET, '(', None))
        elif c == ')':
            tokens.append(Token(TokenType.RIGHT_BRACKET, ')', None))
        elif c.isdigit():
            start = count - 1
            while c is not None and c.isdigit() and count <= len(word):
                c, count = advance(word, count)
            tokens.append(Token(TokenType.NUMBER, word[start:count - 1], int(word[start:count - 1])))
            count -= 1
        else:
            raise Exception(f"Character '{c}' not expected")
    return tokens


result = scan("3 * 6 + 1d4")
