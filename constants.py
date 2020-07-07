import random

# TODO: Change one file of constants + xpath + etc and one file for sql queries + one file for a text_msgs
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
DATE_FORMAT = "%Y-%m-%d"
SECOND_ELEMENT = 1
ZERO_VALUE = 0
HOST = 'localhost'
CHARSET = 'utf8mb4'

# Path
DEFAULT_URL = f'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0'
# EXE_PATH = r'/Users/Sheryl/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
# EXE_PATH = r'/Users/maylev/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
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

# element id
ID_JOB_TITLE_KW = "sc.keyword"
ID_JOB_LOCATION_KW = "sc.location"
ID_SEARCH_BUTTON = "HeroSearchButton"

# Error message
ERROR_NUM_PAGES = """f'Their is a problem trying to get the number of available pages of jobs post, by default the number of '
                f'available pages of jobs post to scrap will be {DEFAULT_NUM_PAGES}'"""

ERROR_NEXT = "Not succeed to click on next"

ERROR_OPTIONAL_DATA = "There is no optional data for this company on this job"
