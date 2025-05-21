circuitMode: bool = False
try:
    import drivers.laptopModeSettings as settings
except:
    circuitMode = True
    import drivers.microModeSettings as settings

dirPath: str = settings.dirPath