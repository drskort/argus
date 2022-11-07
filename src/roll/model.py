class Expr:
    def __init__(self, *args):
        if len(args) > 1:
            self.expr = args[0]
            self.operator = args[1]
            self.term = args[2]
        else:
            self.expr = None
            self.operator = None
            self.term = args[0]

    def accept(self, visitor):
        return visitor.visitExpr(self)


class Term:
    def __init__(self, *args):
        if len(args) > 1:
            self.term = args[0]
            self.operator = args[1]
            self.factor = args[2]
        else:
            self.term = None
            self.operator = None
            self.factor = args[0]

    def accept(self, visitor):
        return visitor.visitTerm(self)


class Factor:
    def __init__(self, is_expression, value):
        if is_expression:
            self.atom = None
            self.expr = value
        else:
            self.expr = None
            self.atom = value

    def accept(self, visitor):
        return visitor.visitFactor(self)


class Atom:
    def __init__(self, *args):
        if len(args) > 1:
            self.number = None
            self.numberOfDice = args[0]
            self.die = args[1]
        else:
            self.numberOfDice = None
            self.die = None
            self.number = args[0]

    def accept(self, visitor):
        return visitor.visitAtom(self)


