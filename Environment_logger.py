# Import libraries
# Libraries for EEPROM
import RPi.GPIO as GPIO
import ES2EEPROMUtils
import os
import smbus2 as SMBUS
import time

#Libraries for ADC
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import threading
import datetime
from adafruit_mcp3xxx.analog_in import AnalogIn 

def setup():
    # Global Variables
    global count
    global rate
    global runtime
    global chan
    global log
    global samples
    global num_samples
    global pwm
    global eeprom
    global saver
    
    count = 0
    runtime = 0
    delay = 10
    log = 0
    samples = []
    num_samples = 0
    saver = 0
    rate = 5
    
    #Memory objects for EEPROM
    eeprom = ES2EEPROMUtils.ES2EEPROM()
    
    # ADC channels and values
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # create the spi bus
    cs = digitalio.DigitalInOut(board.D5) # create the cs (chip select)
    mcp = MCP.MCP3008(spi, cs) # create the mcp object
    chan = AnalogIn(mcp, MCP.P0) # create an analog input channel on pin 0

    # RaspberryPi Values
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(13, GPIO.OUT)
    GPIO.add_event_detect(17, GPIO.RISING, callback=button_rate, bouncetime=200)
    GPIO.add_event_detect(27, GPIO.RISING, callback=button_log, bouncetime=200)
    
    pwm = GPIO.PWM(13,1000)
    pwm.start(0)
    
"""Interrupt functions for debouncing buttons"""
def button_rate(channel):
    #This function changes the sample intervals for a user's choosing
    global count
    global rate
    count += 1
    if count==1:
            print("Sampling rate set at 5s")
            rate = 5
    elif count==2:
            print("Sampling rate changed to 1s")
            rate = 1
            count = 0
    return rate
        
def button_log(channel):
    #This function enables/disables logging
    global log
    global saver
    saver += 1
    if saver == 1:
        print("Logging has begun. Samples are automatically saved.")
        buzz(0)
        log = 1
        saver = 0
    else:
        log = 0
        print("Logging has stopped. Samples are not automatically saved.")
    return log

    
def buzz(boolean):
    global pwm
    if(boolean==1):
        pwm.ChangeDutyCycle(0.5)
        pwm.ChangeFrequency(10)
    else:
        pwm.ChangeDutyCycle(0) #turns buzzer off
        
"""System interactions with the ADC"""
def read_ADC(): 
    #This function converts the bit value to a temperature value in degrees celcius
    global runtime
    global chan
    global rate
    global log
    global samples
    
    thread = threading.Timer(rate, read_ADC)
    thread.daemon = True
    thread.start()
    real_time = datetime.datetime.now().time()
    realtime = real_time.strftime("%H:%M:%S")

    #Get temperature in readable values
    ADC_raw = chan.value
    ADC_voltage = chan.voltage
    temperature = (ADC_voltage-0.5)/0.01 #((ADC_raw*3.3)/float(1023))
    temperature = round(temperature,2)
    temp = int(abs(temperature))
    
    # Run time after operation
    end_time = time.time()
    runtime = round(end_time-start_time, 0)
    if log == 1:
        save_samples(temp,real_time)
        sound = " "
    elif log == 0:
        buzz(1) #Buzzer goes off when there is no logging
        sound = '*'
    line = (f'{real_time}s',f'{runtime}s', f'{temperature} {chr(176)}C',f'{sound}')
    print("{0: <12} {1: <12} {2: <10} {3: <7}".format(*line))
   
 
"""System interactions with memory element EEPROM"""
def save_samples(temp_value,time_value):
    #This module saves up to 20 of the latest samples of our data
    global eeprom
    samples, temp_data = read_log()
    if samples < 20:
        samples += 1
    elif samples >= 20:
        del temp_data[0]
    #Method that actually moves data to EEEPROM
    #temp_data.append([time_value.hour, time_value.minute, time_value.second, temp_value])
    temp_data.append(time_value.hour)
    temp_data.append(time_value.minute)
    temp_data.append(time_value.second)
    temp_data.append(temp_value)
    eeprom.write_block(1, temp_data)
    sampled_data = []
    sampled_data.append(time_value.hour)
    sampled_data.append(time_value.minute)
    sampled_data.append(time_value.second)
    sampled_data.append(temp_value)
    #for data in temp_data:
     #   for value in data[0]:
      #      sampled_data.append(time_value.hour)
       # sampled_data.append(temp_data[1])
    eeprom.write_block(1, sampled_data)
    
def read_log():
    # This module tells us all the samples that we have saved
    global eeprom
    samples = eeprom.read_byte(0) # The number of samples is stored in first byte
    temp_data = []
    for i in range(0, samples+1):
        temp_data.append(eeprom.read_block(i,4))
    return samples, temp_data
    
def display_log():
    #Shows user actual values stored in EEPROM
    stored_data = read_log()
    print("There are {1} samples stored".format(stored_data[0]))
    print("The samples values are:\n", (stored_data[1]))

"""System interaction"""   
    
def main():
    welcome()
    display()
    global start_time
    start_time = time.time()
    read_ADC()
    
"""Modules that ensure safety and housekeeping"""
    
def cleanup():
    # Cleaning module
    GPIO.remove_event_detect(btn_submit)
    GPIO.remove_event_detect(btn_increase)
    GPIO.cleanup()
    

def display():
    #Display setup, so values are displayed in table manner
    tableHeaders = ["Time", "Sys Timer", "Temp","Buzzer"]
    template = '{:<12}|{:<12}|{:<10}|{:<7}'
    print("working bitch")
    print template.replace(':', ':-').format('', '', '', '')
    print template.format(*tableHeaders)
    print template.replace(':', ':-').format('', '', '', '')
 
    
def welcome(): 
    # Extra userability introduction
    os.system('clear')
    print("  ______            _                                      _     _                                ")
    print(" |  ____|          (_)                                    | |   | |                               ")
    print(" | |__   _ ____   ___ _ __ ___  _ __  _ __ ___   ___ _ __ | |_  | |     ___   __ _  __ _  ___ _ __ ")
    print(" |  __| | '_ \ \ / / | '__/ _ \| '_ \| '_ ` _ \ / _ \ '_ \| __| | |    / _ \ / _` |/ _` |/ _ \ '__|")
    print(" | |____| | | \ V /| | | | (_) | | | | | | | | |  __/ | | | |_  | |___| (_) | (_| | (_| |  __/ |   ")
    print(" |______|_| |_|\_/ |_|_|  \___/|_| |_|_| |_| |_|\___|_| |_|\__| |______\___/ \__, |\__, |\___|_|   ")
    print("                                                                              __/ | __/ |          ")
    print("                                                                             |___/ |___/           ")

    
if __name__ == "__main__": #If run as the main script, run main()
    try:
        main()
        while True:
            pass
    except KeyboardInterrupt as e:
        display_log()
        cleanup()
        print(e)
    except Exception as e:
        print(e)
        cleanup()
    finally:
        cleanup()