import discord
from discord import app_commands
from discord.ext import commands
import os
import time

import config
import embeds


class ModActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='kick')
    async def kick(self, interaction, member: discord.Member, reason: str):
        if config.moderator_role_id in [role.id for role in interaction.user.roles]:
            try:
                await member.kick(reason=reason)

                embed = discord.Embed(
                    title=f"Member Kicked", description=f"", color=0xFF7500
                )
                embed.add_field(name="Member", value=f'{member.name} (<@{member.id}>)', inline=False)
                embed.add_field(name=f'Mod', value=f'{interaction.user.name} (<@{interaction.user.id}>)')
                embed.add_field(name=f'Reason', value=reason)
                embed.set_footer(text=f'{member.id}')
                await interaction.response.send_message(embed=embed)
                c_id = config.member_log
                c = self.bot.get_channel(c_id)
                await c.send(embed=embed)

                embed = discord.Embed(
                    title=f"You have been kicked from {interaction.guild.name}", description=f"", color=0xFF7500
                )
                embed.add_field(name=f'Mod', value=f'{interaction.user.name} (<@{interaction.user.id}>)')
                embed.add_field(name=f'Reason', value=reason)
                await member.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title=f"Unable to kick member", description=f'{member.name} (<@{member.id}>\nReason: {e})', color=0xFF0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embeds.no_permission_embed, ephemeral=True)

    @app_commands.command(name='ban')
    async def ban(self, interaction, member: discord.Member, reason: str):
        if config.moderator_role_id in [role.id for role in interaction.user.roles]:
            try:
                await member.ban(reason=reason)

                embed = discord.Embed(
                    title=f"Member Banned", description=f"", color=0xFF0000
                )
                embed.add_field(name="Member", value=f'{member.name} (<@{member.id}>)', inline=False)
                embed.add_field(name=f'Mod', value=f'{interaction.user.name} (<@{interaction.user.id}>)')
                embed.add_field(name=f'Reason', value=reason)
                embed.set_footer(text=f'{member.id}')
                await interaction.response.send_message(embed=embed)
                c_id = config.member_log
                c = self.bot.get_channel(c_id)
                await c.send(embed=embed)

                embed = discord.Embed(
                    title=f"You have been **banned** from {interaction.guild.name}", description=f"", color=0xFF7500
                )
                embed.add_field(name=f'Mod', value=f'{interaction.user.name} (<@{interaction.user.id}>)')
                embed.add_field(name=f'Reason', value=reason)
                await member.send(embed=embed)
            except Exception as e:
                embed = discord.Embed(
                    title=f"Unable to ban member", description=f'{member.name} (<@{member.id}>\nReason: {e})', color=0xFF0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embeds.no_permission_embed, ephemeral=True)

    @commands.command(hidden=True)
    @commands.has_role(config.benbot_perms_role_id)
    async def purge(self, ctx, count: int):
        if count > 100:
            await ctx.send('value too large. (max 100)')
        elif count < 1:
            for number in range(1, count):
                await ctx.send('message')
                time.sleep(0.2)
        else:
            await ctx.channel.purge(limit=count + 1)
            channel_id = config.message_log
            channel = self.bot.get_channel(channel_id)
            s = "s"
            if count == 1:
                s = ""
            embed = discord.Embed(title=f'{count} Message{s} Purged')
            embed.add_field(name=f'Sent by', value={ctx.author.user.name})
            await channel.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_role(config.benbot_perms_role_id)
    async def mvvc(self, member: discord.Member, channel: discord.VoiceChannel = None):
        await member.move_to(channel)




async def setup(bot):
    await bot.add_cog(ModActions(bot), guilds=[discord.Object(id=config.server_id)])
