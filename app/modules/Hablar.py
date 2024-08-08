import pyttsx3


class ttsTalker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('rate', 145)
        self.engine.setProperty('voice', self.voices[2].id)

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

class Talker:
    def __init__(self, talker_cls):
        self.talker_cls = talker_cls

    def talk(self, text):
        self.talker_cls.talk(text)