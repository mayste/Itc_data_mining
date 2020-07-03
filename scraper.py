# from command_args import args

# TODO: try to find better address

# SLEEP_FACTOR = args.sleep_factor

from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
from constants import SLEEP_TIME, LAST_ELEMENT, FIRST_ELEMENT, DEFAULT_NUM_PAGES, ERROR_NUM_PAGES, ERROR_NEXT, \
    DEFAULT_URL, EXE_PATH, pop_up_xpath, num_pages_xpath, next_xpath, id_job_title_kw, id_job_title_location,\
    id_search_button, SPLIT_URL, END_URL, FIRST_PAGE
import command_args


class Scraper():
    """
       Contains functions related to scraping the website.
       """

    def __init__(self):
        """
        Sets up the default URL.
        """
        self.browser = webdriver.Firefox(executable_path=command_args.args.driver_path)
        self.browser.maximize_window()

    def set_search_keywords(self):
        self.browser.get(DEFAULT_URL)
        job_title = self.browser.find_element_by_id(id_job_title_kw)
        job_title.send_keys(command_args.args.job_title)  # TODO: ask user to input job title

        location = self.browser.find_element_by_id(id_job_title_location)
        location.clear()  # TODO: check what it does
        location.send_keys(command_args.args.job_location)  # TODO: ask user to input job location

        try:
            pop_up = self.browser.find_element_by_xpath(pop_up_xpath)
            pop_up.click()
        except NoSuchElementException:
            pass

        search_button = self.browser.find_element_by_id(id_search_button)
        search_button.click()

        time.sleep(SLEEP_TIME)

        return self.browser.current_url

    def get_num_pages(self, current_url):

        self.browser.get(current_url)

        try:
            # take the number of all open positions in Israel over the site
            num_of_available_pages = self.browser.find_element_by_xpath(num_pages_xpath).text
            num_of_available_pages = int(num_of_available_pages.split(' ')[LAST_ELEMENT])

        except ElementClickInterceptedException:
            num_of_available_pages = DEFAULT_NUM_PAGES  # default value
            print(ERROR_NUM_PAGES)

        # time.sleep(SLEEP_TIME)

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
            print(ERROR_NEXT)

        time.sleep(SLEEP_TIME)

        new_url = self.browser.current_url

        current_page = FIRST_PAGE

        while current_page <= num_of_available_pages:
            page_url = new_url.split(SPLIT_URL)[FIRST_ELEMENT] + SPLIT_URL + str(current_page) + END_URL
            list_url.append(page_url)
            current_page += 1

        self.browser.quit()
        return list_url
