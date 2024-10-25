import requests
import datetime
import json
import discord

def convertdatetime(string):
    return datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')

#def get_venues():
    #return requests.get('https://app-api.tinkerhub.org/event/635/venues/basic').json()
#    return requests.get('https://app-api.tinkerhub.org/event/team/635').json()
def get_all_participants():
    return requests.get("https://app-api.tinkerhub.org/event/team/635").json()

def get_started_venues():
    json_ = get_all_participants()
    started = []
    for participant in json_:
        startDate = participant['startDate']
        endDate = participant['endDate']
        now = datetime.datetime.now()
        covstrt = convertdatetime(startDate)
        covend = convertdatetime(endDate)
        if now>=covstrt<=covend:
            started.append(participant)
    #e = [
        #{'name': 'Akhil B Xavier', 'userId': 41, 'membershipId': 143, 'avatar': 'https://appbucket-hoomans.s3.ap-south-1.amazonaws.com/1000104093.jpgduplicate.jpg1714410356128322921', 'teamId': 399, 'teamName': "Akhil B Xavier's Team", 'venueId': 25, 'venueName': 'Albertian Institute of Science and Technology (AISAT)', 'startDate': '2024-10-25T02:30:00Z', 'endDate': '2024-10-25T23:30:00Z', 'checkIn': True, 'dId': '869471461545480212', 'projectSubmitted': False},
    #    {
    #        'name': 'Sreeramachandran S Menon', 'dId': '746027434977001513', 'startDate': '2024-10-25T02:30:00Z', 'endDate': '2024-10-25T23:30:00Z', 'venueId': 25,
    #        'teamId': 1, 'teamName': 'eee'
    #    }
    #]
    return e
    return started

def get_4hr_venues():
    started = get_started_venues()
    _12hrs = []
    for venue in started:
        startDate = venue['startDate']
        conv = convertdatetime(startDate)
        current = datetime.datetime.now()
        if current - conv >= datetime.timedelta(hours=7):
            _12hrs.append(venue)

    return _12hrs

def get_member_from_did(did):
    started = get_started_venues()
    for participant in started:
        if participant['dId'] == str(did):
            return participant

def get_team_members(teamid):
    started = get_started_venues()
    list_ = []
    for participant in started:
        if participant['teamId'] == teamid:
            list_.append(participant)
    return list_

class RawMessage(discord.Message):
    def __init__(self, bot, channel_id, message_id):
        self._state = bot._connection
        self.id = message_id
        self.channel = bot.get_channel(channel_id) or discord.Object(channel_id)
    def __repr__(self):
        return 'lazy'

def get_msgs(teamid, bot):
    e = requests.get('http://18.219.158.1/stat/all').json()
    msgs = []
    for d in e:
        team_id = d['team_id']
        if team_id == teamid:
            msgid = d['msg_ids']
            channel_id = d['channel_id']
            msg = RawMessage(bot, channel_id, msgid)
            msgs.append(msg)
    return msgs




def post_to_api_usr(json_):
    jsondata = json.dumps(json_)
    requests.post('http://18.219.158.1/usr_resp/add', jsondata)


def post_to_api_msg(json_):
    jsondata = json.dumps(json_)
    requests.post('http://18.219.158.1/stat/add', jsondata)