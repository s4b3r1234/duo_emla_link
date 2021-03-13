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


# Oh, right, also, I'm not responsible if this breaks and adds loads of time to your lock. Use at your own risk!
