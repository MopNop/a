import discord
from discord import app_commands
from discord.ext import commands
import os

import config

def rulelist(rule):
    rlist = [
        discord.Embed(title="Rule 1",
                      description="This is a community Discord server, and all of the community guidelines apply here"),
        discord.Embed(title="Rule 2",
                      description="**Be respectful**\nNo discrimination, hateful language, disparaging of others, or inappropriate content. Do not be rude to other server members or server staff. We do not tolerate offensive comments related to gender, gender identity and expression, sexual orientation, disability, mental illness, race, age, etc."),
        discord.Embed(title="Rule 3",
                      description="**Do not spam or cause disruption**\nNo discrimination, hateful language, disparaging of others, or inappropriate content. Do not be rude to other server members or server staff. We do not tolerate offensive comments related to gender, gender identity and expression, sexual orientation, disability, mental illness, race, age, etc."),
        discord.Embed(title="Rule 4",
                      description="**Avoid scams or deceitful practices**\nDo not send phishing, scam links, or false reports against other users or servers. Impersonation of any staff member is not allowed."),
        discord.Embed(title="Rule 5",
                      description="**Do not bypass filters or evade punishments**\nIntentionally bypassing our filters or moderation actions is not allowed. Alternative accounts are not allowed."),
        discord.Embed(title="Rule 6",
                      description="**Do not post false or misleading information**\nDo not post demonstrably false or misleading information, especially that which may impact public safety or cause harm."),
        discord.Embed(title="Rule 7",
                      description="**NSFW**\nNSFW content is not allowed under any circumstances. We don't want to see it"),
        discord.Embed(title="Logging", description="We have a logging bot that logs messages and content"),
        discord.Embed(title="Reporting issues",
                      description="If there is anything that needs to be reported or if you have any questions, feel free to ping <@&1187528310058663956>\n\nPlease have a valid reason.\n\nRepeatedly pinging users or roles will result in a mute, and a ban if continued.\n\nAdmins have the right to take action at their discretion even if it's not stated in the rules.\nIf you have an issue with this, you can DM <@639281094889570323>")
    ]
    return rlist[rule]


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rule")
    @app_commands.choices(rules=[
        app_commands.Choice(name="Rule 1", value=1),
        app_commands.Choice(name="Rule 2", value=2),
        app_commands.Choice(name="Rule 3", value=3),
        app_commands.Choice(name="Rule 4", value=4),
        app_commands.Choice(name="Rule 5", value=5),
        app_commands.Choice(name="Rule 6", value=6),
        app_commands.Choice(name="Rule 7", value=7),
        app_commands.Choice(name="Logging", value=8),
        app_commands.Choice(name="Reporting Issues", value=9),
        app_commands.Choice(name="rule 78", value=10)
    ])
    async def rule(self, interaction, rules: app_commands.Choice[int]):
        try:
            if rules.value == 10:
                await interaction.response.send_message("https://tenor.com/view/rule-rule78-toast-jumpscare-rules-gif-22292883")
            else:
                out = rulelist(rule=rules.value-1)
                await interaction.response.send_message(embed=out)
        except Exception as e:
            await interaction.response.send_message(f":(\n{rules}\n{e}")


async def setup(bot):
    await bot.add_cog(Rules(bot), guilds=[discord.Object(id=config.server_id)])
