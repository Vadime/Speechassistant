from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pytz


class MyCalendar():

    def __init__(self):
        creds = None
        if os.path.exists('res/token.pickle'):
            with open('res/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'res/credentials.json', ['https://www.googleapis.com/auth/calendar.readonly'])
                creds = flow.run_local_server(port=0)

            with open('res/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)
        self.MONTHS = ["january", "february", "march", "april", "may", "june",
                       "july", "august", "september", "october", "november", "december"]
        self.DAYS = ["monday", "tuesday", "wednesday",
                     "thursday", "friday", "saturday", "sunday"]
        self.DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
        self.EXTRA_DAYS=["today", "tomorrow"]

    def get_events(self, phrase):
        day = self.get_date(phrase)
        if not day: return "I hate you"
        date = datetime.datetime.combine(day, datetime.datetime.min.time())
        end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
        utc = pytz.UTC
        date = date.astimezone(utc)
        end_date = end_date.astimezone(utc)

        events_result = self.service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                                   singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return 'No upcoming events found.'
        else:
            answer = ""
            if len(events) == 1:
                answer += "One event found."
            else:
                answer += str(len(events)) + " events found."
            for i in range(0, len(events)):
                event = events[i]
                start = event['start'].get(
                    'dateTime', event['start'].get('date'))
                if "T" not in start:
                    answer += " You have " + \
                        event["summary"] + ", the hole day."
                else:
                    # get rid of the date, just get the time
                    start = str(start.split("T")[1].split("-")[0])
                    # get rid of the +1:00 or something
                    start = str(start.split("+")[0])
                    # get rid of the seconds
                    start_time = str(start.split(
                        ":")[0] + ":" + start.split(":")[1])
                    if int(start_time.split(":")[0]) < 12:
                        start_time = start_time + " am"
                    else:
                        start_time = str(int(start_time.split(":")[0])-12)
                        start_time = start_time + " pm"
                    if len(events) > 1 and i == len(events) - 1:
                        answer += " and"
                    answer += " " + event["summary"] + \
                        " at " + start_time + "."
            return answer

    def get_date(self, text):
        text = text
        today = datetime.date.today()

        if text.count("today") > 0:
            return today
        if text.count("tomorrow") > 0:
            return datetime.date.today() + datetime.timedelta(days=1)

        day = -1
        day_of_week = -1
        month = -1
        year = today.year

        for word in text.split():
            if word in self.MONTHS:
                month = self.MONTHS.index(word) + 1
            elif word in self.DAYS:
                day_of_week = self.DAYS.index(word)
            elif word.isdigit():
                day = int(word)
            else:
                for ext in self.DAY_EXTENTIONS:
                    found = word.find(ext)
                    if found > 0:
                        try:
                            day = int(word[:found])
                        except:
                            pass

        if month < today.month and month != -1:
            year = year+1

        if month == -1 and day != -1:
            if day < today.day:
                month = today.month + 1
            else:
                month = today.month

        if month == -1 and day == -1 and day_of_week != -1:
            current_day_of_week = today.weekday()
            dif = day_of_week - current_day_of_week

            if dif < 0:
                dif += 7
                if text.count("next") >= 1:
                    dif += 7

            return today + datetime.timedelta(dif)

        if day != -1:
            return datetime.date(month=month, day=day, year=year)
