# Data mining project on Itc bootcamp

This is the first checkpoint of our Data mining project on Glassdoor. 

This website is full of jobs offers from different companies around the world.
In our case, we focused on all the jobs offers in Israel and use Selenium to scarp information about them as:
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

As Glassdoor tried to block us many time, we tried to mimic a real scrolling over the website and used a lot of sleep calls with 5 seconds (depending on the computer and the bandwidth of the network).
After Selenium finished to catch the data from each page we save it to our csv file, so even if Glassdoor blocks us we will have part of the data.

Before our main loop, we catch the number of open positions in the website and try to run until it catch everything or until Glassdoor blocks us (whatever happens first).

Our main goal at this stage was to catch all the data we need. 
We choose to focus on job posts in order to find intersting information about what are the most demanding jobs right now after the Covid-19 virus in Israel, and make comparaison between small companies and large one. etc.

## Requirements:

In order to run Selenium, we need to install first a WebDriver (we choose to run over Chrome browser).
The WebDrive installation is inside our GitHub and also over this link:
https://chromedriver.chromium.org/downloads

### Requirements.txt
decorator==4.4.2
numpy==1.18.5
pandas==1.0.4
public==2019.4.13
python-dateutil==2.8.1
pytz==2020.1
selenium==3.141.0
self==2019.4.13
six==1.15.0
urllib3==1.25.9
