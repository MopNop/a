import discord
from discord.ext import commands
import os
import time
import random
from discord import app_commands

import config



class RoleChange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(brief="changes the microplastic role color", hidden=True)
    @commands.has_role(1203916156734546000)
    async def rolecolor(self, ctx, color: discord.Color):
        role = discord.utils.get(ctx.guild.roles, id=1203916156734546000)
        await role.edit(color=color)
        await ctx.send(f'set role color to {color}')

    @app_commands.command(name='rolecolor', description='changes the microplastics role color')
    async def rolecolorcommand(self, interaction, color: str):
        if interaction.user.id == 908502791373336617:
            try:
                color = discord.Color(int(color, base=16))  # Convert hex string to integer
                role = discord.utils.get(interaction.guild.roles, id=1203916156734546000)
                await role.edit(color=color)
                await interaction.response.send_message(f"Set role color to {color}")
            except ValueError:
                await interaction.response.send_message("Invalid color format. Please provide a valid hexadecimal color code (e.g., #RRGGBB).")
        else:
            await interaction.response.send_message(f"you cannot use this command")


async def setup(bot):
    await bot.add_cog(RoleChange(bot), guilds=[discord.Object(id=config.server_id)])
