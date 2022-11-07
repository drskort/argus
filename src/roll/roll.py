from random import random

from discord.ext import commands

from roll.interpreter import ASTInterpreter, ASTPrinter
from roll.parser import Parser
from roll.lexer import scan


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def roll(self, ctx, *, formula):
        result, expr = ASTInterpreter().visitExpr(Parser(scan(formula)).expr())
        await ctx.channel.send(f"{expr} = {result}")

    @commands.command()
    async def rolls(self, ctx, *, formula):
        result, expr = ASTInterpreter().visitExpr(Parser(scan(formula)).expr())
        await ctx.channel.send(result)

