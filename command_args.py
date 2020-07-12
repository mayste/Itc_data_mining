"""
All the argparse options
Authors: May Steinfeld & Sheryl Sitruk
"""

import argparse

# receiving arguments from the command line terminal for the scraping process
parser = argparse.ArgumentParser(description='Scraping jobs position from Glassdoor website')
parser.add_argument('driver_path', help="Enter the path of your firefox webdriver", type=str)
parser.add_argument('database_user', help="Enter your MySQL user", type=str)
parser.add_argument('database_password', help="Enter your MySQL password", type=str)
parser.add_argument('--job_location', help="Choose a job location to scrap", type=str, default=' ')
parser.add_argument('--job_title', help="Choose a job to scrap", type=str, default=' ')
args = parser.parse_args()
