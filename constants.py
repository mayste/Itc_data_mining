import random

# Constant
CONSTANT_DICT = {'HOST':'localhost','CHARSET':'utf8mb4'}

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
FIRST = 1


# Path
DEFAULT_URL = f'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0 '
# EXE_PATH = r'/Users/Sheryl/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
# EXE_PATH = r'/Users/maylev/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
POP_UP_XPATH = "//div[contains(@class,'modal_main')]//span[@class='SVGInline modal_closeIcon']"
NUM_PAGES_XPATH = "//div[@class='cell middle hideMob padVertSm']"
NEXT_XPATH = '//li[@class="next"]//a[@data-test="pagination-next"]'
publication_date_xpath = "//li[contains(@class,'selected')]//div[@class='jobContainer']//div[@data-test='job-age']"
company_name_xpath = '//div[@class="employerName"]'
job_title_xpath = '//div[@class="title"]'
job_location_xpath = '//div[@class="location"]'
job_description_xpath = '//div[@class="jobDescriptionContent desc"]'
overview_xpath = '//div[@class="tab" and @data-tab-type="overview"]'
company_size_xpath = '//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*'
company_founded_xpath = '//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*'
company_industry_xpath = '//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*'
company_sector_xpath = '//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*'
company_type_xpath = '//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*'
company_competitors_xpath = '//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*'
company_revenue_xpath = '//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*'
company_headquarters_xpath = '//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*'
selected_xpath = "//li[contains(@class, 'selected')]"
job_click_button_xpath = "//li[contains(@class, 'job-listing')]"

# element id
id_job_title_kw = "sc.keyword"
id_job_title_location = "sc.location"
id_search_button = "HeroSearchButton"

# Error message
ERROR_NUM_PAGES = """f'Their is a problem trying to get the number of available pages of jobs post, by default the number of '
                f'available pages of jobs post to scrap will be {DEFAULT_NUM_PAGES}'"""

ERROR_NEXT = "Not succeed to click on next"

ERROR_OPTIONAL_DATA = "There is no optional data for this company on this job"
