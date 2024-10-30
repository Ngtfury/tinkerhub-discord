import discord
from utils import api



class ModalView2(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.stacks = None
        self.challenges = None
        self.knowledgelevel = None

    @discord.ui.select(
        placeholder="Select your teams knowledge level.",
        options=[
            discord.SelectOption(
                label="Beginner",
                value='beginner',
                emoji='🌱'
                ),
            discord.SelectOption(label="Intermediate", value='intermediate', emoji='🎩'),
            discord.SelectOption(label="Advanced", value='advanced', emoji='🤓')
            ],
            custom_id="knowledgelevel"
            )
    async def knowledgelevel(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.knowledgelevel = interaction.data['values'][0]
        await interaction.response.send_message(
            f"You selected your teams knowledge level as {self.knowledgelevel}",
            ephemeral=True,
            delete_after=3
        )
        em = interaction.message.embeds[0].copy()
        stacks = em.fields[1].value
        challenges = em.fields[2].value
        for x in range(len(em.fields)):
            em.remove_field(0)
        em.add_field(name="Knowledge Level", value=strpvalue(self.knowledgelevel.capitalize()))
        em.add_field(name="Stacks you use", value=strpvalue(stacks))
        em.add_field(name="Challenges", value=strpvalue(challenges), inline=False)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=em
        )

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        label="Send Form",
        custom_id="form2",
    )
    async def form_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Update2SubmissionModal(interaction, self))

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit2",
    )
    async def submit_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not (self.challenges and self.knowledgelevel and self.stacks):
            await interaction.response.send_message("Please answer all the questions", ephemeral=True, delete_after=3)
            return
        em = discord.Embed(
            title="🚨 Hey Useless Makers!",
            description="Thank you for submitting your response."
        )

        await interaction.response.edit_message(view=None, embed=em)
        return
        mem = api.get_member_from_did(interaction.user.id)

        teamid = mem['teamId']
        name = mem['name']
        venueid = mem['venueId']
        e = {
            "TeamID": str(teamid),
            "SubmittedBy": name,
            "UpdateType": "Status 2",
            "Content": {
                "Stacks": str(self.stacks),
                "KnowledgeLevel": str(self.knowledgelevel),
                "Challenges": str(self.challenges)
            },
            "venue_id": str(venueid)
        }
        api.post_to_api_msg(e)

class ModalView1(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.projecttype = None
        self.projectname = None
        self.projectdescription = None

    @discord.ui.select(
            options=[
                discord.SelectOption(
                    label="Software",
                    value='software',
                    emoji='💻'
                ),
                discord.SelectOption(
                    label="Hardware",
                    value="hardware",
                    emoji='🔩'
                )
            ],
            placeholder="Select your project type.",
            custom_id="projecttype"
    )
    async def project_type(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.projecttype = interaction.data['values'][0]
        await interaction.response.send_message(
            f"You selected your teams Project Type as {self.projecttype}",
            ephemeral=True,
            delete_after=3
        )
        em = interaction.message.embeds[0].copy()
        projectname = em.fields[1].value
        projectdescription = em.fields[2].value
        for x in range(len(em.fields)):
            em.remove_field(0)
        em.add_field(name="Project Type", value=strpvalue(self.projecttype.capitalize()))
        em.add_field(name="Project Name", value=strpvalue(projectname))
        em.add_field(name="Project Description", value=strpvalue(projectdescription), inline=False)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=em
        )
    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        label="Send Form",
        custom_id="form1",
    )
    async def form_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Update1SubmissionModal(interaction, self))

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit1"
    )
    async def submit_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not (self.projecttype and self.projectdescription and self.projectname):
            await interaction.response.send_message("Please answer all the questions", ephemeral=True, delete_after=3)
            return
        em = discord.Embed(
            title="🚨 Hey Useless Makers!",
            description="Thank you for submitting your response."
        )

        await interaction.response.edit_message(view=None, embed=em)
        return
        mem = api.get_member_from_did(interaction.user.id)

        teamid = mem['teamId']
        name = mem['name']
        venueid = mem['venueId']
        e = {
            "TeamID": str(teamid),
            "SubmittedBy": name,
            "UpdateType": "Status 2",
            "Content": {
                "Project Type": str(self.projecttype),
                "Project Name": str(self.projectname),
                "Project Description": str(self.projectdescription)
            },
            "venue_id": str(venueid)
        }
        api.post_to_api_msg(e)



