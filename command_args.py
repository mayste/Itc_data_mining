import argparse

# receiving arguments from the command line terminal for the scraping process
parser = argparse.ArgumentParser(description='Scraping jobs position from Glassdoor website')
parser.add_argument('driver_path', help="Enter the path of you firefox webdriver", type=str)
parser.add_argument('job_location', help="Job location to scrap", type=str,
                    choices=['Israel', 'USA', 'UK', 'Canada'])
parser.add_argument('--job_title', help="Job position to scrap", type=str, default=' ',
                    choices={'Data Scientist', 'Data Analyst', 'Marketing', 'Product Manager', 'Finance', 'Accounting'})

# parser.add_argument('--sleep_factor', help="Sleep factor in sec between requests, default=5", default=5, type=int)

args = parser.parse_args()
