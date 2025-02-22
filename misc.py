import discord
from discord import app_commands
from discord.ext import commands
import os
import embeds
import config


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name='say')
    async def say(self, interaction, message: str, reply_message_id: str = None):
        c_id = interaction.channel.id
        c = self.bot.get_channel(c_id)

        async def execute():
            await c.send(message)

        if config.benbot_perms_role_id in [role.id for role in interaction.user.roles]:
            if reply_message_id:
                try:
                    msg = await c.fetch_message(int(reply_message_id))
                    await msg.reply(content=message)
                    await interaction.response.send_message('whoosh', ephemeral=True)

                except:
                    await execute()
                    await interaction.response.send_message('whoosh\n-# the message ID could not be found, and was ignored', ephemeral=True)
            else:
                await execute()
                await interaction.response.send_message('whoosh', ephemeral=True)

            embed = discord.Embed(title=f"{interaction.user.name} used /say in <#{c.id}>", description=f"", color=0xFF0000)
            embed.add_field(name="Contents:", value=message)
            c_id = config.message_log
            c = self.bot.get_channel(c_id)
            await c.send(embed=embed)
        else:
            await interaction.response.send_message(embed=embeds.no_permission_embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Misc(bot), guilds=[discord.Object(id=config.server_id)])
