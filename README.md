# DuoLingo Linker for Emlalock

Start by downloading then editing the config.txt file. You will need the following:
1. Duolingo Username (I don't think this works with email, you will need to find your actual username in the app on your profile)
2. Duolingo password
3. Emlalock user ID (This can be found under settings > API on the website)
4. Emlalock user API key (This can be found under settings > API on the website)
5. (Optional) Emlalock session holder API key

The other options available set the duration to either add or subtract from time, depending on if the emlalock_holder_api is set. If this value is blank then no time is subtracted. If there is a value here then the script will attempt to remove time if the streak value is true.

The time is formatted according to the Emlalock WIKI (which has the information yet the actual API docs doesn't lol) https://wiki.emlalock.com/doku.php?id=the_emlalock_api

So if you wanted to add 4 days for a failure to study then you would type D4

Lastly you need to set what time to run, in 24 hours format.

You will need python3 and pip3 for this to work. 

#Install all dependencies
$ pip3 install -r requirements.txt --user

This can be ran directly from the terminal as:
$ nohup python3 duolingo_emlalock.py config.txt &

Or it can be installed as a service. On Ubuntu-based distro:

#Move duolingo_emlalock.service file to proper folder

$ sudo mv ./etc/systemd.system/duolingo_emlalock.service /etc/systemd/system/

#Move the script into a system accesible folder for better configuration

$ sudo mkdir -p /usr/local/lib/duolingo_emlalock/ && sudo mv ./duolingo_emlalock.py /usr/local/lib/duolingo_emlalock/

#Update systemd

$ sudo systemctl daemon-reload

#Check that the service loaded

$ sudo systemctl list-unit-files | grep duo

If you decide to run it as a service you will have to edit the duolingo_emlalock.service file and add in the location of your config.txt file:

ExecStart=/usr/bin/python3 /usr/local/lib/duolingo_emlalock/duolingo_emlalock.py /path/to/your/config.txt








# Oh, right, also, I'm not responsible if this breaks and adds loads of time to your lock. Use at your own risk!
