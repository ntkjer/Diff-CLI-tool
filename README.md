# EnergyHub Coding Challenge

## Setup
To install our required packages we will use the `install.sh` script.

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

### Fields
Available fields are heatTemp, ambientTemp, and schedule.

### S3
We can also download straight from s3. Note: this link will only work for `s3://net.energyhub.assets/public/dev-exercises/audit-data/`
```
$ replay --field ambientTemp --field schedule s3://net.energyhub.assets/public/dev-exercises/audit-data/ 2016-01-01T03:00
>>{"state": {"ambientTemp": 77.0, "schedule": false}, "ts": "2016-01-01T03:00:00"}
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
General functionality is tested in `test_replay/test.py` and helper methods are tested in `test_helper_lib/test.py`
We can test either our helper library or replay package separately via the `test-helpers.sh` and `test-replay.sh` scripts.\n


## Helpful resources/literature
Click Documentation. \n
Click testing. \n
functools32. \n


