import requests
import datetime

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

    return started

def get_4hr_venues():
    started = get_started_venues()
    _12hrs = []
    for venue in started:
        startDate = venue['startDate']
        conv = convertdatetime(startDate)
        current = datetime.datetime.now()
        if current - conv >= datetime.timedelta(hours=4):
            _12hrs.append(venue)

    return _12hrs

