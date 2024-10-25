from bot import TestBot
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

bot = TestBot()

@bot.command(name='reload')
@commands.is_owner()
async def reloadext(ctx, ext):
    try:
        await bot.reload_extension(ext)
        await ctx.send(f'Reloaded {ext}')
    except Exception as e:
        await ctx.send(e)

token = os.getenv("TOKEN")
bot.run(token)

