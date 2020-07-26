from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
from dateutil.relativedelta import relativedelta
from datetime import date
from job import Job
from company import Company
import logging
import sys
from scraper import Scraper
from company_page_scraping import CompanyPageScraper
import configparser
import API
import random



class JobsListScraper(Scraper):
    """
       This class contains specific functions to scrape the job list part on the website.
       Authors: May Steinfeld & Sheryl Sitruk
    """

    def __init__(self, geckodriver_path, key_api, keyword_job_title, keyword_job_location):
        """
        Sets up the default URL.
        """
        Scraper.__init__(self, geckodriver_path)
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('Constants')
        self.key_api = key_api
        self.keyword_job_title = keyword_job_title
        self.keyword_job_location = keyword_job_location
        self.geckodriver_path = geckodriver_path

    def set_search_keywords(self):
        """
        This function allows to search a specific job title and location according to the
        input of the user on the command line
        """
        self.browser.get(self.config['Path']['DEFAULT_URL'])
        logging.info(self.config['General']['BROWSER_CONNECTION'])

        job_title = self.browser.find_element_by_id(self.config['ID']['ID_JOB_TITLE_KW'])
        job_title.clear()  # clear if something is already written
        job_title.send_keys(self.keyword_job_title)
        logging.info(self.config['General']['SEARCH_JOB'])

        location = self.browser.find_element_by_id(self.config['ID']['ID_JOB_LOCATION_KW'])
        location.clear()  # clear if something is already written
        location.send_keys(self.keyword_job_location)
        logging.info(self.config['General']['SEARCH_LOCATION'])
        time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                  int(self.config['Constant']['SLEEP_TIME_MAX'])))
        self.close_popup()

        # Click on search button
        search_button = self.browser.find_element_by_id(self.config['ID']['ID_SEARCH_BUTTON'])
        search_button.click()
        logging.info(self.config['General']['CONNECT_NEW_URL'])
        time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                  int(self.config['Constant']['SLEEP_TIME_MAX'])))

    def get_num_pages(self):
        """
        Get the number of available pages for a specific job and location
        :return: integer
        """

        try:
            # take the number of all open positions in Israel over the site
            num_of_available_pages = self.browser.find_element_by_xpath(self.config['Path']['NUM_PAGES_XPATH']).text
            num_of_available_pages = int(num_of_available_pages.split(' ')[int(self.config['Constant']
                                                                               ['LAST_ELEMENT'])])
            logging.info(self.config['General']['AVAILABLE_PAGES'])

        except NoSuchElementException:
            logging.critical(self.config['General']['ERROR_NUM_PAGES'])
            self.browser.quit()
            sys.exit(int(self.config['General']['EXIT']))
        return num_of_available_pages

    def convert_publication_date(self, publication_date):
        """
        Take a publication date and convert into format Year-Month-Day
        :param publication_date: string
        :return: date
        """
        # if the job has been published this day print the day of today
        if self.config['Constant']['HOUR'] in publication_date and \
                self.config['Constant']['ALL_DAY'] not in publication_date:
            return date.today()
        elif self.config['Constant']['HOUR'] in publication_date and \
                self.config['Constant']['ALL_DAY'] in publication_date:
            return date.today() - relativedelta(days=int(self.config['Constant']['ONE_DAY']))
        elif self.config['Constant']['DAY'] in publication_date:
            return (date.today() - relativedelta(
                days=int(publication_date.split(self.config['Constant']['DAY'])[int(self.config['Constant']
                                                                                    ['FIRST_ELEMENT'])])))
        elif self.config['Constant']['MONTH'] in publication_date:
            return (date.today() - relativedelta(
                months=int(publication_date.split(self.config['Constant']['MONTH'])[int(self.config['Constant']
                                                                                        ['FIRST_ELEMENT'])])))
        else:
            return None

    def convert_split_name_and_rating(self, company_name):
        """
        The function split the company name to name + rating if we have one
        :param company_name: string
        :return: tuple
        """
        if '\n' in company_name:  # We have a rating
            try:
                company_rating = float(company_name.split('\n')[int(self.config['Constant']['SECOND_ELEMENT'])])
            except ValueError:
                logging.exception(self.config['General']['CONVERT_RATING_FAIL'])
                company_rating = None
            finally:
                company_name = company_name.split('\n')[int(self.config['Constant']['FIRST_ELEMENT'])]
                if company_name.lower().split(' ')[int(self.config['Constant']['LAST_ELEMENT'])] \
                        in list(self.config['Constant']['CORPORATION']):
                    company_name = ''.join(company_name.lower().split(' ')[:int(self.config['Constant']
                                                                                ['LAST_ELEMENT'])])
        else:  # No rating
            company_rating = None
        return company_name, company_rating

    def catch_mandatory_data_and_rating(self, button_job):
        """
        Collect all the mandatory information on the website
        :param button_job:
        :return: tuple
        """
        #Check if sleep time work
        time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                  int(self.config['Constant']['SLEEP_TIME_MAX'])))
        collect_mandatory = False
        while not collect_mandatory:
            # click the job button
            button_job.click()
            try:
                # Catch the publication date and call function to convert publication date
                job_publication_date = self.convert_publication_date(self.browser.find_element_by_xpath(
                    self.config['Path']['PUBLICATION_DATE_XPATH']).text)
                time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                          int(self.config['Constant']['SLEEP_TIME_MAX'])))

                # Collect Company Name from a post, Sometimes: company name and rating are join, we need to split
                # them into Company Name and Rating
                company_name, company_rating = self.convert_split_name_and_rating(self.browser.find_element_by_xpath(
                    self.config['Path']['COMPANY_NAME_XPATH']).text)

                # Collect Job Title from a post
                job_title = self.browser.find_element_by_xpath(self.config['Path']['JOB_TITLE_XPATH']).text

                # Collect Job Location from a post
                job_location = self.browser.find_element_by_xpath(self.config['Path']['JOB_LOCATION_XPATH']).text

                # Collect Job Description
                job_description = self.browser.find_element_by_xpath(self.config['Path']['JOB_DESCRIPTION_XPATH']).text

                # finish collect mandatory fields + rating if the company has in the name
                collect_mandatory = True
                job = Job(job_title, job_description, job_location, job_publication_date, company_name)
                company = Company(company_name, company_rating)
                return job, company

            except NoSuchElementException:
                logging.exception(self.config['General']['MANDATORY_DATA_FAIL'])
                time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                          int(self.config['Constant']['SLEEP_TIME_MAX'])))

    def catch_optional_data(self, company):
        """
        Catch all the optional information of a company
        :param company: Company
        :return: Company
        """

        # Collect optional information
        try:
            # Click on company in the hyper details
            self.browser.find_element_by_xpath(self.config['Path']['OVERVIEW_XPATH']).click()
            time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                      int(self.config['Constant']['SLEEP_TIME_MAX'])))

            # Catch company size information
            company.set_company_size(self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_SIZE_XPATH']))
            # Catch founded year of company
            company.set_company_founded(self.convert_company_founded_year(self.catch_optional_text_value_by_xpath(
                self.config['Path']['COMPANY_FOUNDED_XPATH'])))
            # Catch company industry
            company.set_company_industry(self.catch_optional_text_value_by_xpath(self.config['Path']
                                                                                 ['COMPANY_INDUSTRY_XPATH']))
            # Catch company sector
            company.set_company_sector(self.catch_optional_text_value_by_xpath(self.config['Path']
                                                                               ['COMPANY_SECTOR_XPATH']))
            # Catch company type
            company_type = self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_TYPE_XPATH'])
            if company_type is not None and self.config['Constant']['DASH'] in company_type:
                company_type = company_type.split(self.config['Constant']['DASH'])[int(self.config['Constant']
                                                                                       ['SECOND_ELEMENT'])].strip()
                company.set_company_type(company_type)
            else:
                company.set_company_type(company_type)

            # Catch company revenue
            company.set_company_revenue(self.catch_optional_text_value_by_xpath(self.config['Path']
                                                                                ['COMPANY_REVENUE_XPATH']))
            # Catch company headquarters
            company.set_company_headquarters(self.catch_optional_text_value_by_xpath(self.config['Path']
                                                                                     ['COMPANY_HEADQUARTER_XPATH']))

            competitors = self.catch_optional_text_value_by_xpath(self.config['Path']['COMPANY_COMPETITORS_XPATH'])
            if competitors is not None and self.config['Constant']['COMA'] in competitors:
                competitors = competitors.split(self.config['Constant']['COMA'])
            elif competitors is not None:  # single competitor
                competitors = competitors.split()
            company.set_company_competitors(competitors)

        # If there is no overview page(company tab)
        except NoSuchElementException:
            logging.error(self.config['General']['ERROR_OPTIONAL_DATA'])
        finally:
            return company

    def click_next_button(self, current_page):
        """
        get the current page number, click on next button and update the current page
        :param current_page: int
        :return: int
        """
        try:
            next_button = self.browser.find_element_by_xpath(self.config['Path']['NEXT_XPATH'])
            next_button.click()
            logging.info(self.config['General']['NEXT_SUCCESS'])
        except NoSuchElementException:
            logging.exception(self.config['General']['ERROR_NEXT'])
        time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                  int(self.config['Constant']['SLEEP_TIME_MAX'])))
        current_page += int(self.config['Constant']['SECOND_ELEMENT'])
        return current_page

    def create_competitors_insert(self, database, company):
        """
        get database instance and company and insert the competitors to DB & update competitors table
        :param database:
        :param company:
        :return:
        """
        if company.get_company_competitors() is not None:
            for competitor_name in company.get_company_competitors():
                competitor_name = competitor_name.strip()
                if competitor_name.lower().split(' ')[int(self.config['Constant']['LAST_ELEMENT'])] \
                        in self.config['Constant']['CORPORATION']:
                    competitor_name = ' '.join(competitor_name.lower().split(' ')[:int(self.config['Constant']
                                                                                       ['LAST_ELEMENT'])])
                if not database.get_company(competitor_name):  # we don't have the competitor in DB
                    competitor = Company(competitor_name, None)
                    competitor_scraping = CompanyPageScraper(self.geckodriver_path, competitor_name)
                    competitor_scraping.set_search_keywords()
                    competitor = competitor_scraping.enter_company_page(competitor)
                    competitor.set_company_sector(company.get_company_sector())
                    database.insert_company(competitor)
                    if competitor.get_company_sector():
                        database.insert_company_sector(competitor)
                    if competitor.get_company_type():
                        database.insert_company_type(competitor)
                    if competitor.get_company_industry():
                        database.insert_company_industry(competitor)
                database.insert_competitor(competitor_name, company)


    def collecting_data_from_pages(self, database):
        """
        Collect all the data on a specific search
        """
        time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                  int(self.config['Constant']['SLEEP_TIME_MAX'])))
        self.close_popup()

        glassdoor_number_pages = self.get_num_pages()

        try:
            self.browser.find_element_by_xpath(self.config['Path']['SELECTED_XPATH']).click()
        except ElementClickInterceptedException:
            logging.exception(self.config['General']['SELECTED_XPATH'])
            pass

        time.sleep(random.randint(int(self.config['Constant']['SLEEP_TIME_MIN']),
                                  int(self.config['Constant']['SLEEP_TIME_MAX'])))

        # Take all the buttons of each job in this page we want to click on
        current_page = int(self.config['Constant']['FIRST_PAGE'])
        while current_page <= glassdoor_number_pages:
            job_click_button = self.browser.find_elements_by_xpath(self.config['Path']['JOB_CLICK_BUTTON_XPATH'])
            self.close_popup()
            logging.info(self.config['General']['COLLECT_DATA'])
            for button_job in job_click_button:
                # start collect job data
                job, company = self.catch_mandatory_data_and_rating(button_job)
                company = self.catch_optional_data(company)
                database.insert_company(company)
                if company.get_company_sector():
                    database.insert_company_sector(company)
                if company.get_company_type():
                    database.insert_company_type(company)
                if company.get_company_industry():
                    database.insert_company_industry(company)
                self.create_competitors_insert(database,company)
                database.insert_job(job)
                google_api_info = API.create_api_connect(company.get_name(), job.get_location(), self.key_api)
                if (not google_api_info.get_address_google()) or (self.config['Constant']['UNNAMED']
                                                                  in google_api_info.get_address_google()):
                    google_api_info.set_address_google(job.get_location())
                database.insert_job_location(google_api_info)
            logging.info(self.config['General']['COLLECT_DATA_SUCCESS'])
            # call to click on next button
            current_page = self.click_next_button(current_page)
