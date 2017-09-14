# Imports
import os
import time
import logging
import RPi.GPIO as GPIO
import shutil
import json


# Settings
sleep_time = 5 #300
logging_level = 'logging.INFO'
logging_state = True
log_file_name = 'app_logs.txt'
relay_pin_1 = 12
relay_pin_2 = 13
log_temperature = True
temp_format = 'F'
logs_folder = 'logs/'
th_high = 80
th_low = 70
cd_th = 3
wu_th = 3
device_list = {'28-0516a1a7d7ff':'Sensor 1',
     	       '28-0416b059cfff':'Sensor 2'}

# Setups
logging.basicConfig(filename=log_file_name, level=logging_level, format="%(asctime)s %(levelname)s %(message)s")
logging.info("Logging Enabled.")
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Variables
base_dir = '/sys/bus/w1/devices/'
mon_temp_sensor_count = len(device_list)
temp_sensor_count = len(device_list)
config_file_name = 'config_file.json'
example_config_file_name = 'config_file.json_example'


# Setups
if logging_state:
    import logging
    logging.basicConfig(filename=log_file_name, level=logging_level, format="%(asctime)s %(levelname)s %(message)s")
    logging.info("Logging Enabled.")
else:
    pass

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def config_file_check():
    config_file_status = os.path.isfile(config_file_name)

    if config_file_status:
        logging.info('Config file found.')
    else:
        logging.info('No config file found.  Creating config file from example.')
        shutil.copy(example_config_file_name, config_file_name)
        if config_file_status:
            logging.info('Config file creation SUCCESS.')
        else:
            logging.error('Error Creating log file. Check permissions.')
            break

# Config File Import
with open(config_file_name, encoding="utf-8") as config_file:
    config = json.loads(config_file.read())

id_import_example = config["settinggroup1"]["id1"]


# Functions
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
                lines = read_temp_raw()
            
            equals_pos = lines[1].find('t=')

            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                return temp_c, temp_f

        def sensor():
            if device_name.upper() == 'SENSOR 1':
                return relay_pin_1

            elif device_name.upper() == 'SENSOR 2':
                return relay_pin_2

        relay_pin = sensor()

        # Fan Controller
        def fan_control(status):

            def gpio_setup():
                GPIO.setwarnings(False) 
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(relay_pin_1, GPIO.OUT)
                GPIO.setup(relay_pin_2, GPIO.OUT)

            print("Checking Device : {}".format(device_name))

            def fan_on():
                gpio_setup()
                GPIO.output(relay_pin, 0)	#fan on
                return()

            def fan_off():
                gpio_setup()
                GPIO.output(relay_pin, 1)	#fan off
                return()

            if status.upper() == 'ON':
                fan_on()

            elif status.upper() == 'OFF':
                fan_off()

            elif status.upper() == 'NONE':
                fan_off()

            else:
                logging.error('No status for {} found.'.format(status.upper()))

        # Heat Control
        def heat_control(status):
            def heat_on():
                print("Heat control ON.")

            def heat_off():
                print("Heat control off.")

            if status.upper() == 'ON':
                heat_on()

            elif status.upper() == 'OFF':
                heat_off()

            elif status.upper() == 'NONE':
                heat_off()
        
        # Action to take based on current temperature
        def temp_action():
            if ctemp_f >= th_high:
                att = "ON"
                fan_control(att)

            elif ctemp_f <= (th_high - cd_th): # cool-down temp
                att = "OFF"
                fan_control(att)

            elif ctemp_f < (th_low - wu_th):
                att = "ON"
                heat_control(att)

            else:
                att = "NONE"
                fan_control(att)
                heat_control(att)

            return att

        # Write to sensor ID titled logs in the 'logs' folder
        def write_to_log():
            log_data = [device_name, device_id, ctemp_f, ctemp_c, current_time, action_to_take]

            temp_data_exist = os.path.exists(temp_data_file)

            if temp_data_exist is False:
                open(temp_data_file, 'a').close()
                logging.info("Log file {} has been Created ...".format(temp_data_file))

            with open(temp_data_file, mode='+a', encoding='utf-8') as log_open:
                final_write_data = str(log_data) + '\n'
                log_open.write(final_write_data)
                log_open.close()
        
        current_time = time.ctime()
        current_temp = read_temp()
        ctemp_f = int(current_temp[1])
        ctemp_c = int(current_temp[0])
        action_to_take = temp_action()

        if temp_format.upper() == 'F':
            print("Current temp on {} is : {}F at {}".format(device_name, ctemp_f, current_time))
        else:
            print("Current temp on {} is : {}C at {}".format(device_name, ctemp_c, current_time))
     
        if log_temperature:
            write_to_log()


# App Call
while True:
    config_file_check()
    device_check()
    time.sleep(sleep_time)