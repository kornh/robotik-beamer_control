""" motorcontrol """
#import time                     # Zeitsteuerung
from RPi import GPIO
#import RPi.GPIO as GPIO         # Ansteuerung der GPIO

print("Steuerprogram gestartet")
print("Bibliotheken geladen")

## Deklaration der Variablen
#pin_motor_1_1 = 27
#pin_motor_1_2 = 22
#pin_motor_2_1 = 23
#pin_motor_2_2 = 24
PINS = [
    [27, 22],
    [23, 24]
]

print("Variablen deklariert")

## Setzten der Portrichtung
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINS[0][0], GPIO.OUT)
GPIO.setup(PINS[0][1], GPIO.OUT)
GPIO.setup(PINS[1][0], GPIO.OUT)
GPIO.setup(PINS[1][1], GPIO.OUT)

print("Portrichtungen gesetzt")

def set_pin(motor, status):
    """Set the pins to control the motors"""

    GPIO.output(PINS[0][0], 0)
    GPIO.output(PINS[0][1], 0)
    GPIO.output(PINS[1][0], 0)
    GPIO.output(PINS[1][1], 0)

    if status == 0:
        return

    motor = (0 if motor == 1 else 1)
    status = (0 if status > 0 else 1)
    print('Motor: {} Status: {}'.format(motor, status))

    pin = PINS[motor][status]
    print(pin)
    GPIO.output(pin, 1)

def reset():
    """Reset the GPIO-Pins"""
    GPIO.cleanup()           # Bei Programabbruch GPIO zuruecksetzten
'''
    time.sleep(1)
'''