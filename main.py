import os
import speech_recognition as sr
import mycalendar
import myweather
import mynotes
from gtts import gTTS
import playsound
import time
import random


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = 'res/voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    print("[Assistant]:", text, "\n")


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        said = ""
        try:
            said = r.recognize_google(r.listen(source)).lower()
            print("[Vadime]:", said, "\n")
        except Exception as e:
            print("[Vadime-Exception]:", str(e), "\n")
    return said


def openProgram(user_call):
    call = user_call + ".desktop"
    files = os.listdir(path)
    filefound = False
    for file in files:
        if file == call:
            filefound = True
            f = open(path + call)
            for line in f:
                if line.startswith("Exec="):
                    os.system(line.split("=")[1])
                    speak("Opening " + user_call)
                    break
            break
    if not filefound:
        print("File not found!\nAll files:\n", files)


def getNote(n, NOTE_____STRS, phrase):
    if "open latest note" in phrase:
        n.openNote()
        speak("Latest Note opened")
        pass
    for p in NOTE_____STRS:
        if p in phrase:
            speak("What should I write ? ")
            n.createNote(get_audio())
            speak("got it")


def closeNote(n, phrase):
    if "close note" in phrase:
        if not n.closeNote():
            speak("Note closed")


def getCalendar(c, CALENDAR_STRS, phrase):
    for p in CALENDAR_STRS:
        if p in phrase:
            speak(c.get_events(phrase))


def getWeather(w, WEATHER__STRS, phrase):
    for p in WEATHER__STRS:
        if p in phrase:
            speak(w.get_standardWeather("Apolda", "DE"))


def chatBot(GREETINGS, RESPONSES, phrase):
    if "beautiful" in phrase:
        speak("Bitch please, I know. This Body is not for your eyes")
    for i in range(0, len(GREETINGS)):
        g = GREETINGS[i]
        if g in phrase:
            speak(RESPONSES[i])


if __name__ == "__main__":
    WAKE = "sam"
    WAKE_RESP = ["yes", "yeah", "go ahead"]
    path = "/usr/share/applications/"
    CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
    WEATHER__STRS = ["tell me the weather", "what's the weather like"]
    CRT_NOTE_STRS = ["make a note", "create a note"]
    GREETINGS = ["hey", "how you doing", "what up", "how's it going"]
    RESPONSES = ["hey", "chilling bro", "i'm fine",
                 "You gotta do, what you gotta do"]
    THANKS_ANSWERS = ["You're welcome", "No problem", "No worries", "Don't mention it",
                      "My pleasure", "Anyime", "It was the least i could do", "Glad to help"]
    c = mycalendar.MyCalendar()
    w = myweather.MyWeather()
    n = mynotes.MyNote(),

    speak("Program started")
    while True:
        phrase = get_audio()
        if phrase.count(WAKE) > 0:
            speak(WAKE_RESP[random.randint(0, len(WAKE_RESP)-1)])
            phrase = get_audio()
            getNote(n, CRT_NOTE_STRS, phrase)
            getCalendar(c, CALENDAR_STRS, phrase)
            getWeather(w, WEATHER__STRS, phrase)
            closeNote(n, phrase)
            chatBot(GREETINGS, RESPONSES, phrase)
        if "thanks" in phrase:
            speak(THANKS_ANSWERS[random.randint(0, len(THANKS_ANSWERS) - 1)])
