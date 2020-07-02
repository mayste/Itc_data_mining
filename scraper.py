# from command_args import args

# TODO: try to find better address

# SLEEP_FACTOR = args.sleep_factor


from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from element_id import id_job_title_kw, id_job_title_location, id_search_button
from path import DEFAULT_URL, EXE_PATH, pop_up_xpath, num_pages_xpath, next_xpath
import time
from constants import SLEEP_TIME, LAST_ELEMENT, FIRST_ELEMENT


class Scraper():
    """
       Contains functions related to scraping the website.
       """

    def __init__(self):
        """
        Sets up the default URL.
        """
        self.URL = (DEFAULT_URL)


    def create_driver(self):
        """
        Returns:
        driver -- a Firefox webdriver.
        """
        firefox_options = webdriver.FirefoxOptions()
        browser = webdriver.Firefox(firefox_options=firefox_options, executable_path=EXE_PATH)
        browser.maximize_window()
        browser.get(self.URL)

        return browser

    def set_search_keywords(self, browser):

        job_title = self.browser.find_element_by_id(id_job_title_kw)
        job_title.send_keys("Data science")  # TODO: ask user to input job title

        location = self.browser.find_element_by_id(id_job_title_location)
        location.clear()
        location.send_keys('Israel')  # TODO: ask user to input job location

        try:
            pop_up = self.browser.find_element_by_xpath(pop_up_xpath)
            pop_up.click()
        except NoSuchElementException:
            pass

        search_button = self.browser.find_element_by_id(id_search_button)
        search_button.click()

        current_url = self.browser.current_url  # how to get the url ?

        time.sleep(SLEEP_TIME)

        return current_url


    def get_num_pages(self, current_url):

        self.browser.get(current_url)

        try:
            # take the number of all open positions in Israel over the site
            num_of_available_pages = self.browser.find_element_by_xpath(num_pages_xpath).text
            num_of_available_pages = int(num_of_available_pages.split(' ')[LAST_ELEMENT])

        except ElementClickInterceptedException:
            num_of_available_pages = 1  # default value
            print(
                f'Their is a problem trying to get the number of available pages of jobs post, by default the number of '
                f'available pages of jobs post to scrap will be {num_of_available_pages}')

        time.sleep(SLEEP_TIME)

        return num_of_available_pages


    def generate_pages_links(self, current_url, num_of_available_pages):
        # call page_analysis to scrap the first page and also save first page address
        # here implement click next and save a list with new url format from page 2 until number of pages
        # send this list to page _analysis

        self.browser.get(current_url)

        list_url = []

        try:
            next_button = self.browser.find_element_by_xpath(next_xpath)
            next_button.click()
        except NoSuchElementException:
            print(f"Not succeed to click on next")

        time.sleep(SLEEP_TIME)

        new_url = self.browser.current_url

        current_page = 1

        while current_page < num_of_available_pages:
            URL = new_url.split('IP')[FIRST_ELEMENT] + 'IP' + str(current_page) + '.htm'
            list_url.append(URL)
            current_page += 1

        return list_url
