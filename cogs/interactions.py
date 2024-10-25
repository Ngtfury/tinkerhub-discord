import discord
from discord.ext import commands
from discord.utils import MISSING
import utils.api as api


class ModalView1(discord.ui.View):
    def __init__(self, mem):
        super().__init__(timeout=None)
        self.mem = mem

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit1",
    )
    async def submit_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        return
    
class ModalView2(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit2"
    )
    async def submit_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        return

class InteractionHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sendmodal')
    @commands.is_owner()
    async def sendmodal(self, ctx, index: int):
        em = discord.Embed(
            color=0x2F3136,
            description="Please submit your response here!"
        )
        if index == 1:
            await ctx.send(view = ModalView1(ctx), embed=em)
            return
        else:
            await ctx.send(view = ModalView2(ctx), embed=em)
            return

    @commands.Cog.listener('on_interaction')
    async def modal_submit(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.modal_submit:
            return

        if not interaction.response.is_done():
            custom_id = interaction.message.components[0].children[0].custom_id
            mem = api.get_member_from_did(interaction.user.id)
            if not mem:
                #disable button
                await interaction.response.edit_message(view=None)
                return
            if custom_id == 'submit1':
                await interaction.response.send_modal(Update2SubmissionModal(interaction, self.bot, mem['teamId'], mem['teamName'], mem['venueId']))
            else:
                await interaction.response.send_modal(Update1SubmissionModal(interaction, self.bot, mem['teamId'], mem['teamName'], mem['venueId']))
            return


#submission modals
class Update1SubmissionModal(discord.ui.Modal):
    projectname = discord.ui.TextInput(
        label="Project Name",
        style=discord.TextStyle.short,
        custom_id="projectname",
        placeholder="Share your project name."
    )
    projectdescription = discord.ui.TextInput(
        label="Description",
        style=discord.TextStyle.long,
        custom_id="projectdescription",
        placeholder="Share a short description about your project."
    )
    projecttype = discord.ui.TextInput(
        label="Project type",
        style=discord.TextStyle.short,
        custom_id="projecttype",
        placeholder="Select your project type {software/hardware}."
    )

    def __init__(self, oldinteraction, bot, teamid, teamname, venue_id) -> None:
        super().__init__(title=f"Submit your response.", custom_id='update1submissionmodal')
        self.oldinteraction = oldinteraction
        self.teamid = teamid
        self.bot = bot
        self.venue_id = venue_id
    

    async def on_submit(self, interaction: discord.Interaction):

        e = {
            "TeamID": str(self.teamid),
            "SubmittedBy": interaction.user.display_name,
            "UpdateType": "Status 1",
            "Content": {
                "ProjectName": str(self.projectname),
                "ProjectDescription": str(self.projectdescription),
                "ProjectType": str(self.projecttype)
            },
            "venue_id": str(self.venue_id)
        }

        api.post_to_api_usr(e)
        em1 = discord.Embed(
            color=0x2F3136,
            description=f"""Hey Maker, {self.oldinteraction.user.mention}
Your shared your latest team update now! 🫰 
Keep building"""
        )
        em = discord.Embed(
            color=0x2F3136,
            description=f"""Hey Maker, {self.oldinteraction.user.mention}
Your team member already shared your latest team update 🫰 
Keep building"""
        )
        v = discord.ui.View()
        v.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.gray,
                disabled=True,
                label="Submitted"
            )
        )
        await interaction.response.edit_message(embed=em1, view=v)
        #edit other user messages
        msgs = api.get_msgs(self.teamid, self.bot)
        if msgs:
            for msg in msgs:
                #await msg.edit(embed=em, view=v)
                await msg.delete()
        #edit original response to submitted

        #await self.oldinteraction.edit_original_response(
        #    embed=em,
        #    view = v
        #    
        #)

class Update2SubmissionModal(discord.ui.Modal):
    stacks = discord.ui.TextInput(
        label="Stacks you use.",
        style=discord.TextStyle.short,
        custom_id="stacks",
        placeholder="Share the Stacks/hardware components you used (JS, python, pi)."
    )
    knowledgelevel = discord.ui.TextInput(
        label = "Teams current knowledge level",
        style=discord.TextStyle.short,
        placeholder="Teams current knowledge level {beginner, intermediate,advanced}",
        custom_id="knowledgelevel"
    )
    challenges = discord.ui.TextInput(
        label="Challenge you face.",
        style=discord.TextStyle.long,
        placeholder="Currently any challenges your team face.",
        custom_id="challenges"
    )

    def __init__(self, oldinteraction, bot, teamid, teamname, venue_id) -> None:
        super().__init__(title=f"Submit your response", custom_id='update2submissionmodal')
        self.oldinteraction = oldinteraction
        self.teamid = teamid
        self.teamname = teamname
        self.venue_id = venue_id
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):

        e = {
            "TeamID": str(self.teamid),
            "SubmittedBy": interaction.user.display_name,
            "UpdateType": "Status 2",
            "Content": {
                "Stacks": str(self.stacks),
                "KnowledgeLevel": str(self.knowledgelevel),
                "Challenges": str(self.challenges)
            },
            "venue_id": str(self.venue_id)
        }
        api.post_to_api_usr(e)
        #await interaction.response.send_message(str(e))
        #edit original response to submitted
        em1 = discord.Embed(
            color=0x2F3136,
            description=f"""Hey Maker, {self.oldinteraction.user.mention}
Your shared your latest team update now! 🫰 
Keep building"""
        )
        em = discord.Embed(
            color=0x2F3136,
            description=f"""Hey Maker, {self.oldinteraction.user.mention}
Your team member already shared your latest team update 🫰 
Keep building"""
        )
        v = discord.ui.View()
        v.add_item(
            discord.ui.Button(
                style=discord.ButtonStyle.gray,
                disabled=True,
                label="Submitted"
            )
        )
        await interaction.response.edit_message(embed=em1, view=v)
        #edit other user messages
        msgs = api.get_msgs(self.teamid, self.bot)
        if msgs:
            for msg in msgs:
                #await msg.edit(embed=em, view=v)
                await msg.delete()

async def setup(client):
    await client.add_cog(InteractionHandler(client))