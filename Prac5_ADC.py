import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import RPi.GPIO as GPIO
import threading
import datetime
import time
from adafruit_mcp3xxx.analog_in import AnalogIn

def setup():
    # Global Variables
    global count
    global delay
    global runtime
    global chan
    count = 0
    runtime = 0
    delay = 10

    # ADC channels and values
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
    cs = digitalio.DigitalInOut(board.D5) # create the cs (chip select)
    mcp = MCP.MCP3008(spi, cs) # create the mcp object
    chan = AnalogIn(mcp, MCP.P0) # create an analog input channel on pin 0

    # RaspberryPi Values
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(17, GPIO.RISING, callback=button_toggle, bouncetime=200)


def convertTemperature():
        """
        This function converts the bit value to a temperature value in degrees celcius
        """
        global runtime
        global chan
        global delay
        thread = threading.Timer(delay, convertTemperature)
        thread.daemon = True
        thread.start()

        #Get temperature in readable values
        ADC_raw = chan.value
        ADC_voltage = chan.voltage
        temperature = ((ADC_raw*3.3)/float(1023))
        temperature = round(temperature,2)
        
        # Run time after operation
        end_time = time.time()
        runtime = round(end_time-start_time, 0)
        line = (f'{runtime}s',ADC_raw, f'{temperature} {chr(176)}C')
        print("{0: <20} {1: <20} {2: <20}".format(*line))


def button_toggle(channel):
        global count
        global delay
        count += 1
        if count==1:
                print("Button presed once")
                delay = 5
        elif count==2:
                print("Button pressed twice")
                delay = 1
        elif count==3:
                print("Button pressed thrice!")
                delay = 10
                count = 0
        return delay

def main():
    setup()
    line =  ('Runtime',"Temp Reading", "Temp")
    print("{0: <20} {1: <20} {2: <20}".format(*line))
    global start_time
    start_time = time.time()
    convertTemperature()

if __name__ == "__main__":
        try:
                main()
                while True:
                        pass
        except KeyboardInterrupt:
                print("\nExiting Gracefully..")
        except Exception as e:
                print(e)
        finally:
                GPIO.cleanup()

        if GPIO.input(17) == GPIO.HIGH:
                print("Button was pushed!")
                data = chan.value
                print("{0: <20} {1: <20} {2: <20}".format(* "Runtime"; "Temp Reading"; "Temp"))
                print("ADC Voltage: " + str(chan.voltage) + "V")