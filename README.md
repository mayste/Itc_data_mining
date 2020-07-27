# Data mining project on Itc bootcamp

This is our Data mining project on Glassdoor. 

This website is full of jobs offers from different companies around the world.
In our case, the user can enter specific keywords for job title and location and use Selenium to scarp information about them as:
- Company Name
- Job Title
- Job Description
- Job Location
- Publication Date
- Company Size
- Founding Date
- Company Industry
- Company Sector
- Company Type
- Company Rating
- Competitors
- Revenue
- Headquarters

As Glassdoor tried to block us many time, we tried to mimic a real scrolling over the website and used a lot of sleep calls with random time.
After Selenium finished to catch the data from each job and company we save it to our MySQL DB, so even if Glassdoor blocks us we will have part of the data.

Our main goal at this stage was to catch all the data we need and create a DB. 
We choose to focus on job posts in order to find intersting information about what are the most demanding jobs right now after the Covid-19 virus, and make comparaison between small companies and large one. etc.

In addition, we used the Google places API to add more information to our database regarding the job location: Full address, Longitude and Latitude of job offers.

## DB design:
![image](https://user-images.githubusercontent.com/66407270/88477795-aa9af400-cf4b-11ea-9864-504b043fe1d1.png)

## Requirements:

In order to run Selenium, we need to install first a WebDriver (we choose to run over Firefox browser).
The WebDrive installation is inside our GitHub and also over this link:
https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

In order to run the Google Places API you must have an API key, you can sign in and get one through this link: 
https://developers.google.com/maps/gmp-get-started

### Requirements.txt
* certifi==2020.6.20
* chardet==3.0.4
* configparser==5.0.0
* decorator==4.4.2
* idna==2.10
* numpy==1.18.5
* pandas==1.0.4
* public==2019.4.13
* PyMySQL==0.9.3
* python-dateutil==2.8.1
* pytz==2020.1
* requests==2.24.0
* selenium==3.141.0
* self==2019.4.13
* six==1.15.0
* urllib3==1.25.9

## Installation:
```python
git clone https://github.com/mayste/Itc_data_mining.git
pip3 install -r requirments.txt
```

## Run:
Optional arguments are job title & job location, if the user don't enter them- the program will run for every job and location around the world.
```python
run main_glassdoor.py <path to geckodriver> <MySQL user name> <MySQL password> <Key API> --job_title="XXX" --job_location="XXX"
```
