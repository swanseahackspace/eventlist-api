import requests
import json
import datetime as dt

### Nicked from https://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (dt.datetime, dt.date, dt.time)):
            return obj.isoformat()
        elif isinstance(obj, dt.timedelta):
            return (dt.datetime.min + obj).time().isoformat()
        return super(DateTimeEncoder, self).default(obj)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def thisWeek():
    nW = getEvents()
    enc = DateTimeEncoder()
    return enc.encode(nW)

def getEvents(gid=218):
    er = requests.get(f'http://opentechcalendar.co.uk/api1/group/{gid}/events.json')
    events = [{'end': dt.datetime.fromtimestamp(x['end']['timestamp']), 'start': dt.datetime.fromtimestamp(x['start']['timestamp']), 'title': x['summary'], 'cancelled': x['cancelled']} for x in er.json()['data'] if not x['deleted']]
    today = dt.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)
    eoW = today + dt.timedelta(days=14)
    nextWeek = [x for x in events if x['start'] >= today and x['end'] < eoW]
    return nextWeek


