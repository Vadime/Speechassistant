import os
import time


class MyNote():

    def __init__(self):
        self.noteOpened = False

    def createNote(self, phrase):
        name = f"/home/vadime/MyNotes/Note_{str(time.time())}_.txt"
        fileObject = open(name, "w")
        fileObject.write(phrase)
        fileObject.close()
        os.system("xed " + name + " &")
        self.noteOpened = True

    def openNote(self):
        path = "/home/vadime/MyNotes/"
        os.system("xed " + os.listdir(path)[0] + " &")
        self.noteOpened = True

    def closeNote(self):
        if self.noteOpened:
            os.system("killall xed")
            self.noteOpened = False
        return self.noteOpened