# RealDeviceMap-LoginLimitEnforcer
A tool to enforce a limitation on the number of consecutive sessions for users of the RealDeviceMap front end.

## Basis of the RealDeviceMap-LoginLimitEnforcer

The RDM-LLE script was written to query the RDM database for the number of user sessions for each user, select the session tokens for those over the limit, and delete the user token over the allowed limit.

The RDM-LLE script queries the RDM database to find a users' most recently updated session tokens and reserves those while deleting those over the set limit of sessions a person may have.

The result, with the default settings, a person is allowed two session tokens, aka logins, at one time when a person logins in again, those sessions when a user has logged in more frequently are kept whereas the older user sessions are deleted.

#### Cases of Known User Abuse

The default setting for the script is to allow `2` user sessions at once. If a person knows that RDM logins are being abused, it's advised to change the user session to `1` in the database scripts and change the delay in pulling from the database to 30 seconds. More info on that is posted later in this readme. This will not stop users from logging in on 2 separate devices at one time, but will heavily discourage the users from abusing their RDM privileges as users will be continuously logging each other out, when they themselves log in, with shared credentials, to the point where sharing credentials becomes utterly useless.

## Install

Compatible and tested with python2.7, python3.5, and python3.6 although print out formatting is better with python3.5+

```
git clone https://github.com/ftballpack/RealDeviceMap-LoginLimitEnforcer
cd RealDeviceMap-LoginLimitEnforcer
pip install -r requirements.txt
```

For python3 users, use `pip3` or `pip3.6` or `pip3.7` depending upon the python flavor you choose to use with RDM-LLE

All users need to input their RDM database credentials in the `conn = mysql.connector.connect` section to enable the script to interact with your database. 

#### To Run the Script

Simply use `python loginlimit.py` or for python3 `python3 loginlimit.py` etc.


### LoginLimit.py

The default setting is to allow two user sessions per account. To increase or decrease the number of allowed sessions, change the `2` in the first SQL Select query to the number of allowed user sessions. Also, a person will also need to change the number `2` in the second SQL Select query to the number of user sessions a person wants to allow at one time.

The default time between querying the database is 2 minutes, in seconds. To change this, change `time.sleep(120)` setting to the desired number of seconds between checking the database. These need to be updated in both the last line of `loginlimit.py` and also in the error section, near the end of `loginlimit.py`.


### Automatic Restart of LoginLimit.py on machine restart.

The best way to run LoginLimit.py is in a tmux session. This allows users, especially on a VPS to restart the script automatically and still be able to easily interact and kill the script, if need be.

If tmux installed in not installed, on a Ubuntu based system, a person can use, `sudo apt-get update` followed by `sudo apt-get install tmux` to install tmux.

To accomplish this, we will use the `startLLE.sh` script paired with an `@restart` cron to automatically restart the python script and to put the script in a new window called `LLE` by default. The script path in `startLLE.sh` assumes a person followed the earlier instructions of how to git clone this project. If you put the `loginlimit.py` script in a different directory, you will need to change the path accordingly.

If a person wants to use a different version of python with the script, other than the default, you will have to change the python setting in front of the directory location in the `startLLE.sh` script. If you want to use the default python 3 on your system use `python3` instead of `python` or `python3.6` instead of `python` etc.

##### First

755 permissions need to be given to the `startLLE.sh` script so that the system can automatically restart the script on reboot. `sudo chmod -R 755 ~/RealDeviceMap-LoginLimitEnforcer/startLLE.sh` If a person is running the `startLLE.sh` script in a different directory, you will need to adjust the path accordingly.

##### Second

On Ubuntu based systems, use `crontab -e` to set the task to be run using a cron. To set the start script to run on reboot, scoll to the bottom on the window and add `@reboot /bin/sleep 180; sh ~/RealDeviceMap-LoginLimitEnforcer/startLLE.sh` This tells the cron to run that script on reboot, with a 180 second (3 minute) delay. If your system is faster or slow, you will need to adjust the delay. If no delay is included, the cron may execute too early and the script may fail to open tmux. If your `startLLE.sh` file is in a different location, you will need to adjust the path accordingly.

##### Post restart

Upon restart, the `sh.startLLE.sh` script will execute. By default it's set to start a new, detached, tmux session called `LLE`. To connect to this tmux session use `tmux a -t LLE`. To leave the tmux session use `ctrl + b` followed by `d`. This tell tmux to detach from the current session but to keep the script going. To kill the tmux session and thus killing `loginlimit.py` use `tmux kill-session -t LLE`.

In the event the bash script executes and starts the tmux session and starts the `loginlimit.py` before the database server is ready, the script's catch will catch the error and delay for a default of two minutes before attempting to make another connection to the database.

More background info for those new to tmux. https://hackernoon.com/a-gentle-introduction-to-tmux-8d784c404340

#### TODO

-Change the number of allowed concurrent user sessions and the delay in seconds to variables.

-Setting the user credentials to variables that can be entered at the top of the script, for easier user access.
