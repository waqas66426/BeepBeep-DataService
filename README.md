[![Build Status](https://travis-ci.org/giacomodeliberali/BeepBeep-DataService.svg?branch=master)](https://travis-ci.org/giacomodeliberali/BeepBeep-DataService)
[![Coverage Status](https://coveralls.io/repos/github/giacomodeliberali/BeepBeep-DataService/badge.svg?branch=master)](https://coveralls.io/github/giacomodeliberali/BeepBeep-DataService?branch=master)


# BeepBeep-DataService

The other repo of strava-worker is [https://github.com/giacomodeliberali/BeepBeep-StravaWorker](https://github.com/giacomodeliberali/BeepBeep-StravaWorker)

# Development

## Install & setup
To install dependencies and setup the app:
```
pip install -r requirements.txt
python setup.py develop
```

## Run

To run the app launch:
```
python beepbeep/dataservice/run.py
```

## Test

To run coverage launch:
```
pytest --cov-config .coveragerc --cov beepbeep/dataservice --cov-report html:cov_html
```
A new html report will be generated inside the *./cov_html* folder