#!/usr/bin/python3
# coding=utf-8
# Written by s4b3r1234 for the emlalock discord - 2021
# I know it's not pretty... but it works.
# March 14, 2021 - Fixed an issue where the streak value would hold as what it was when the script was first run. This was purely due to me not knowing anything.

import duolingo
import time
import schedule
import requests
import sys
import configparser

# Setup the config parser
config = configparser.RawConfigParser(allow_no_value=True)
config.read('config.txt')

# Check for configs. I'm not actually sure this works, I'm not sure why it's returning if the value exists, not if there is a value.
# If anyone knows why this is or how I can fix it please let me know.
if config.has_option('DUOLINGO', 'duo_user') == True:
    pass
else:
    print("Missing value for duo_user. Please add it to config.txt")
    sys.exit(1)

if config.has_option('DUOLINGO', 'duo_pass') == True:
    pass
else:
    print("Missing value for duo_pass. Please add it to config.txt")
    sys.exit(1)

# Moved the streak checker into a callable function. Previously it was holding the value (Duh, stupid me!)
def streak_check():
    duo_user = config['DUOLINGO']['duo_user']
    duo_pass = config['DUOLINGO']['duo_pass']
    lingo = duolingo.Duolingo(duo_user, duo_pass)
    streak_info = lingo.get_streak_info()
    streak_value = streak_info.get('streak_extended_today')
    if streak_value != True and streak_value != False:
        print("Invalid Return")
        return streak_value
    else:
        return streak_value
        print(streak_value)

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
duration_sub = config['EMLALOCK']['duration_sub']

if config.has_option('EMLALOCK', 'emlalock_holder_api') == True:
    emlalock_holder_api = config['EMLALOCK']['emlalock_holder_api']
    holder_api_exists = True
else:
    holder_api_exists = False

def add_time():
    payload = {'userid': emlalock_user_id, 'apikey': emlalock_user_api, 'value': duration_add}
    response = requests.get("https://api.emlalock.com/add", params=payload)
    response.text

def sub_time():
    if holder_api_exists == True:
        payload = {'userid': emlalock_user_id, 'apikey': emlalock_user_api, 'holderapikey': emlalock_holder_api, 'value': duration_sub}
        response = requests.get("https://api.emlalock.com/sub", params=payload)
        response.text
    else:
        pass

def did_user_learn():
    if streak_check() == True:
        if config.has_option('EMLALOCK', 'emlalock_holder_api') == True:
            sub_time()
            print(duration_sub, "has been removed")
        else:
            if config.has_option('EMLALOCK', 'emlalock_holder_api') == False:
                sys.stdout.write("No Time is Added Today, Good Work!")
    else:
        print(duration_add, "has been added")
        add_time()

# Setup scheduling
time_to_run = config['RUNTIME']['time_to_run']
schedule.every().day.at(time_to_run).do(did_user_learn)

while True:
    schedule.run_pending()
    time.sleep(60)
