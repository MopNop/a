import discord
from discord.ext import commands
import os
import config


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    @commands.has_role(config.benbot_perms_role_id)
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        embed = discord.Embed(title='done.', description=f'synced {len(fmt)} commands')
        await ctx.channel.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Sync(bot), guilds=[discord.Object(id=config.server_id)])
