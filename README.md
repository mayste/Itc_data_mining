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

## DB design:
![image](https://user-images.githubusercontent.com/34678172/87239999-029b0c00-c41e-11ea-9160-59c427c8e925.png)

## Requirements:

In order to run Selenium, we need to install first a WebDriver (we choose to run over Firefox browser).
The WebDrive installation is inside our GitHub and also over this link:
https://github.com/mozilla/geckodriver/releases/tag/v0.26.0

### Requirements.txt
decorator==4.4.2
numpy==1.18.5
pandas==1.0.4
public==2019.4.13
PyMySQL==0.9.3
python-dateutil==2.8.1
pytz==2020.1
selenium==3.141.0
self==2019.4.13
six==1.15.0
urllib3==1.25.9

## Installation:
```python
git clone https://github.com/mayste/Itc_data_mining.git
pip3 install -r requirments.txt
```

## Run:
Optional arguments are job title & job location, if the user don't enter them- the program will run for every job and location around the world.
```python
run main_glassdoor.py <paath to geckodriver> <MySQL user name> <MySQL password> --job_title="XXX" --job_location="XXX"
```
