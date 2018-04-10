from pygame import mixer
import Config
mixer.init()

Test = mixer.Sound(Config.testSound)
TestChan = mixer.Channel(2)
if Config.music:
    BackChan = mixer.Channel(1)
    Background = mixer.Sound(Config.backgroundMusic, loop=-1)
    BackChan.play(Background)


def test():
    TestChan.play(Test)
