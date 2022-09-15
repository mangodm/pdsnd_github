# Explore US Bikeshare Data

## Overview
This repo contains an interactive program which lets users explore data related to bike-sharing systems for three cities in the United States - Chicago, New York City, and Washington. The program helps users to understand the features of bike share usage patterns in three cities. Here are some key information provided in the program:

**1. Popular times of travel** (i.e., occurs most often in the start time)
- most common month
- most common day of week
- most common hour of day

**2. Popular stations and trip**
- most common start station
- most common end station
- most common trip from start to end (i.e., most frequent combination of start station and end station)

**3. Trip duration**
- total travel time
- average travel time

**4. User info**
- counts of each user type
- counts of each gender (only available for NYC and Chicago)
- earliest, most recent, most common year of birth (only available for NYC and Chicago)

## Data used

To get the statistics, three CSV files(`chicago.csv`, `new_york_city.csv`, and `washington.csv`) containing the bike share usage patterns were used and they were provided by [Motivate](https://www.motivateco.com/), a bike share system provider for many major cities in the United States.

The datasets include data for the first six months of 2017. All three files contain the following six columns:

- `Start Time`: The date and time of check-out (e.g., 2017-01-01 00:07:57)
- `End Time`: The date and time of return (e.g., 2017-01-01 00:20:53)
- `Trip duration`: The elapsed rental time in seconds (e.g., 776)
- `Start Station`: The name of station where the bike was checked out (e.g., Broadway & Barry Ave)
- `End Station`: The name of station where the bike was returned (e.g., Sedgwick St & North Ave)
- `User Type`: A string code signifying the user type (Subscriber or Customer)

The *Chicago* and *New York City* files have the following two more columns:
- `Gender`: The gender of user (if available)
- `Birth Year`: The birth year of user (if available)

## Environment

To run this project, please install:
- [Python 3.7 or above](https://www.python.org/downloads/release/python-370/)

## How to run it 

From your project directory, type the following command:
```bash
pip install -r requirements.txt
```

This installs all of the modules (i.e. Pandas only) listed in the requirements file into the project environment.

To run the program, type the following command:
```bash
python3 bikeshare.py
```

If everything is okay, it will start the program with a message, "Hello! Let's explore some US bikeshare data!". 