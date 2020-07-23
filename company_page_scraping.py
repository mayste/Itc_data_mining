from selenium.common.exceptions import ElementClickInterceptedException
import logging
import time
from scraper import Scraper
import configparser

class CompanyPageScraper(Scraper):
    """
    This class contains specific functions to scrape the company page on the website.
    Authors: May Steinfeld & Sheryl Sitruk
    """
    def __init__(self, geckodriver_path, competitor_name):
        """
        Sets up the default URL.
        """
        Scraper.__init__(self, geckodriver_path)
        self.competitor_name = competitor_name
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('Constants')


    def set_search_keywords(self):
        """
        This function allows to search a specific company page (competitor)
        """
        self.browser.get(self.config['Path']['DEFAULT_URL'])
        logging.info(self.config['General']['BROWSER_CONNECTION'])

        self.browser.find_element_by_xpath(self.config['Path']['COMPANY_XPATH']).click()

        company_name = self.browser.find_element_by_id(self.config['ID']['ID_JOB_TITLE_KW'])
        company_name.clear()  # clear if something is already written
        company_name.send_keys(self.competitor_name)

        location = self.browser.find_element_by_id(self.config['ID']['ID_JOB_LOCATION_KW'])
        location.clear()  # clear if something is already written
        logging.info(self.config['General']['COMPETITOR_PAGE'])
        self.close_popup()

        # Click on search button
        search_button = self.browser.find_element_by_id(self.config['ID']['ID_SEARCH_BUTTON'])
        search_button.click()
        logging.info(self.config['General']['NEW_COMPANY_URL'])
        time.sleep(int(self.config['Constant']['SLEEP_TIME']))

    def enter_company_page(self, company):
        """
        This function click on the first company name and enter the page
        """
        try:
            self.browser.find_element_by_xpath(self.config['Path']['FIRST_COMPANY_XPATH']).click()
        except ElementClickInterceptedException:
            logging.exception(self.config['General']['X_PATH_FAIL'])
            pass
        finally:
            return self.catch_company_data(company)

    def catch_company_data(self, company):
        """
        This function catch all the data on a company page
        :param company: Company
        :return: Company
        """
        time.sleep(int(self.config['Constant']['SLEEP_TIME']))
        # Catch company size information
        company.set_company_size(self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_SIZE_XPATH']))
        # Catch founded year of company
        company.set_company_founded(self.convert_company_founded_year(self.catch_optional_text_value_by_xpath(
            self.config['Path']['COMPANY_FOUNDED_XPATH'])))
        # Catch company industry
        company.set_company_industry(self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_INDUSTRY_XPATH']))
        # Catch company type
        company_type = self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_TYPE_XPATH'])
        if company_type is not None and self.config['Constant']['DASH'] in company_type:
            company_type = company_type.split(self.config['Constant']['DASH'])[int(self.config['Constant']['SECOND_ELEMENT'])].strip()
            company.set_company_type(company_type)
        else:
            company.set_company_type(company_type)

        # Catch company revenue
        company.set_company_revenue(self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_REVENUE_XPATH']))
        # Catch company headquarters
        company.set_company_headquarters(self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_HEADQUARTER_XPATH']))
        #catch company rating
        company.set_company_rating(self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_RATING_XPATH']))
        self.browser.quit()
        logging.info(self.config['General']['BROWSER_CLOSE'])
        return company


