import discord




class ModalView1(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.select(
        placeholder="Select your teams knowledge level.",
        options=[
            discord.SelectOption(
                label="Beginner",
                value='beginner'
                ),
            discord.SelectOption(label="Intermediate", value='intermediate'),
            discord.SelectOption(label="Advanced", value='advanced')
            ],
            custom_id="knowledgelevel"
            )
    async def knowledgelevel(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.knowledgelevel = interaction.data['values'][0]
        await interaction.response.send_message(
            f"You selected your teams knowledge level as {self.knowledgelevel}",
            ephemeral=True
        )
        em = interaction.message.embeds[0].copy()
        stacks = em.fields[1].value
        challenges = em.fields[2].value
        for x in range(len(em.fields)):
            em.remove_field(0)
        em.add_field(name="Knowledge Level", value=self.knowledgelevel.capitalize())
        em.add_field(name="Stacks you use", value=stacks)
        em.add_field(name="Challenges", value=challenges)

        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=em
        )

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        label="Send Form",
        custom_id="form",
    )
    async def form_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Update2SubmissionModal(interaction, self))

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit1",
    )
    async def submit_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=None)

class ModalView2(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        label="Submit",
        custom_id="submit2"
    )
    async def submit_bttn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Update1SubmissionModal(interaction, self.bot))



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

    def __init__(self, oldinteraction, bot) -> None:
        super().__init__(title=f"Submit your response.", custom_id='update1submissionmodal')
        self.oldinteraction = oldinteraction
        self.bot = bot
    

    async def on_submit(self, interaction: discord.Interaction):


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
        await interaction.response.send_message('hi')
        self.stop()
        #await interaction.response.edit_message(embed=em1, view=v)
        return
        #edit other user messages
        mem = api.get_member_from_did(interaction.user.id)
        teamid = mem['teamId']
        venueid = mem['venueId']
        e = {
            "TeamID": str(teamid),
            "SubmittedBy": interaction.user.display_name,
            "UpdateType": "Status 2",
            "Content": {
                "Stacks": str(self.stacks),
                "KnowledgeLevel": str(self.knowledgelevel),
                "Challenges": str(self.challenges)
            },
            "venue_id": str(venueid)
        }
        #edit other user messages
        msgs = api.get_msgs(self.teamid, self.bot)
        api.post_to_api_usr(e)
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
        em.add_field(name="Knowledge Level", value=knowledge)
        em.add_field(name="Stacks you use", value=self.stacks)
        em.add_field(name="Challenges", value=self.challenges)
        await interaction.response.send_message("Your response has been recorded. Please click submit button after reviewing."
                                                , ephemeral=True)
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=em
        )
