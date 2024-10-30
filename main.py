
from bot import TestBot
import os
from discord.ext import commands
import discord
import re
from dotenv import load_dotenv
load_dotenv()



# More complicated cases might require parsing state out from the custom_id instead.
# For this use case, the library provides a `DynamicItem` to make this easier.
# The same constraints as above apply to this too.
# For this example, the `template` class parameter is used to give the library a regular
# expression to parse the custom_id with.
# These custom IDs will be in the form of e.g. `button:user:80088516616269824`.


bot = TestBot()

@bot.command(name='reload')
@commands.is_owner()
async def reloadext(ctx, ext):
    try:
        await bot.reload_extension(ext)
        await ctx.send(f'Reloaded {ext}')
    except Exception as e:
        await ctx.send(e)


@bot.command()
@commands.is_owner()
async def prepare(ctx: commands.Context):
    """Starts a persistent view."""
    # In order for a persistent view to be listened to, it needs to be sent to an actual message.
    # Call this method once just to store it somewhere.
    # In a more complicated program you might fetch the message_id from a database for use later.
    # However this is outside of the scope of this simple example.
    await ctx.send("What's your favourite colour?", view=PersistentView())




token = os.getenv("TOKEN")
bot.run(token)

