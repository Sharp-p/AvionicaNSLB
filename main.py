import drivers.stubs as stb
import drivers.Driver as td
import thirdParty
import time
from analysis import Analisys


def main() -> None:
    td.openParachute(0)

    analisys = Analisys()

    # Waiting for the lauch, with extra condition on the time based on the simulations
    while analisys.launch_counter < 10:
        time.sleep(0.050)
        analisys.update_log()

    td.printToLog("Partito")
    # Waiting the apogee, with extra condition on the time based on the simulations
    while analisys.return_counter < 10:
        time.sleep(0.050)
        analisys.update_log()

    td.printToLog("Apogeo raggiunto")
    start = time.monotonic()
    # Active wait for the first igniter, while logging
    while time.monotonic() - start < 2:
        time.sleep(0.050)
        analisys.update_log()
    td.openParachute(1)
    start = time.monotonic()
    # Active wait for the second igniter, while logging

    #while time.monotonic() - start < 0.5:
    #    analisys.update_log()


    while analisys.get_deviation() > 0.02:
        time.sleep(0.050)
        analisys.update_log()

main()
