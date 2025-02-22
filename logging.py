import discord
from discord.ext import commands
import os
import datetime
import config



def get_permission_changes(before_overwrites, after_overwrites):
    """
    This function compares permission overwrites for two dictionaries and
    returns a list of permission changes.
    """
    changes = []
    for role, before_overwrite in before_overwrites.items():
        after_overwrite = after_overwrites.get(role)
        if not after_overwrite:
            # Role removed, permission denied
            changes.append(f"**Role Removed:** {role.name} (Permissions Denied)")
            continue
        for permission in discord.Permissions:
            if before_overwrite.allow & permission != after_overwrite.allow & permission:
                # Permission changed (allowed/denied)
                if before_overwrite.allow & permission:
                    change = f"**Permission Lost:** {role.name} - {permission.name}"
                else:
                    change = f"**Permission Gained:** {role.name} - {permission.name}"
                changes.append(change)
    for role, after_overwrite in after_overwrites.items():
        if not before_overwrites.get(role):
            # Role added, permission granted by default
            changes.append(f"**Role Added:** {role.name} (Default Permissions)")
    return changes


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel_id = config.message_log
        channel = self.bot.get_channel(channel_id)
        if after.author.id != self.bot.user.id:
            if before.content != after.content:
                embed = discord.Embed(title="Message Edited", description=f"Channel: {after.channel}", color=0xD8E941)
                embed.set_author(name=before.author.name, icon_url=after.author.avatar.url if after.author.avatar else after.author.default_avatar.url)
                embed.add_field(name='Before', value=before.content, inline=False)
                embed.add_field(name='After', value=after.content, inline=True)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        message = payload.cached_message
        channel_id = config.message_log
        channel = self.bot.get_channel(channel_id)

        mchannel_name = str(message.channel.name)

        if message.author.id != self.bot.user.id:
            if message.attachments:
                urls = [attachment.url for attachment in message.attachments]
                embed = discord.Embed(title="Message Deleted", description=f"{message.content} & images", color=0xB80000)
                embed.add_field(name="Channel:", value={mchannel_name})
                embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                await channel.send(embed=embed)
                await channel.send(urls)
            else:
                embed = discord.Embed(title="Message Deleted", description=f"{message.content}", color=0xB80000)
                embed.add_field(name="Channel", value=f"{mchannel_name}")
                embed.set_author(name=message.author.name, icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
                await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        c_id = config.server_log  # server logging channel
        ch = self.bot.get_channel(c_id)

        now = datetime.datetime.now()
        formatted_time = now.strftime("%m/%d/%Y | %H:%M:%S")

        embed = discord.Embed(title="Channel Updated", description=f"Channel: {before.name}")
        changes = {
            "name": (lambda c: c.name, lambda c: c.name),
            "Type": (lambda c: c.type, lambda c: c.type),
            "Topic": (lambda c: c.topic if c.type == discord.TextChannel else None,
                      lambda c: c.topic if c.type == discord.VoiceChannel else None,
                      lambda values: f"Before: {values[0]} \nAfter: {values[1]}"),
            "Position": (lambda c: c.position, lambda c: c.position),
            "Slowmode": (lambda c: c.slowmode_delay, lambda c: c.slowmode_delay,
                         lambda values: f"Before: {values[0]} seconds\nAfter: {values[1]} seconds"),
        }

        def format_change(b, a):
            return f"Before: {b}\nAfter: {a}"

        for name, (before_func, after_func) in changes.items():
            before_value = before_func(before)
            after_value = after_func(after)
            if before_value != after_value:
                embed.add_field(name=name, value=format_change(before_value, after_value), inline=False)

        embed.set_footer(text=f"{formatted_time}")
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Member Joined", description=f'{member.nick} ({member.name})')
        embed.add_field(name="Joined at", value=f'<t:{int(member.joined_at.timestamp())}>')
        embed.add_field(name="Account Created at", value=f'<t:{int(member.created_at.timestamp())}>')
        c_id = config.member_log
        ch = self.bot.get_channel(c_id)
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title="Channel Created", description=f'{channel.name}')
        c_id = config.server_log
        ch = self.bot.get_channel(c_id)
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title="Channel Removed", description=f'{channel.name}')
        c_id = config.server_log
        ch = self.bot.get_channel(c_id)
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Member Left", description=f'{member.nick} ({member.name})')
        embed.add_field(name="Joined at", value=f'<t:{int(member.joined_at.timestamp())}>')
        embed.add_field(name="Account Created at", value=f'<t:{int(member.created_at.timestamp())}>')
        c_id = config.member_log
        ch = self.bot.get_channel(c_id)
        await ch.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_emoji_update(self, em):
        if em.before != em.after:
            c_id = config.server_log
            ch = self.bot.get_channel(c_id)
            await ch.send(f"before: {em.before}\nafter: {em.after}")


async def setup(bot):
    await bot.add_cog(Logging(bot), guilds=[discord.Object(id=config.server_id)])
