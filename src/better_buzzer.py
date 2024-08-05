from time import sleep
import RPi.GPIO as GPIO # type: ignore

class customBuzzer:
    buzzerPin = 18
    dutyCycle: int
    def __init__(self, volume: int = 20):			# PWM pin connected to LED
        self.dutyCycle = volume
        GPIO.setwarnings(False)			#disable warnings
        GPIO.setmode(GPIO.BCM)		#set pin numbering system
        GPIO.setup(18,GPIO.OUT)


    def __note_to_frequency(self, note: str) -> int:
        # A dictionary to hold the base frequencies of the notes in the 4th octave
        base_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13, 'E': 329.63,
            'F': 349.23, 'F#': 369.99, 'G': 392.00, 'G#': 415.30, 'A': 440.00,
            'A#': 466.16, 'B': 493.88
        }

        # Extract the note part and the octave part
        if note[-1].isdigit():
            note_part = note[:-1]
            octave = int(note[-1])
        else:
            note_part = note
            octave = 4  # Default octave is 4 if not specified

        # Get the base frequency of the note in the 4th octave
        base_frequency = base_frequencies.get(note_part)

        if base_frequency is None:
            raise ValueError("Invalid musical note")

        # Calculate the frequency of the note in the given octave
        frequency = base_frequency * (2 ** (octave - 4))

        # Return the frequency as an integer
        return int(frequency)


    def playTone(self, note: str, durationSec=0.075):
        freq = self.__note_to_frequency(note)
        pi_pwm = GPIO.PWM(self.buzzerPin,freq)		#create PWM instance with frequency
        pi_pwm.start(0)				#start PWM of required Duty Cycle 
        pi_pwm.ChangeDutyCycle(self.dutyCycle) # Turn on buzzer
        sleep(durationSec)
        pi_pwm.ChangeDutyCycle(0) # Turn off buzzer


    def beep(self, ontimeSec, offtimeSec, repeatnum):
        for cnt in range(repeatnum):
            self.playTone("C4",durationSec=ontimeSec) 
            sleep(offtimeSec)

        

if __name__ == "__main__":
    buzzer = customBuzzer()
    buzzer.playTone("B5",0.04)
    buzzer.playTone("E6",0.46)
    sleep(0.3)