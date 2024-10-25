import discord.member
import discord
from discord.ext import commands
from discord.ext import tasks
import utils.api as api
from cogs.interactions import ModalView1, ModalView2

class BasicCommands(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.bot = client
        self.bot.venue_task = self.started_venues_task
        self.bot._12hr_task = self._12hr_venues_task

    @commands.command(name='synctree')
    @commands.is_owner()
    async def synctree(self, ctx, guild = None):
        if guild == None:
            await self.bot.tree.sync()
        else:
            guild = self.bot.get_guild(1298629168958935092)
            try:
                await self.bot.tree.sync(guild=guild)
            except Exception as e:
                await ctx.send(e)
                return
        await ctx.send("Done!")

    @tasks.loop(minutes=30)
    async def started_venues_task(self):
        started_venues = api.get_started_venues()
        if started_venues == []:
            return
        if not started_venues == []:
            for participants in started_venues:
                #print(participants)
                discordid = int(participants['dId'])
                teamid = int(participants['teamId'])
                usr = self.bot.get_user(discordid)
                d = api.get_msgs(teamid, self.bot)
                #print(d)
                if not d == []:
                    continue
                em = discord.Embed(
                color=0x2F3136,
                description="Please submit your response here!"
                )
                #print('done1')
                msg = await usr.send(embed=em, view=ModalView2(usr))
                #print('done2')
                json_ = {
                    'team_id': teamid,
                    'msg_ids': msg.id,
                    'channel_id': msg.channel.id,
                    'is_second': False
                }
                api.post_to_api_msg(json_)
                #update to api


                #cname = f'venue-{venues['venueId']}'
                #channel:discord.TextChannel = discord.utils.get(c.channels, cname)
                #if channel.last_message:
                #    return
                #await channel.send('hi', view=ModalView(channel))


#automation
    @tasks.loop(minutes=30)
    async def _12hr_venues_task(self):
        _12hr_venues = api.get_4hr_venues()
        if _12hr_venues:
            for participants in _12hr_venues:
                discordid = int(participants['dId'])
                usr = self.bot.get_user(discordid)
                teamid = int(participants['teamId'])
                d = api.is_second(teamid)
                if d:
                    return
                em = discord.Embed(
                color=0x2F3136,
                description="Please submit your response here!"
                )
                msg = await usr.send(embed=em, view=ModalView1(participants))
                json_ = {
                    'team_id': teamid,
                    'msg_ids': msg.id,
                    'channel_id': msg.channel.id,
                    'is_second': True
                }
                api.post_to_api_msg(json_)

                #update to api
                #cname = f'venue-{venues['venueId']}'
                #channel:discord.TextChannel = discord.utils.get(c.channels, cname)
                #if channel.last_message.content == "@everyone Hey its been above 12 hours":
                #    return
                #await channel.send('@everyone Hey its been above 12 hours')

    @commands.command(name = 'startloop')
    @commands.is_owner()
    async def startloop(self, ctx):
        await ctx.send('Loop Started!')
        self.started_venues_task.start()
        


    @commands.command(name='start12hrloop')
    async def start12hrloop(self, ctx):
        try:
            self._12hr_task.start()
            await ctx.send('Loop started')
        except Exception as e:
            await ctx.send(e)

    @commands.command(name = 'stoploop')
    @commands.is_owner()
    async def stoploop(self, ctx):
        await ctx.send('Loop Stopped!')
        self.started_venues_task.stop()

async def setup(client):
    await client.add_cog(BasicCommands(client))