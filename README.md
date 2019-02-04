# RealDeviceMap-LoginLimitEnforcer
A tool to enforce a limitation on the number of consecutive sessions for users of the RealDeviceMap front end.

## Basis of the RealDeviceMap-LoginLimitEnforcer

The RDM-LLE script was written to query the RDM database for the number of user sessions for each user, select the session tokens for those over the limit, and delete the user token over the allowed limit.

The RDM-LLE script queries the RDM database to find a users' most recently updated session tokens and reserves those while deleting those over the set limit of sessions a person may have.

The result, with the default settings, a person is allowed one session token, aka logins, at one time. When a person logins in again, the session(s) where a user has logged in more frequently are kept whereas the older user sessions are deleted.

#### Reducing Database Queries and Increasing the Number of Allowed Users

The default setting for the script is to allow `1` user session at once while checking the database every 30 seconds for anyone who is over the session limit. Increasing the time between loops will decrease the overall number of queries to the database and reduce any database strain that may be occurring with the combination of tools such as Novabot, RDM-Tools, combined with the RDM-LLE script on the database. Increasing the run time to 120 seconds between loops will reduce DB queries to 1/4 of the default setting, thus, if a database is under strain, raising the time between loops can be a simple way to alleviate some of the stress on the database.

If a person wants to increase the number of allowed concurrent user session per account, follow the instructions in the LoginLimit.py section of this readme. 

## Install

Compatible and tested with python2.7, python3.5, and python3.6 although print out formatting and mysql error codes display better with python3.5+

```
git clone https://github.com/ftballpack/RealDeviceMap-LoginLimitEnforcer
cd RealDeviceMap-LoginLimitEnforcer
pip install -r requirements.txt
```
If the above fails to install correctly for you, you may need to pip install setup tools first. i.e., `sudo pip install setuptools` for regular python/python2.7. If you are using an alternate version of python, you will need use pip with that version of python to install setup tools and the mysql connector. ie., If using python 3.7 you would need to use `sudo pip3.7 install setuptools` followed by `pip3.7 install -r requirements.txt` if setup tools is not already installed on your system.

For python3 users, use `pip3` or `pip3.6` or `pip3.7` depending upon the python flavor you choose to use with RDM-LLE

All users need to input their RDM database credentials in the DB config section to enable the script to interact with your database. 

#### To Run the Script

Simply use `python loginlimit.py` or for python3 `python3 loginlimit.py` etc.


### LoginLimit.py

The default setting is to allow one user sessions per account. To increase or decrease the number of allowed sessions, change the config setting for the variable `number_of_concurrent_allowed_user_sessions_per_account` to the desired number of allowed users sessions. Changing the number in this variable will automatically make the proper adjustments for the rest of the sql queries to allow up to the limit of user sessions, per id, a person wants to allow.

The default time between querying the database is 30 seconds. To change this, change the `time_in_seconds_between_check_cycles` from 30 to the desired number of cycles desired for the script to check before querying the database again.


### Automatic Restart of LoginLimit.py on machine reboot.(Instructions for headless Ubuntu installs)

The best way to run LoginLimit.py is in a tmux session. tmux allows users, especially on a VPS, to restart the script automatically and still be able to interact and kill the script easily.

If tmux is not installed, on a Ubuntu based system, a person can use, `sudo apt-get update` followed by `sudo apt-get install tmux` to install tmux.

To accomplish this, we will use the `startLLE.sh` script paired with an `@restart` cron to automatically restart the python script and to put the script in a new tmux session called `LLE` by default. The script path in `startLLE.sh` assumes a person followed the earlier instructions of how to git clone this project. If you put the `loginlimit.py` script in a different directory, you will need to change the path accordingly.

If a person wants to use a different version of python with the script, other than the default, you will have to change the python setting in front of the file path in the `startLLE.sh` script. If you want to use the default python 3 on your system use `python3` instead of `python` or `python3.6` instead of `python` etc.

##### First

755 permissions need to be given to the `startLLE.sh` script so that the system can automatically restart the script on reboot. `sudo chmod -R 755 ~/RealDeviceMap-LoginLimitEnforcer/startLLE.sh` If a person is running the `startLLE.sh` script in a different directory, you will need to adjust the path accordingly.

##### Second

On Ubuntu based systems, use `crontab -e` to set the task to be run using a cron. To set the start script to run on reboot, scroll to the bottom on the window and add `@reboot /bin/sleep 180; sh ~/RealDeviceMap-LoginLimitEnforcer/startLLE.sh` This tells the cron to run that script on reboot, with a 180 second (3 minute) delay. If your system is faster or slow, you will need to adjust the delay. If no delay is included, the cron may execute too early and the script may fail to open tmux. If your `startLLE.sh` file is in a different location, you will need to adjust the path accordingly.

##### Post restart

Upon restart, the `sh.startLLE.sh` script will execute. By default, it's set to start a new, detached, tmux session called `LLE`. To connect to this tmux session after it has started use `tmux a -t LLE`. To leave the tmux session use `ctrl + b` followed by `d`. This tells tmux to detach from the current session but to keep the script going. To kill the tmux session and thus killing `loginlimit.py` use `tmux kill-session -t LLE`.

More background info for those new to tmux. https://hackernoon.com/a-gentle-introduction-to-tmux-8d784c404340

#### TODO

-Change the number of allowed concurrent user sessions and the delay in seconds to variables, that link back to a config for easier setup/changes.

-Setting the user credentials to variables that can be entered at the top of the script, for easier user access.
