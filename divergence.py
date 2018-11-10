import random
import time
from datetime import datetime
import ZeroSeg.led as led
import RPi.GPIO as GPIO

n = 7  # frequency to cross to the beta attractField


def newWorldLine():
    attractField = random.choice([0] * (n - 1) + [1])

    # Different distributions based on the attractField
    if attractField == 1:  # High % of low numbers
        worldDiffer = random.betavariate(2, 5)
    else:  # High % of high numbers
        worldDiffer = random.betavariate(5, 2)

    worldLine = str(attractField + worldDiffer)
    return(worldLine)


device = led.sevensegment()
dots = [False] * 8
dots[0] = True


def divergenceDisplay(device, deviceId, number, dots):

    device.letter(deviceId, 7, number[0], dots[0])
    device.letter(deviceId, 6, number[2], dots[1])  # number[1] is a dot
    device.letter(deviceId, 5, number[3], dots[2])
    device.letter(deviceId, 4, number[4], dots[3])
    device.letter(deviceId, 3, number[5], dots[4])
    device.letter(deviceId, 2, number[6], dots[5])
    device.letter(deviceId, 1, number[7], dots[6])


switch1 = 17
switch2 = 26

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers

GPIO.setup(switch1, GPIO.IN)
GPIO.setup(switch2, GPIO.IN)


def matrixflow():
    return(str(random.uniform(0, 10)))


device.brightness(3)

running = True

while running:
    if not GPIO.input(switch1):
        for i in range(24):
            dots = [False] * 8
            dots[i % 8] = True
            divergenceDisplay(device, 0, matrixflow(), dots)
            time.sleep(0.1)

            if i == 23:
                dots = [False] * 8
                dots[0] = True
                divergenceDisplay(device, 0, newWorldLine(), dots)

    if datetime.now().hour == 23:
        if datetime.now().minute == 59:
            if datetime.now().second == 59:
                for i in range(24):
                    dots = [False] * 8
                    dots[i % 8] = True
                    divergenceDisplay(device, 0, matrixflow(), dots)
                    time.sleep(0.1)

                    if i == 23:
                        dots = [False] * 8
                        dots[0] = True
                        divergenceDisplay(device, 0, newWorldLine(), dots)
