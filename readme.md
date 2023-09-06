# Installation
## Prerequisite
* Python 3.10 or above

## Instructions

1.  Download the source from Github: 
```
$ git clone https://github.com/sunyzm/geostats.git
```
2.  Donwload the basic version of `worldcities.csv` from https://simplemaps.com/data/world-cities; copy the file to both `geostats/data/` and `geostats/instance/data/`
3.  Add `geostats/gquery/` to the **PYTHONPATH** environment variable
4.  Setup Python venv:
```
$ python3.11 -m venv venv
$ pip install -r requirements.txt
$ source venv/bin/activate
```

#  Usage of `gquery`
```
$ python gquery/gquery.py info "san francisco"
$ python gquery/gquery.py compare "san francico" seattle "new york"
$ python gquery/gquery.py distance tokyo "hong kong"
$ python gquery/gquery.py distance "new york" london --unit=mi
```

# Usage of geostats server
```
$ flask --app server run
```
