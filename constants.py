"""
All constants
Authors: May Steinfeld & Sheryl Sitruk
"""

import random

# Constant
SLEEP_TIME = random.randint(5, 10)
LAST_ELEMENT = -1
FIRST_ELEMENT = 0
DEFAULT_NUM_PAGES = 1
FIRST_PAGE = 1
SPLIT_URL = 'IP'
END_URL = '.htm'
HOUR = 'h'
DAY = 'd'
MONTH = 'm'
ALL_DAY = '24'
ONE_DAY = 1
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
SECOND_ELEMENT = 1
ZERO_VALUE = 0
UNKNOWN_INFO = 'unknown'
HOST = 'localhost'
CHARSET = 'utf8mb4'
LOGGING_DIR_NAME = 'logging'
CORPORATION = ['corp','corporation','corp.']
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_FILE = 'glassdoor_scrap_'
LOG = '.log'
FILE_MODE = 'w'
SPACE = ' '
NEW_LINE = '\n'
DASH = '-'
COMA = ','
EXIT = 1

# Path
DEFAULT_URL = "https://www.glassdoor.com/Job/index.htm"
POP_UP_XPATH = "//div[contains(@class,'modal_main')]//span[@class='SVGInline modal_closeIcon']"
NUM_PAGES_XPATH = "//div[@class='cell middle hideMob padVertSm']"
NEXT_XPATH = '//li[@class="next"]//a[@data-test="pagination-next"]'
PUBLICATION_DATE_XPATH = "//li[contains(@class,'selected')]//div[@class='jobContainer']//div[@data-test='job-age']"
COMPANY_NAME_XPATH = '//div[@class="employerName"]'
JOB_TITLE_XPATH = '//div[@class="title"]'
JOB_LOCATION_XPATH = '//div[@class="location"]'
JOB_DESCRIPTION_XPATH = '//div[@class="jobDescriptionContent desc"]'
OVERVIEW_XPATH = '//div[@class="tab" and @data-tab-type="overview"]'
COMPANY_SIZE_XPATH = '//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*'
COMPANY_FOUNDED_XPATH = '//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*'
COMPANY_INDUSTRY_XPATH = '//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*'
COMPANY_SECTOR_XPATH = '//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*'
COMPANY_TYPE_XPATH = '//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*'
COMPANY_COMPETITORS_XPATH = '//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*'
COMPANY_REVENUE_XPATH = '//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*'
COMPANY_HEADQUARTER_XPATH = '//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*'
SELECTED_XPATH = "//li[contains(@class, 'selected')]"
JOB_CLICK_BUTTON_XPATH = "//li[contains(@class, 'job-listing')]"
COMPANY_XPATH ="//div[@class='context-choice-tabs-box']//li[@class='col-3 reviews ']"
FIRST_COMPANY_XPATH = '//div[@class="single-company-result module "][1]//div[@class="col-9 pr-0"]//h2//a'
COMPANY_RATING_XPATH = '//div[@class="v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large"]'

# element id
ID_JOB_TITLE_KW = "KeywordSearch"
ID_JOB_LOCATION_KW = "LocationSearch"
ID_SEARCH_BUTTON = "HeroSearchButton"

