# Imports
import os
import time
import logging
import RPi.GPIO as GPIO


# Setups
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# Variables
base_dir = '/sys/bus/w1/devices/'


# Settings
sleep_time = 5 #300
diag_mode = True
relay_pin_1 = 12
relay_pin_2 = 12
log_weather = 'Y'
temp_format = 'F'
logs_folder = 'logs/'
th_high = 80
th_low = 70
device_list = {'28-0516a1a7d7ff':'Sensor 1',
     	       '28-0416b059cfff':'Sensor 2'}


# Functions

# Temp functions to be removed later #########
def space():
    space = '\n' + 32 * '-' + '\n'
    print(space)

##############################################

def device_check():
    for device_id, device_name in device_list.items():

        temp_data_file = logs_folder + device_id
        device_id_loc = base_dir + device_id + '/w1_slave'
        
        # Grab Sensor file
        def read_temp_raw():
            f = open(device_id_loc, 'r')
            lines = f.readlines()
            f.close()
            return lines
        
        # Extract the temp, convert it, and return it        
        def read_temp():
            lines = read_temp_raw()

            while lines[0].strip()[-3:] != 'YES':
                #time.sleep(0.2)
                lines = read_temp_raw()
            
            equals_pos = lines[1].find('t=')

            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f

        # Fan Controller
        def fan_control(status):

            if diag_mode == True :
                print("Fan Control function Called with {} sent to it.".format(status))

            def GPIOsetup():
                GPIO.setwarnings(False) 
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(relay_pin_1, GPIO.OUT)

            def sensor():
                if device_name.upper() in 'SENSOR 1':
                    relay_pin = relay_pin_1
                    return relay_pin
                    print("Using Relay 1")

                elif device_name.upper() in 'SENSOR 2':
                    relay_pin = relay_pin_2
                    return relay_pin
                    print("Using Relay 2")

            relay_pin = sensor()
                
            def fan_on():
                GPIOsetup()
                GPIO.output(relay_pin, 0)	#fan on
                return()
                print("Fan Turned ON for {}".format(device_name))

            def fan_off():
                GPIOsetup()
                GPIO.output(relay_pin, 1)	#fan off
                return()
                print("Fan Turned OFF for {}".format(device_name))

            if status.upper() == 'ON':
                fan_on()
            elif status.upper() == 'OFF':
                fan_off()
        
        # Action to take based on current temperature
        def temp_action():

            if ctemp_f <= int(th_low):
                att = "OFF"
                fan_control(att)
                print()
                return att

            elif ctemp_f >= int(th_high):
                att = "ON"
                fan_control(att)
                return att

            print("Temp action called and returned {}".format(att))
        
        # Write to sensor titled logs in the 'logs' folder
        def write_to_log():
            log_data = [device_name, device_id, ctemp_f, ctemp_c, current_time, actiontt]

            print("Logging : {} \n".format(log_data))

            if os.path.exists(temp_data_file) == False:
                open(temp_data_file, 'a').close()
                print("Log file {} has been Created ...".format(temp_data_file))

            with open(temp_data_file, mode='+a', encoding='utf-8') as log_open:
                final_write_data = str(log_data) + '\n'
                log_open.write(final_write_data)
                log_open.close()
        
        current_time = time.ctime()
        current_temp = read_temp()
        ctemp_f = int(current_temp[1])
        ctemp_c = int(current_temp[0])
        actiontt = temp_action()


## Delete me later ##
        print(actiontt)
        print(type(actiontt))

#####################

        print('Checking {}'.format(device_name))
        print('Sensor file location: {}'.format(device_id_loc))
        print('Action : {}'.format(actiontt))

        if temp_format.upper() == 'F':
            print("Current temp on {} is : {}F at {}".format(device_name, ctemp_f, current_time))
        else:
            print("Current temp on {} is : {}C at {}".format(device_name, ctemp_c, current_time))
     
        if log_weather.upper() == 'Y':
            write_to_log()


# App Call
while True:
    space() # Will be removed later
    device_check()
    time.sleep(sleep_time)
