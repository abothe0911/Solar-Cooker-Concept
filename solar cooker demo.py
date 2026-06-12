import pandas as pd
from pvlib import solarposition
import pytz
from datetime import datetime
import RPi.GPIO as GPIO
import time

# Location set
LATITUDE = 41.3126
LONGITUDE = -81.1437

#Setting up the servo

servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

#50 Hz is standard for servos
servo = GPIO.PWM(servo_pin, 50)
servo.start(0)

#Set an angle with a help method
def set_angle(angle):
    #Move the servo to the desired angle, assumes range of 0 - 180 degrees

    duty_cycle = 2 + (angle/18)
    GPIO.output(servo_pin, True)
    servo.ChangeDutyCycle(duty_cycle)

    time.sleep(0.5)

    GPIO.output(servo_pin, False)
    servo.ChangeDutyCycle(0)

#Timezone set

timezone = pytz.timezone('America/New_York')

try:
    while True:

        now = datetime.now(timezone)

        times = pd.DatetimeIndex([now])

        solpos = solarposition.get_solarposition(
            times,
            LATITUDE,
            LONGITUDE
        )

        azimuth = solpos['azimuth'].iloc[0]
        zenith = solpos['zenith'].iloc[0]

        elevation = 90 - zenith

        #We map the azimuth vector to servo range
        pan_angle = max(0, min(180, azimuth - 90))

        set_angle(pan_angle)

        print(
            f"{now.strftime('%H:%M:%S')} | "
            f"Azimuth: {azimuth:.1f}° | "
            f"Elevation: {elevation:.1f}° | "
            f"Servo: {pan_angle:.1f}°"
        )

        #Update every 5 minutes
        time.sleep(300)

except KeyboardInterrupt:
    print("Tracking stopped....")

finally:
    servo.stop()
    GPIO.cleanup()
