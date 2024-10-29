import discord
import os
import re
import jishaku
from discord.ext import commands
from cogs.interactions import ModalView1, ModalView2

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Green', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is green.', ephemeral=True)

    @discord.ui.button(label='Red', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is red.', ephemeral=True)

    @discord.ui.button(label='Grey', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is grey.', ephemeral=True)



class TestBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('?'),
            intents= discord.Intents.all(),
            owner_ids = [746027434977001513]
        )
        self.tinkerguild = 735180366297563257

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
        print("Starting loops.")
        #self.venue_task.start()
        #self._12hr_task.start()
        print('Loops Started')
        print('Bot ready.')

    async def on_command_error(self, ctx, exception):
        print(exception)

    async def setup_hook(self):
        v1 = ModalView1(self)
        v2 = ModalView2(self)
        self.add_view(v1)
        self.add_view(v2)

