from __future__ import print_function
# from googleapiclient.discovery import build
# from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def add_meal_to_google(year, month, day):
    print('entered add meal to google function')
    try:
        print('enters try ')
        import argparse
        flags = (argparse.ArgumentParser(parents=[tools.argparser])).parse_args()
        print('end of try')
    except ImportError:
        flags = None
    print('got past first try except')
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('storage.json')
    creds = store.get()
    print('got past scopes store and creds')
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        if flags:
            creds = tools.run_flow(flow, store, flags)
        else:
            creds = tools.run(flow, store)
    print('got past if not creds ')
    CAL = build('calendar', 'v3', http=creds.authorize(Http()))

    GMT_OFF = '-07:00'
    EVENT = {
        'summary': "doing the other thing",
        'start': {'dateTime': year+"-"+month+"-"+day+'T20:00:00%s' % GMT_OFF},
        'end': {'dateTime': year+"-"+month+"-"+day+'T20:30:00%s' % GMT_OFF},
        'description': 'three eggs, \n pepper, salt, butter, olive oil, beans, cumin, oranges, peanut butter, crushed red pepper, asparagus'

    }
    print('recognized event and it is filled out and ready to be stored')
    e = CAL.events().insert(calendarId='primary', body=EVENT).execute()

    print('''*** %r event added:
        Start: %s
        End: %s''' % (e['summary'].encode('utf-8'),
          e['start']['dateTime'], e['end']['dateTime']))
