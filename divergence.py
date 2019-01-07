import random
import time
from datetime import datetime
import ZeroSeg.led as led
import RPi.GPIO as GPIO

n = 7  # frequency to cross to the beta attractField

device = led.sevensegment()
dots = [False] * 8
dots[0] = True

switch1 = 17
switch2 = 26

GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
GPIO.setup(switch1, GPIO.IN)
GPIO.setup(switch2, GPIO.IN)

device.brightness(3)


def newWorldLine():
    attractField = random.choice([0] * (n - 1) + [1])

    # Different distributions based on the attractField
    if attractField == 1:  # High % of low numbers
        worldDiffer = random.betavariate(2, 5)
    else:  # High % of high numbers
        worldDiffer = random.betavariate(5, 2)

    worldLine = str(attractField + worldDiffer)
    return(worldLine)


def divergenceDisplay(device, deviceId, number, dots):

    device.letter(deviceId, 7, number[0], dots[0])
    device.letter(deviceId, 6, number[2], dots[1])  # number[1] is a dot
    device.letter(deviceId, 5, number[3], dots[2])
    device.letter(deviceId, 4, number[4], dots[3])
    device.letter(deviceId, 3, number[5], dots[4])
    device.letter(deviceId, 2, number[6], dots[5])
    device.letter(deviceId, 1, number[7], dots[6])


# Creating the matrix of world lines

def divergenceMatrixCreate():
    divergenceMatrix = [random.uniform(0, 10)] * 24
    for i in range(23):
        divergenceMatrix[i] = str(random.uniform(0, 10))
    divergenceMatrix[23] = str(newWorldLine())
    return(divergenceMatrix)

# Updating the world line every day depending on th ehour, minute, second


def dayUpdate(hour, minute, second):
    if datetime.now().hour == hour:
        if datetime.now().minute == minute:
            if datetime.now().second == second:

                updateWorld()

# Updates the display with the new world line - roll in fucntion


def updateWorld():
    divergenceMatrix = divergenceMatrixCreate()
    for i in range(24):
        if i == 0:
            j = 1

        if i <= (24 - 8):
            divergenceDisplay(device, 0, divergenceMatrix[i], dots)

        if i > (24 - 8):
            divergenceDisplay(
                device, 0, divergenceMatrix[23][0:j] + divergenceMatrix[i][j:8], dots)
            j += 1
            if j == 2:
                j += 1
        time.sleep(0.15)
    print(divergenceMatrix)


running = True

while running:
    dayUpdate(23, 59, 59)

    if not GPIO.input(switch2):
        updateWorld()
