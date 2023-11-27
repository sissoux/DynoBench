import board
import digitalio
import time
import analogio
import storage

_cal_ADCVRef = 3.01

class analogMeasurement():
    def __init__(self, pin:board.A0, gain) -> None:
        pass

    def calibrateOffset(self):
        pass

def autoZero(ADC:analogio.AnalogIn, averaging = 100, aperture = 0.01, verbose=False):
    cntr  = 0
    val = 0
    while cntr < averaging:
        val += ADC.value
        time.sleep(aperture)
        cntr+=1
        if verbose: print(f"{cntr}\r")
    if verbose: print(f"AutoZero value = {val/averaging}")
    return val/averaging

def getAverage(ADC:analogio.AnalogIn, averaging = 50, aperture = 0.01, verbose=False):
    cntr  = 0
    val = 0
    while cntr < averaging:
        val += ADC.value
        time.sleep(aperture)
        cntr+=1
    return val/averaging

def getADC(ADC:analogio.AnalogIn, gain=1.0, offset=0.0, averaging = 50, aperture = 0.01):
    if averaging !=0 :
        val = (getAverage(ADC, averaging, aperture)-offset)*_cal_ADCVRef/65535.0*gain
    else:
        val = (ADC.value-offset)*_cal_ADCVRef/65535.0*gain
    return val


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

PFMPin = digitalio.DigitalInOut(board.SMPS_MODE)
PFMPin.direction =  digitalio.Direction.OUTPUT
PFMPin.value = 1



currentGain = 1/8.8e-3 #mV/A

def StartLog(timeout:float):
    led.value = 1
    tstart = time.monotonic()
    print(f"Starting acquisition for {timeout}s.")

    while (time.monotonic() - tstart) < timeout:
        led.value = not led.value

        currentValue = getADC(I_input, gain=currentGain, offset=CurrentOffset, averaging=0, aperture=10e-3 )
        VBattery = getADC(Vbat, gain=1, offset=0, averaging=10, aperture=10e-3 )
        print(f"{time.monotonic()-tstart},{currentValue:0.6f},{VBattery:0.6f}")
        time.sleep(0.01)
    print("Finished acquisition.")
    led.value = 0




I_input = analogio.AnalogIn(board.A1)
Vbat = analogio.AnalogIn(board.A2)

print("Getting ILoad offset.")
CurrentOffset = autoZero(I_input)

while True:
    ans = input(">>>>")
    cmd = ans.split(" ")
    if cmd[0] is "get":
        try:
            StartLog(float(cmd[1]))
        except ValueError:
            print("Enter valid command")
    pass