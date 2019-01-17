# RealDeviceMap-LoginLimitEnforcer
A tool to enforce a limitation on the number of consecutive sessions for users of the RealDeviceMap front end.

## Basis of the RealDeviceMap-LoginLimitEnforcer

The RDM-LLE script was written to query the RDM database for the number of user sessions for each user, select the session tokens for those in excess of the limit, and delete the user token in excess of the allowed limit.

The RDM-LLE script queries the RDM database to find a users' most recently updated session tokens and reserves those while deleting those in excess of the set limit of sessions a person may have.

The end result, with the default settings, a person is allowed two session tokens, aka logins, at one time. When a person logins in again, those sessions when a user has logged in more freqently are kept whereas the older user sessions are deleted.

#### Cases of Known User Abuse

The default setting for the script is to allow `2` user sessions at once. If a person knows that RDM logins are being abused, it's advised to change the user session to `1` in the database scripts and change the delay in pulling from the database to 30 seconds. More info on that is posted later in this readme. This will not stop users from logging in on 2 seperate devices at one time, but will heavily discourage the use of users abusing their RDM priveleges as users will be continously logging each other out, when they themselves log in, with shared credentials, to the point where sharing credentials becomes utterly useless.

## Install

Compatible and tested with python2.7, python3.5 and python3.6 although print out formatting is better with python3.5+

```
git clone https://github.com/ftballpack/RealDeviceMap-LoginLimitEnforcer
cd RealDeviceMap-LoginLimitEnforcer
pip install -r requirements.txt
```

For python3 users, use `pip3` or `pip3.6` or `pip3.7` depending upon your python flavor you choose to use with RDM-LLE

#### To Run the Script

Simply use `python loginlimit.py` or for python3 `python3 loginlimit.py` etc.


### LoginLimit.py

The default setting are to allow 2 user sessions per account. To increase or decrease the number of allowed sessions, change the `2` in the first SQL Select query to the number of allowed user sessions. Also a person will also need to change the number `2` in the second SQL Select query to the number of user sessions a person wants to allow at one time.

The default time between querying the database is 2 minutes, in seconds. To change this, change `time.sleep(120)` setting to the desired number of seconds between checking the database. These need to be updated in both the last line of `loginlimit.py` and also in the error section, near the end of `loginlimit.py`.


#### TODO

-Change the number of allowed concurrent user sessions and the delay in seconds to variables.

-Setting the user credentials to variables that can be entered at the top of the script, for easier user access.
