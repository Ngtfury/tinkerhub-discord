import discord
import os
import jishaku
from discord.ext import commands

class TestBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('?'),
            intents= discord.Intents.all()
        )
        self.tinkerguild = 1298629168958935092

    def load_cache(self):
        self.INITIAL_EXTENSIONS = []
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.INITIAL_EXTENSIONS.append(f'cogs.{filename[:-3]}')

    async def load_extensions(self):
        for x in self.INITIAL_EXTENSIONS:
            await self.load_extension(x)
        await self.load_extension('jishaku')

    async def on_ready(self):
        self.load_cache()
        await self.load_extensions()
        print("Bot ready.")
