dirPath: str = "/mSD"

#PINs stuff
from digitalio import DigitalInOut as _DigitalInOut, Direction as _Direction
from microcontroller.pin import (GPIO0 as _pyro0Gp, GPIO1 as _pyro1Gp, GPIO9 as _pyroEnGp,
                                 GPIO2 as _sdSckGp, GPIO3 as _sdMosiGp, GPIO4 as _sdMisoGp, GPIO7 as _sdCsGp,
                                 GPIO8 as _speakerGp,
                                 GPIO12 as _bLedGp, GPIO13 as _gLedGp, GPIO14 as _rLedGp,
                                 GPIO22 as _baroCsGp,
                                 GPIO26 as _sensorSckGp, GPIO27 as _sensorMosiGp, GPIO28 as _sensorMisoGp)

pyro0: _DigitalInOut = _DigitalInOut(_pyro0Gp)
pyro0.direction = _Direction.OUTPUT
pyro1: _DigitalInOut = _DigitalInOut(_pyro1Gp)
pyro1.direction = _Direction.OUTPUT
pyroEn: _DigitalInOut = _DigitalInOut(_pyroEnGp)
pyroEn.direction = _Direction.OUTPUT

_speaker: _DigitalInOut = _DigitalInOut(_speakerGp)
_speaker.direction = _Direction.OUTPUT

bLed: _DigitalInOut = _DigitalInOut(_bLedGp)
bLed.direction = _Direction.OUTPUT
gLed: _DigitalInOut = _DigitalInOut(_gLedGp)
gLed.direction = _Direction.OUTPUT
rLed: _DigitalInOut = _DigitalInOut(_rLedGp)
rLed.direction = _Direction.OUTPUT

_baroCs: _DigitalInOut = _DigitalInOut(_baroCsGp)
_baroCs.direction = _Direction.OUTPUT

_sdCs: _DigitalInOut = _DigitalInOut(_sdCsGp)
_sdCs.direction = _Direction.OUTPUT

#devices
from busio import SPI as _SPI
from storage import VfsFat, mount
from thirdParty.adafruit_bmp3xx import BMP3XX_SPI as _BMP
from thirdParty.adafruit_sdcard import SDCard as _SDcard

_sensorSPI: _SPI = _SPI(clock=_sensorSckGp, MISO=_sensorMisoGp, MOSI=_sensorMosiGp)
barometer: _BMP = _BMP(spi=_sensorSPI, cs=_baroCs)

_sdSPI: _SPI = _SPI(clock=_sdSckGp, MISO=_sdMisoGp, MOSI=_sdMosiGp)
_mSD: _SDcard = _SDcard(spi=_sdSPI, cs=_sdCs)
mount(VfsFat(_mSD), dirPath)