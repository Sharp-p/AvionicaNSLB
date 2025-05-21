from drivers.stubs import settings, circuitMode
import io
import sys

if circuitMode:
    settings.rLed.value = True

def openParachute(channel: bool) -> None:
    """
    fire phyro
    :param channel: 0 or 1, the firing channel
    """
    print(f"P{int(channel)}", end="\0")


class Baro:
    """
    interface to the physical bmp 388
    """
    def __init__(self):
        print("S", end="\0")

    def getPressure(self) -> float:
        """

        :return: latest pressure esteeme
        """
        print("G", end='\0')
        buffer = io.StringIO()
        while (x := sys.stdin.read(1)) != '\0':
            buffer.write(x)

        data: str = buffer.getvalue()
        return float(data) / 10

def changeState() -> None:
    """
    when testing communicate to the simulator that the state has changed
    """
    print("C", end="\0")


def printToLog(arg) -> None:
    """
    when testing send a stringable message to the simulator
    :param arg: stuff to print
    """
    print(f"D{str(arg)}", end="\0")


def endFlight() -> None:
    """
    when testing halt simulator
    """
    print("E", end="\0")

def flightReady() -> bool:
    return False

def setLeds(R: bool | None = None, G: bool | None = None, B: bool | None = None):
    if circuitMode:
        if R != None:
            settings.rLed.value = R
        if G != None:
            settings.gLed.value = G
        if B != None:
            settings.bLed.value = B
    else:
        if R != None:
            if R:
                print("LR", end="\0")
            else:
                print("Lr", end="\0")
        if G != None:
            if R:
                print("LG", end="\0")
            else:
                print("Lg", end="\0")
        if B != None:
            if R:
                print("LB", end="\0")
            else:
                print("Lb", end="\0")