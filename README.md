# EnergyHub Coding Challenge
Thanks for checking out my program! It was a blast to work on and I really liked working with EnergyHub's data. Hope you all enjoy my solution! :octocat:

## Setup
To install our required packages we will use the `install.sh` script. This will install everything we need, including the energy_hub data in `/tmp/ehub_data`

### Requirements
This installation requires `python 2.7`, `pip`, as well as `virtualenv` on the local machine. 

### Install
```
$ chmod +x install.sh
$ ./install.sh
```

### File Structure
Here's what our directory layout looks like:
```
.
├── README.md
├── install.sh
├── test-all.sh
└── src
    ├── Replay.egg-info
    │   ├── PKG-INFO
    │   ├── SOURCES.txt
    │   ├── dependency_links.txt
    │   ├── entry_points.txt
    │   ├── requires.txt
    │   └── top_level.txt
    ├── click_datetime
    │   ├── __init__.py
    │   └── __init__.pyc
    ├── click_flexpath
    │   ├── __init__.py
    │   └── __init__.pyc
    ├── helper_lib
    │   ├── __init__.py
    │   └── __init__.pyc
    ├── replay
    │   ├── __init__.py
    │   └── __init__.pyc
    ├── setup.py
    ├── test_helper_lib
    │   └── test.py
    └── test_replay
        └── test.py
```

### Run
To run our program we need to activate our virtual environment from the top level directory.
```
$ source venv/bin/activate
```

## Usage
### General 
```
replay --field/-f [a_valid_field] /tmp/ehub_data timestamp
```
### One field
```
$ replay --field ambientTemp /tmp/ehub_data 2016-01-01T03:00
>>{"timestamp": "2016-01-01T03:00:00", "state": {"ambientTemp": 77.0}}
```
### Multiple fields
We can specify as many fields as we need. A shortened version of the flag (-f) also available:
```
$ replay --field ambientTemp -f schedule --field heatTemp /tmp/ehub_data 2016-01-01T03:00
>> {"timestamp": "2016-01-01T03:00:00", "state": {"heatTemp": "false", "ambientTemp": 77.0, "schedule": "false"}}
```
If a field doesn't exist in the diff, we mark it as false in our return object.

### Arguments 
For `path` replay requires the input path to be /tmp/ehub_data or an s3 link.\n
For `timestamp` replay requires the input timestamp to be in the format `%Y-%M-%dT%H%m`, such as: `2016-01-01T03:00`.
Where Y is year, M is month, d is day, T (splitter), H is hour, and m is minutes.

### Fields
Available fields are heatTemp, ambientTemp, and schedule.

### S3
We can also download straight from s3. Note: this link will only work for `s3://net.energyhub.assets/public/dev-exercises/audit-data/`
```
$ replay --field ambientTemp --field schedule s3://net.energyhub.assets/public/dev-exercises/audit-data/ 2016-01-01T03:00
>>{"state": {"ambientTemp": 77.0, "schedule": false}, "ts": "2016-01-01T03:00:00"}
```

The command will return a 404 not found if the s3 link is invalid:
```
$ replay --field ambientTemp --field schedule s3://net.energyhub.assets/public/dev-exercises/fakepath/ 2016-01-01T03:00
>>404 not found
```
Downloading for s3 is assumed to be a **very** expensive opereation. 
To mediate this, we check if the data is available locally in /tmp/ehub_data before initiating a download.
We also use Python's built-in LRU cache for a performance boost. 

### Help
Helpful details are also available by using the `--help` option.
```
$ replay --help
```

## Running unittests
We can run unittests by using the `test-all.sh` script.
```
$ chmod +x test-all.sh
$ ./test-all.sh
>>
Activated virtualenv
Testing replay
....
----------------------------------------------------------------------
Ran 4 tests in 2.326s

OK
Testing helper_lib
..mkdir: /tmp/ehub_data/: File exists
...........
----------------------------------------------------------------------
Ran 13 tests in 2.041s

OK
Done
```

## Helpful links, related literature
[Click Documentation.](https://click.palletsprojects.com/en/7.x/)
[Click testing.](http://click.palletsprojects.com/en/7.x/testing/)
[functools32 backporting initative.](https://github.com/michilu/python-functools32)
[Datetime class reference.](github.com/click-contrib/click-datetime/)


