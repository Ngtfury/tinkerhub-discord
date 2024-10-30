import discord
from discord.ext import commands
from discord.utils import MISSING
import utils.api as api
from utils.classes import ModalView1, ModalView2


class InteractionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sendmodal')
    @commands.is_owner()
    async def sendmodal(self, ctx, index: int):
        em = discord.Embed(
            color=0x2F3136,
            title="🚨 Hey Useless Makers!",
            description="""Quick check before you build - we need one person from your team to fill this form about your wonderfully useless project!"""
        )
        em.add_field(name="Knowledge Level", value="Please select.")
        em.add_field(name="Stacks you use", value="Please select.")
        em.add_field(name="Challenges", value="Please select.", inline=False)
        em.set_footer(
            text="Please review your submissions before clicking submit.",
        )
        em2 = discord.Embed(
            color=0x2F3136,
            title="🚨 Hey Useless Makers!",
            description="""Quick check before you build - we need one person from your team to fill this form about your wonderfully useless project!"""
        )
        em2.add_field(name='Project Type', value="Please select.")
        em2.add_field(name='Project Name', value="Please select.")
        em2.add_field(name='Project Description', value="Please select.", inline=False)
        em.set_footer(
            text="Please review your submissions before clicking submit.",
        )
        #usr = api.get_member_from_did(user.id)
        if index == 1:
            v = ModalView1(ctx)
            await ctx.send(view = v, embed=em2)
            return
        else:
            await ctx.send(view = ModalView2(ctx), embed=em)
            return



async def setup(client):
    await client.add_cog(InteractionHandler(client))