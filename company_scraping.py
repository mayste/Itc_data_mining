from selenium.common.exceptions import NoSuchElementException
from scraper import Scraper
import logging
import time
import constants as cst


class CompanyPage(Scraper):
    def __init__(self, competitor_name):
        Scraper.__init__(self)
        self.competitor_name = competitor_name

    def set_search_keywords(self):
        """
        This function allows to search a specific job title and location according to the
        input of the user on the command line
        """
        self.browser.get(cst.DEFAULT_URL)
        logging.info(f"Browser connect to URL")

        self.browser.find_element_by_xpath(
            "//div[@class='context-choice-tabs-box']//li[@class='col-3 reviews ']").click()
        company_name = self.browser.find_element_by_id(cst.ID_JOB_TITLE_KW)
        company_name.clear()  # clear if something is already written
        company_name.send_keys(self.competitor_name)

        location = self.browser.find_element_by_id(cst.ID_JOB_LOCATION_KW)
        location.clear()  # clear if something is already written
        logging.info(f"Search for competitor's company page: {self.competitor_name}")
        try:
            # Close pop up
            pop_up = self.browser.find_element_by_xpath(cst.POP_UP_XPATH)
            pop_up.click()
        except NoSuchElementException:
            pass

        # Click on search button
        search_button = self.browser.find_element_by_id(cst.ID_SEARCH_BUTTON)
        search_button.click()
        logging.info(
            f"Browser connect to new URL of a company with : {self.competitor_name}")
        time.sleep(cst.SLEEP_TIME)
