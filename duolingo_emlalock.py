#!/usr/bin/python3
# coding=utf-8
# Written by s4b3r1234 for the emlalock discord - 2021
# I know it's not pretty... but it works.

import duolingo
import time
import schedule
import requests
import sys
import configparser

if len(sys.argv) < 2:
    sys.stdout.write("\nUsage: nohup python3 duo_amlalock.py config.txt & \n")
    sys.stdout.write("Make sure that all required values are filled out in config.txt. All values are required except for emlalock-holder-api, which is only used if time is being subtracted. \n")
    sys.stdout.write("Time can be added or subtracted in the format W1 for 1 week or D1 for 1 day or H1 for 1 hour or M1 for 1 minute.")
    sys.exit(1)
# Setup the config parser
config = configparser.RawConfigParser(allow_no_value=True)
config.read('config.txt')

# Setup DuoLingo
if config.has_option('DUOLINGO', 'duo_user') == True:
    duo_user = config['DUOLINGO']['duo_user']
else:
    print("Missing value for duo_user. Please add it to config.txt")
    sys.exit(1)

if config.has_option('DUOLINGO', 'duo_pass') == True:
    duo_pass = config['DUOLINGO']['duo_pass']
else:
    print("Missing value for duo_pass. Please add it to config.txt")
    sys.exit(1)

lingo = duolingo.Duolingo(duo_user, duo_pass)
streak_info = lingo.get_streak_info()
streak_value = streak_info.get('streak_extended_today')

# Setup Emlalock
if config.has_option('EMLALOCK', 'emlalock_user_id') == True:
    emlalock_user_id = config['EMLALOCK']['emlalock_user_id']
else:
    print("Missing value for emlalock_user_id. Please add it to config.txt")
    sys.exit(1)
if config.has_option('EMLALOCK', 'emlalock_user_api') == True:
    emlalock_user_api = config['EMLALOCK']['emlalock_user_api']
else:
    print("Missing value for emlalock_user_api. Please add it to config.txt")
    sys.exit(1)
if config.has_option('EMLALOCK', 'duration_add') == True:
    duration_add = config['EMLALOCK']['duration_add']
else:
    print("Missing value for duration_add. Please add it to config.txt")
    sys.exit(1)

# These options are not required in config.txt, but are required if time will be subtracted on successful streak increase.
emlalock_holder_api = config['EMLALOCK']['emlalock_holder_api']
duration_sub = config['EMLALOCK']['duration_sub']

def add_time():
    payload = {'userid': emlalock_user_id, 'apikey': emlalock_user_api, 'value': duration_add}
    response = requests.get("https://api.emlalock.com/add", params=payload)
    response.text

def sub_time():
    if config.has_option('EMLALOCK', 'emlalock_holder_api') == True:
        payload = {'userid': emlalock_user_id, 'apikey': emlalock_user_api, 'holderapikey': emlalock_holder_api, 'value': duration_sub}
        response = requests.get("https://api.emlalock.com/sub", params=payload)
        response.text
    else:
        pass

def did_user_learn():
    if streak_value == True:
        if config.has_option('EMLALOCK', 'emlalock_holder_api') == False:
            sys.stdout.write("No Time is Added Today, Good Work!")
        else:
            sub_time()
            sys.stdout.write(duration_sub, "has been removed")
    else:
        sys.stdout.write(duration_add, "has been added")
        add_time()

#Setup scheduling
time_to_run = config['RUNTIME']['time_to_run']
schedule.every().day.at(time_to_run).do(did_user_learn)

while True:
    schedule.run_pending()
    time.sleep(60)
