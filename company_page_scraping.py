from selenium.common.exceptions import ElementClickInterceptedException
import logging
import time
from scraper import Scraper
import constants as cst
import text_messages as tm


class CompanyPageScraper(Scraper):
    def __init__(self, competitor_name):
        """
        Sets up the default URL.
        """
        Scraper.__init__(self)
        self.competitor_name = competitor_name

    def set_search_keywords(self):
        """
        This function allows to search a specific job title and location according to the
        input of the user on the command line
        """
        self.browser.get(cst.DEFAULT_URL)
        logging.info(tm.BROWSER_CONNECTION)

        self.browser.find_element_by_xpath(cst.COMPANY_XPATH).click()

        company_name = self.browser.find_element_by_id(cst.ID_JOB_TITLE_KW)
        company_name.clear()  # clear if something is already written
        company_name.send_keys(self.competitor_name)

        location = self.browser.find_element_by_id(cst.ID_JOB_LOCATION_KW)
        location.clear()  # clear if something is already written
        logging.info(tm.COMPETITOR_PAGE)
        self.close_popup()

        # Click on search button
        search_button = self.browser.find_element_by_id(cst.ID_SEARCH_BUTTON)
        search_button.click()
        logging.info(tm.NEW_COMPANY_URL)
        time.sleep(cst.SLEEP_TIME)

    def enter_company_page(self, company):
        """
        This function click on a company name an take all information on the page
        """
        try:
            self.browser.find_element_by_xpath(cst.FIRST_COMPANY_XPATH).click()
        except ElementClickInterceptedException:
            logging.exception(f'There is a problem with click on xpath: {cst.FIRST_COMPANY_XPATH}')
            pass
        finally:
            return self.catch_company_data(company)

    def catch_company_data(self, company):
        """
        This function catch all the data on a company page
        """
        time.sleep(cst.SLEEP_TIME)
        # Catch company size information
        company.set_company_size(self.catch_optional_text_value_by_xpath(cst.COMPANY_SIZE_XPATH))
        # Catch founded year of company
        company.set_company_founded(self.convert_company_founded_year(self.catch_optional_text_value_by_xpath(
            cst.COMPANY_FOUNDED_XPATH)))
        # Catch company industry
        company.set_company_industry(self.catch_optional_text_value_by_xpath(cst.COMPANY_INDUSTRY_XPATH))
        # Catch company type
        company_type = self.catch_optional_text_value_by_xpath(cst.COMPANY_TYPE_XPATH)
        if company_type is not None and '-' in company_type:
            company_type = company_type.split('-')[cst.SECOND_ELEMENT].strip()
            company.set_company_type(company_type)
        else:
            company.set_company_type(company_type)

        # Catch company revenue
        company.set_company_revenue(self.catch_optional_text_value_by_xpath(cst.COMPANY_REVENUE_XPATH))
        # Catch company headquarters
        company.set_company_headquarters(self.catch_optional_text_value_by_xpath(cst.COMPANY_HEADQUARTER_XPATH))
        #catch company rating
        company.set_company_rating(self.catch_optional_text_value_by_xpath(cst.COMPANY_RATING_XPATH))
        self.browser.quit()
        logging.info('close browser successfully')
        return company


