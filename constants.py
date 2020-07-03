import random

# Constant
SLEEP_TIME = random.randint(5, 10)
LAST_ELEMENT = -1
FIRST_ELEMENT = 0
DEFAULT_NUM_PAGES = 1
FIRST_PAGE = 1
SPLIT_URL = 'IP'
END_URL = '.htm'

# Path
DEFAULT_URL = f'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0 '
# EXE_PATH = r'/Users/Sheryl/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
EXE_PATH = r'/Users/maylev/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
pop_up_xpath = "//div[contains(@class,'modal_main')]//span[@class='SVGInline modal_closeIcon']"
num_pages_xpath = "//div[@class='cell middle hideMob padVertSm']"
next_xpath = '//li[@class="next"]//a[@data-test="pagination-next"]'

# element id
id_job_title_kw = "sc.keyword"
id_job_title_location = "sc.location"
id_search_button = "HeroSearchButton"

# Error message
ERROR_NUM_PAGES = """f'Their is a problem trying to get the number of available pages of jobs post, by default the number of '
                f'available pages of jobs post to scrap will be {DEFAULT_NUM_PAGES}'"""

ERROR_NEXT = "Not succeed to click on next"