#submission modals
class Update1SubmissionModal(discord.ui.Modal):
    #teamid = discord.ui.TextInput(
    #    label="Team ID",
    #    style=discord.TextStyle.short,
    #    custom_id="teamid",
    #    placeholder="Share your team id."
    #)
    #venueid = discord.ui.TextInput(
    #    label="Venue ID",
    #    style=discord.TextStyle.short,
    #    custom_id="venueid",
    #    placeholder="Share your venue ID."
    #)
    projectname = discord.ui.TextInput(
        label="Project Name",
        style=discord.TextStyle.short,
        custom_id="projectname",
        placeholder="Share your project name."
    )
    projectdescription = discord.ui.TextInput(
        label="Project Description",
        style=discord.TextStyle.long,
        custom_id="projectdescription",
        placeholder="Share a short description about your project."
    )
    #projecttype = discord.ui.TextInput(
    #    label="Project type",
    #    style=discord.TextStyle.short,
    #    custom_id="projecttype",
    #    placeholder="Select your project type {software/hardware}."
    #)

    def __init__(self, oldinteraction, view) -> None:
        super().__init__(title=f"Submit your response.", custom_id='update1submissionmodal')
        self.oldinteraction = oldinteraction
        self.view = view
    

    async def on_submit(self, interaction: discord.Interaction):
        self.view.projectname = self.projectname
        self.view.projectdescription = self.projectdescription
        em = interaction.message.embeds[0]
        projectype = em.fields[0].value
        for x in range(len(em.fields)):
            em.remove_field(0)
        em.add_field(name="Project Type", value=strpvalue(projectype))
        em.add_field(name="Project Name", value=strpvalue(self.projectname))
        em.add_field(name="Project Description", value=strpvalue(self.projectdescription), inline=False)
        await interaction.response.send_message("Your response has been recorded. Please click submit button after reviewing."
                                                , ephemeral=True,
                                                delete_after=3)
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=em
        )


class Update2SubmissionModal(discord.ui.Modal):
    stacks = discord.ui.TextInput(
        label="Stacks you use.",
        style=discord.TextStyle.short,
        custom_id="stacks",
        placeholder="Share the Stacks/hardware components you used (JS, python, pi)."
    )
#    knowledgelevel = discord.ui.TextInput(
#        label = "Teams current knowledge level",
#        style=discord.TextStyle.short,
#        placeholder="Teams current knowledge level {beginner, intermediate,advanced}",
#        custom_id="knowledgelevel"
#    )
    challenges = discord.ui.TextInput(
        label="Challenge you face.",
        style=discord.TextStyle.long,
        placeholder="Currently any challenges your team face.",
        custom_id="challenges"
    )

    def __init__(self, oldinteraction, view) -> None:
        super().__init__(title=f"Submit your response", custom_id='update2submissionmodal')
        self.oldinteraction = oldinteraction
        #self.teamid = teamid
        #self.teamname = teamname
        #self.venue_id = venue_id
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):

        #e = {
        #    "TeamID": str(self.teamid),
        #    "SubmittedBy": interaction.user.display_name,
        #    "UpdateType": "Status 2",
        #    "Content": {
        #        "Stacks": str(self.stacks),
        #        "KnowledgeLevel": str(self.knowledgelevel),
        #        "Challenges": str(self.challenges)
        #    },
        #    "venue_id": str(self.venue_id)
        #}
        self.view.stacks = self.stacks
        self.view.challenges = self.challenges
        em = interaction.message.embeds[0]
        knowledge = em.fields[0].value
        for x in range(len(em.fields)):
            em.remove_field(0)
        em.add_field(name="Knowledge Level", value=strpvalue(knowledge))
        em.add_field(name="Stacks you use", value=strpvalue(self.stacks))
        em.add_field(name="Challenges", value=strpvalue(self.challenges), inline=False)
        await interaction.response.send_message("Your response has been recorded. Please click submit button after reviewing."
                                                , ephemeral=True,
                                                delete_after=3)
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=em
        )

def strpvalue(value):
    value = str(value)
    if not len(value) > 1024:
        return value
    return value[:1021] + '...'