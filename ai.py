import discord
from discord import app_commands
from discord.ext import commands
import os
import io
import config

import torch
import intel_extension_for_pytorch as ipex

from transformers import pipeline
import scipy


if torch.xpu.is_available():
    device = torch.device("xpu")
    print(f"Using Intel XPU: {torch.xpu.current_device()}")
else:
    device = torch.device("cpu")
    print("No Intel XPU found, using CPU.")

synthesizer = pipeline("text-to-audio", "facebook/musicgen-medium")

if isinstance(synthesizer.model, torch.nn.Module):
    synthesizer.model.to(device)
    # 3. IPEX Optimization (After moving to device)
    synthesizer.model = ipex.optimize(synthesizer.model)
else:
    print("Model in pipeline is not a torch.nn.Module, cannot move to device or optimize with IPEX")


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def music(self, content):
        print('t')
        music = synthesizer(f'{content}')
        scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])
        print('a')



async def setup(bot):
    await bot.add_cog(AI(bot), guilds=[discord.Object(id=config.server_id)])
