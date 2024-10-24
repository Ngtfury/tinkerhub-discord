import discord
from discord.ext import commands
from discord.utils import MISSING

class ModalView1(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit1"
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
            if custom_id == 'submit1':
                await interaction.response.send_modal(Update1SubmissionModal(interaction))
            else:
                await interaction.response.send_modal(Update2SubmissionModal(interaction))
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

    def __init__(self, oldinteraction, teamid = None) -> None:
        super().__init__(title="Submit your response.", custom_id='update1submissionmodal')
        self.oldinteraction = oldinteraction
        self.teamid = teamid
    

    async def on_submit(self, interaction: discord.Interaction):

        e = {
            "TeamID": str(self.teamid),
            "SubmittedBy": interaction.user.display_name,
            "UpdateType": "Status 1",
            "Content": {
                "ProjectName": str(self.projectname),
                "ProjectDescription": str(self.projectdescription),
                "ProjectType": str(self.projecttype)
            }
        }

        #update to api
        await interaction.response.send_message(str(e))
        #edit original response to submitted
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
        await self.oldinteraction.edit_original_response(
            embed=em,
            view = v
            
        )

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

    def __init__(self, oldinteraction, teamid = None) -> None:
        super().__init__(title="Submit your response.", custom_id='update2submissionmodal')
        self.oldinteraction = oldinteraction
        self.teamid = teamid

    async def on_submit(self, interaction: discord.Interaction):

        e = {
            "TeamID": str(self.teamid),
            "SubmittedBy": interaction.user.display_name,
            "UpdateType": "Status 1",
            "Content": {
                "Stacks": str(self.stacks),
                "KnowledgeLevel": str(self.knowledgelevel),
                "Challenges": str(self.challenges)
            }
        }
        #post to api
        #await interaction.response.send_message(str(e))
        #edit original response to submitted
        await self.oldinteraction.edit_original_response(view=None)

async def setup(client):
    await client.add_cog(InteractionHandler(client))