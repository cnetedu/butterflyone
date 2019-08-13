# Status of Project
[![CircleCI](https://circleci.com/gh/butterflyone/butterflyone.svg?style=svg)](https://circleci.com/gh/butterflyone/butterflyone)

# Structure of Application
## V1 - iOS Application

* Data - Data is currently stored in MySQL backend
* APIs - APIs are served by a python flask backend
* Mobile - iOS application written in swift.

## Environment Setup
- PyCharm CE (Community) - https://www.jetbrains.com/pycharm/download/#section=mac
- iTerm - https://www.iterm2.com/
- Gcloud - https://cloud.google.com/sdk/docs/quickstart-macos
  - After putting Gcloud in the user's home directory, update your ~/.bash_profile to have the PATH include ~/google-cloud-sdk/bin/
  - run `gcloud init`
- Python3 - https://www.python.org/downloads/
- Virtualenv - `sudo pip3 install virtualenv`

# butterflyone flask app testing
To run tests.

* Create virtualenv at the base of `/webapp`.
* Activate it `. venv/bin/activate`
* Install requirements with `pip install -r requirements.txt`
* Run `pytest`


## Optional Installs
- Oh My Zsh - https://ohmyz.sh/ (lets your terminal be more useful)
- Autoswitch of virtual environments - https://github.com/MichaelAquilina/zsh-autoswitch-virtualenv (when you 'cd' into a directory with a venv/ directory, will auto activate it.)

## Iterm setup
I've set up iterm to use zsh as the default by going to iTerm2 -> Preferences -> Profiles -> Default and in the General Tab set the Command to /bin/zsh instead of Login shell.


# Zippia Data
In order to bootstrap our initial version of our application, we retrieved data from https://www.zippia.com/. We have our data currently stored in a MySQL database in google cloud. Please talk with Diego + George if there are any questions on how to access it.

## Scraped/Structured Data
The latest version of scraped/structured data exists in the following GCS bucket
https://console.cloud.google.com/storage/browser/butterflyone-data
* industries.tar.gz - A tar'd file that lists at the top an industry and then a list of urls (of jobs).
* jobs.tar.gz - All job htmls scraped from zippia.
* jobs_csvs.tgz - Job html parsed and structured in CSV.
* majors.tar.gz - All major htmls scraped from zippia.
* majors.csv - Major html parsed and structured in CSV.


There are two aspects to how we "bootstrapped" our data.

1. Retrieving the raw webpages from Zippia for Majors and Jobs
2. Structuring it in CSVs
3. Uploading the data to MySQL

All code for this is in webapp/bfly/zippia.py and webapp/bfly/zippia_data_load.py

## Retrieving raw webpages
### Majors
`webapp.zippia.major_dumps` - goes through the majors navigation page and retrieves all linked major pages. Then it dumps them onto local disk.

### Jobs
In order to find jobs we went through the industries portal in Zippia. Which groups all jobs to industries. In `webapp.zippia.industry_to_careers` we go through each industry and write all the job links into a local file.

After generating this file, `webapp.zippia.job_dumps` goes through each of the industries files and grabs the job urls, retrieves the html and writes it to local disk.

## Structuring into CSVs
`webapp.zippia.zippia_data_load` is a file that creates Job and Major objects and writes them into csvs. These csvs were then uploaded to our remote MySQL instance via MySQL Workbench.
