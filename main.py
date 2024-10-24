from bot import TestBot
import os

bot = TestBot()

@bot.command(name='reload')
async def reloadext(ctx, ext):
    try:
        await bot.reload_extension(ext)
        await ctx.send(f'Reloaded {ext}')
    except Exception as e:
        await ctx.send(e)

token = os.getenv("TOKEN")
bot.run(token)

