import discord
from discord import app_commands
from discord.ext import commands
import os
import json
from pathlib import Path

import config


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name='userinfo')
    async def userinfo(self, interaction, user: discord.Member = None):
        if user:
            user = user
        else:
            user = interaction.user

        user_id = user.id
        user_name = user.name
        user_display = user.display_name
        user_avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        user_role_ids = [f"<@&{role.id}>" for role in user.roles if role.name != "@everyone"]
        join_date = user.joined_at
        join_timestamp = round(join_date.timestamp()) if join_date else None


        try:
            with open('', 'r') as file:
                user_warnings = json.load(file)
        except FileNotFoundError:
            user_warnings = {}

        warning_count = user_warnings.get(str(user.id), 0)

        embed = discord.Embed(
            title=user_display, description=user_name, color=0x336EFF
        )
        embed.set_thumbnail(url=user_avatar_url)
        embed.add_field(name="Roles", value=", ".join(user_role_ids) if user_role_ids else "No roles", inline=False)

        target_role_id = config.benbot_perms_role_id
        has_role = any(role.id == target_role_id for role in user.roles)
        if user_id == 1079578703295696917:
            embed.add_field(name="Bot Permissions", value="owner", inline=False)
        elif has_role:
            embed.add_field(name="Bot Permissions", value="admin", inline=False)

        embed.add_field(name="Warnings", value=warning_count, inline=False)
        embed.add_field(name="Join Date", value=f"<t:{join_timestamp}>", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(UserInfo(bot), guilds=[discord.Object(id=config.server_id)])
