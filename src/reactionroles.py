import codecs
import configparser
import json

from discord.ext import commands
from discord.utils import get

class ReactionRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # Parse config
        config = configparser.ConfigParser()
        with codecs.open('bot.ini', 'r', encoding='utf-8-sig') as f:
            config.read_file(f)
        self.roles = json.loads(config["ReactionRoles"]["roles"])
        self.reactions = json.loads(config["ReactionRoles"]["reactions"])
        self.admin_role = config["ReactionRoles"]["admin_role"]
        self.config = config
        if "role_message_id" in config["ReactionRoles"]:
            self.role_message_id = int(config["ReactionRoles"]["role_message_id"])
        else:
            self.role_message_id = 0

    @commands.command()
    async def roles(self, ctx):
        # Check whether author is the correct role
        if not await self.check_admin(ctx):
            return
        # List roles and their reactions
        txt = "Join a role by using the corresponding reaction on this message: \n"
        for i, role in enumerate(self.roles):
            txt += f"{role}: {self.reactions[i]} \n"
        self.msg = await ctx.send(txt)
        # Update config and id
        self.config["ReactionRoles"]["role_message_id"] = str(self.msg.id)
        with codecs.open('bot.ini', 'w', encoding='utf-8-sig') as f:
            self.config.write(f)
        self.role_message_id = self.msg.id
        # React to the message
        for i, role in enumerate(self.roles):
            await self.msg.add_reaction(self.reactions[i])

    @commands.command()
    async def add_role(self, ctx, role_name):
        # Check whether author is the correct role
        if not await self.check_admin(ctx):
            return
        self.roles.append(role_name)
        self.config["ReactionRoles"]["roles"] = json.dumps(self.roles)
        with codecs.open('bot.ini', 'w', encoding='utf-8-sig') as f:
            self.config.write(f)
        await ctx.send(f"Role '{role_name}' was successfully added")

    @commands.command()
    async def remove_role(self, ctx, role_name):
        # Check whether author is the correct role
        if not await self.check_admin(ctx):
            return
        self.roles.remove(role_name)
        self.config["ReactionRoles"]["roles"] = json.dumps(self.roles)
        with codecs.open('bot.ini', 'w', encoding='utf-8-sig') as f:
            self.config.write(f)
        await ctx.send(f"Role '{role_name}' was successfully removed")


    # Checks whether author has the required role
    async def check_admin(self, ctx):
        for role in ctx.author.roles:
            if role.name == self.admin_role:
                return True
        await ctx.send(f"I am sorry {ctx.author.mention} but you must be a '{self.admin_role}' to invoke this command:")
        return False

    # Adds corresponding role to user
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.role_message_id:
            for i, role_name in enumerate(self.roles):
                if self.reactions[i] == payload.emoji.name:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    role = get(guild.roles, name=role_name)
                    await member.add_roles(role)

    # Removes corresponding role from user
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.role_message_id:
            for i, role_name in enumerate(self.roles):
                if self.reactions[i] == payload.emoji.name:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    role = get(guild.roles, name=role_name)
                    await member.remove_roles(role)