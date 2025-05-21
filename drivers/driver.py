from drivers.stubs import settings, circuitMode

if not circuitMode:
    raise Exception("WRONG SETTINGS!\nCan not fly with laptop mode settings")

class Baro:

    def getPressure(self) -> float:
        return settings.barometer.pressure * 100


def openParachute(channel: bool):
    if channel:
        settings.pyro0.value = True
    else:
        settings.pyro1.value = True

def changeState() -> None:
    pass


def printToLog(arg) -> None:
    pass

def endFlight():
    pass

def flightReady() -> bool:
    return True

def setLeds(R: bool | None = None, G: bool | None = None, B: bool | None = None):
    if R != None:
        settings.rLed.value = R
    if G != None:
        settings.gLed.value = G
    if B != None:
        settings.bLed.value = B