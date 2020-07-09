from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import logging
import time
from scraper import Scraper
import constants as cst


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
        logging.info(f"Browser connect to URL")

        self.browser.find_element_by_xpath(
            "//div[@class='context-choice-tabs-box']//li[@class='col-3 reviews ']").click()

        company_name = self.browser.find_element_by_id(cst.ID_JOB_TITLE_KW)
        company_name.clear()  # clear if something is already written
        company_name.send_keys(self.competitor_name)

        location = self.browser.find_element_by_id(cst.ID_JOB_LOCATION_KW)
        location.clear()  # clear if something is already written
        logging.info(f"Search for competitor's company page")
        self.close_popup()

        # Click on search button
        search_button = self.browser.find_element_by_id(cst.ID_SEARCH_BUTTON)
        search_button.click()
        logging.info(
            f"Browser connect to new URL of a company")
        time.sleep(cst.SLEEP_TIME)

    def enter_company_page(self, company):
        try:
            self.browser.find_element_by_xpath('//div[@class="single-company-result module "][1]//div[@class="col-9 pr-0"]//h2//a').click()
        except ElementClickInterceptedException:
            pass
        finally:
            return self.catch_company_data(company)

    def catch_company_data(self, company):
        # Collect optional information
        time.sleep(cst.SLEEP_TIME)
        try:
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
            company.set_company_rating(self.catch_optional_text_value_by_xpath('//div[@class="v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__large"]'))
        except NoSuchElementException:
            logging.error(cst.ERROR_OPTIONAL_DATA)
        finally:
            self.browser.quit()
            return company


