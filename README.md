
# How to build

## Prerequisites

1. Xcode

Standard IDE for building iOS and OSX apps on Mac. Can be downloaded from AppStore

2. Python development environment

Should be installed by default on any Mac.

3. PIP

Python package manager. can be installed by executing the following line in Terminal:
```
# sudo easy_install pip
```

4. lxml for Python

LibXml library for Python. Can be installed using PIP by executing the following line in Terminal:
```
# sudo pip install lxml
```

## Building

Just run from the project's root folder
```
# python setup.py py2app
```

If everything is ok, this should produce an app package in dist/ folder.

# Disclaimer

Gatherer algorithm is borrowed from https://github.com/carpeamentum/GathererScraper