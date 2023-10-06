# Installation

## Prerequisite

- Python 3.10 or above

## Instructions

1. Download the source from Github:

```bash
$ git clone https://github.com/sunyzm/geostats.git
```

2. Setup Python venv:

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

3. Install [`gquery`](https://github.com/sunyzm/gquery) package from GitHub:
```bash
$ pip install git+https://github.com/sunyzm/gquery.git
```

Alternative, you can download `gquery` package to a local directory, and install it in editable mode:
```bash
$ git clone https://github.com/sunyzm/gquery.git
$ pip install -e PATH/TO/GQUERY/PACKAGE
```

4. Install `flask`:
```bash
$ pip install flask
```

# Usage
Start the server:

```
$ flask --app server run
```
