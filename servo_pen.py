import RPi.GPIO as GPIO
import time

# ---------- Configuratie ----------
SERVO_PIN  = 18         # PWM-capabele GPIO pin
BUTTON_PIN = 17         # GPIO pin voor de drukknop
PWM_FREQ   = 50         # MG90S werkt op 50 Hz

# Hoeken voor de twee toestanden (pas aan op jouw mechanisme)
ANGLE_REST   = 0        # pen ligt (rusttoestand)
ANGLE_ACTIVE = 60       # pen opgetild (actieve toestand)

DEBOUNCE_MS = 200       # ontdender-tijd in milliseconden

pen_is_up = False   # begint in rusttoestand (pen ligt)

def angle_to_duty(angle):
    """Zet een hoek (0-180°) om naar duty cycle (%) voor 50 Hz PWM."""
    return 2.5 + (angle / 180.0) * 10.0

def set_angle(pwm, angle):
    pwm.ChangeDutyCycle(angle_to_duty(angle))
    time.sleep(0.4)              # tijd om naar positie te bewegen
    pwm.ChangeDutyCycle(0)       # signaal uit -> voorkomt jitter/zoemen

def button_pressed(channel):
    global pen_is_up
    if pen_is_up:
        print("Knop ingedrukt -> pen neerleggen")
        set_angle(pwm, ANGLE_REST)
        pen_is_up = False
    else:
        print("Knop ingedrukt -> pen optillen")
        set_angle(pwm, ANGLE_ACTIVE)
        pen_is_up = True

def main():
    global pwm

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
    pwm.start(0)

    # Zorg dat de pen bij start in rusttoestand staat
    set_angle(pwm, ANGLE_REST)

    # Detecteer dalende flank (knop verbindt GPIO met GND bij indrukken)
    GPIO.add_event_detect(
        BUTTON_PIN,
        GPIO.FALLING,
        callback=button_pressed,
        bouncetime=DEBOUNCE_MS
    )

    print("Klaar. Druk op de knop om de pen op te tillen / neer te leggen.")
    print("Druk Ctrl+C om te stoppen.")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgramma gestopt.")
    finally:
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
