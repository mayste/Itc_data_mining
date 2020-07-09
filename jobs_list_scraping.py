from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
import constants as cst
import command_args
from dateutil.relativedelta import relativedelta
from datetime import date
from job import Job
from company import Company
import logging
import sys
from scraper import Scraper
from company_page_scraping import CompanyPageScraper


class JobsListScraper(Scraper):
    """
       Contains functions related to scraping the website.
       """

    def __init__(self):
        """
        Sets up the default URL.
        """
        Scraper.__init__(self)

    def set_search_keywords(self):
        """
        This function allows to search a specific job title and location according to the
        input of the user on the command line
        """
        self.browser.get(cst.DEFAULT_URL)
        logging.info(f"Browser connect to URL")

        job_title = self.browser.find_element_by_id(cst.ID_JOB_TITLE_KW)
        job_title.clear()  # clear if something is already written
        job_title.send_keys(command_args.args.job_title)
        logging.info(f"Search for job title: {command_args.args.job_title}")

        location = self.browser.find_element_by_id(cst.ID_JOB_LOCATION_KW)
        location.clear()  # clear if something is already written
        location.send_keys(command_args.args.job_location)
        logging.info(f"Search for job location: {command_args.args.job_location}")
        time.sleep(cst.SLEEP_TIME)
        self.close_popup()

        # Click on search button
        search_button = self.browser.find_element_by_id(cst.ID_SEARCH_BUTTON)
        search_button.click()
        logging.info(
            f"Browser connect to new URL with : {command_args.args.job_title}, {command_args.args.job_location}")
        time.sleep(cst.SLEEP_TIME)

    def get_num_pages(self):
        """
        Get the number of pages availables for a specific job and location
        :param current_url: string
        :return: integer
        """

        try:
            # take the number of all open positions in Israel over the site
            num_of_available_pages = self.browser.find_element_by_xpath(cst.NUM_PAGES_XPATH).text
            num_of_available_pages = int(num_of_available_pages.split(' ')[cst.LAST_ELEMENT])
            logging.info(f'Succeed to catch number of available pages: {num_of_available_pages}')

        # TODO: click again on search if dont have job numbers
        except NoSuchElementException:
            logging.critical(cst.ERROR_NUM_PAGES)
            sys.exit(1)
        return num_of_available_pages

    def convert_publication_date(self, publication_date):
        """
        Take a publication date and convert into format Year-Month-Day
        :param publication_date: string
        :return: date
        """
        # if the job has been published this day print the day of today
        if cst.HOUR in publication_date and cst.ALL_DAY not in publication_date:
            return date.today()
        elif cst.HOUR in publication_date and cst.ALL_DAY in publication_date:
            return date.today() - relativedelta(days=1)
        elif cst.DAY in publication_date:
            return (date.today() - relativedelta(
                days=int(publication_date.split(cst.DAY)[cst.FIRST_ELEMENT])))
        elif cst.MONTH in publication_date:
            return (date.today() - relativedelta(
                months=int(publication_date.split(cst.MONTH)[cst.FIRST_ELEMENT])))
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
                company_rating = float(company_name.split('\n')[cst.SECOND_ELEMENT])
            except ValueError:
                company_rating = None
            finally:
                company_name = company_name.split('\n')[cst.FIRST_ELEMENT]
                if company_name.lower().split(' ')[-1] in ['corp','corporation','corp.'] :
                    company_name = ''.join(company_name.lower().split(' ')[:-1])
        else:  # No rating
            company_rating = None
        return company_name, company_rating

    def catch_mandatory_data_and_rating(self, button_job):
        """
        Collect all the mandatory information on the website
        """
        time.sleep(cst.SLEEP_TIME)
        collect_mandatory = False
        while not collect_mandatory:
            # click the job button
            button_job.click()
            try:
                # Catch the publication date and call function to convert publication date
                job_publication_date = self.convert_publication_date(self.browser.find_element_by_xpath(
                    cst.PUBLICATION_DATE_XPATH).text)
                time.sleep(cst.SLEEP_TIME)

                # Collect Company Name from a post, Sometimes: company name and rating are join, we need to split
                # them into Company Name and Rating
                company_name, company_rating = self.convert_split_name_and_rating(self.browser.find_element_by_xpath(
                    cst.COMPANY_NAME_XPATH).text)

                # Collect Job Title from a post
                job_title = self.browser.find_element_by_xpath(cst.JOB_TITLE_XPATH).text

                # Collect Job Location from a post
                job_location = self.browser.find_element_by_xpath(cst.JOB_LOCATION_XPATH).text

                # Collect Job Description
                job_description = self.browser.find_element_by_xpath(cst.JOB_DESCRIPTION_XPATH).text

                # finish collect mandatory fields + rating if the company has in the name
                collect_mandatory = True
                job = Job(job_title, job_description, job_location, job_publication_date, company_name)
                company = Company(company_name, company_rating)
                return job, company

            except NoSuchElementException:
                time.sleep(cst.SLEEP_TIME)

    def catch_optional_data(self, company):
        """
        Catch all the optional information of a company
        :param company: string
        """

        # Collect optional information
        try:
            # Click on company in the hyper details
            self.browser.find_element_by_xpath(cst.OVERVIEW_XPATH).click()
            time.sleep(cst.SLEEP_TIME)

            # Catch company size information
            company.set_company_size(self.catch_optional_text_value_by_xpath(cst.COMPANY_SIZE_XPATH))
            # Catch founded year of company
            company.set_company_founded(self.convert_company_founded_year(self.catch_optional_text_value_by_xpath(
                cst.COMPANY_FOUNDED_XPATH)))
            # Catch company industry
            company.set_company_industry(self.catch_optional_text_value_by_xpath(cst.COMPANY_INDUSTRY_XPATH))
            # Catch company sector
            company.set_company_sector(self.catch_optional_text_value_by_xpath(cst.COMPANY_SECTOR_XPATH))
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

            # Catch competitors and convert to list
            competitors = self.catch_optional_text_value_by_xpath(cst.COMPANY_COMPETITORS_XPATH)
            if competitors is not None and ',' in competitors:
                competitors = competitors.split(',')
            elif competitors is not None:  # single competitor
                competitors = list(competitors)
            company.set_company_competitors(competitors)

        # If there is no overview page(company tab)
        except NoSuchElementException:
            logging.error(cst.ERROR_OPTIONAL_DATA)
        finally:
            return company

    def collecting_data_from_pages(self, database):
        """
        Collect all the data on for a specific search
        """
        time.sleep(cst.SLEEP_TIME)
        self.close_popup()

        glassdoor_number_pages = self.get_num_pages()

        try:
            self.browser.find_element_by_xpath(cst.SELECTED_XPATH).click()
        except ElementClickInterceptedException:  # NoSuchElementException TODO: check the error
            pass

        time.sleep(cst.SLEEP_TIME)

        # Take all the buttons of each job in this page we want to click on
        current_page = cst.FIRST_PAGE
        while current_page <= glassdoor_number_pages:
            job_click_button = self.browser.find_elements_by_xpath(cst.JOB_CLICK_BUTTON_XPATH)

            self.close_popup()

            logging.info(f"Start to collect all data from page: {current_page}")
            for button_job in job_click_button:
                # start collect job data
                job, company = self.catch_mandatory_data_and_rating(button_job)
                company = self.catch_optional_data(company)
                database.insert_company(company)
                if company.get_company_competitors() is not None:
                    for competitor_name in company.get_company_competitors():
                        competitor_name = competitor_name.strip()
                        if competitor_name.lower().split(' ')[-1] in ['corp', 'corporation', 'corp.']:
                            competitor_name = ''.join(competitor_name.lower().split(' ')[:-1])
                        if not database.get_company(competitor_name): # we don't have the competitor in DB
                            competitor = Company(competitor_name, None)
                            competitor_scraping = CompanyPageScraper(competitor_name)
                            competitor_scraping.set_search_keywords()
                            competitor = competitor_scraping.enter_company_page(competitor)
                            competitor.set_company_sector(company.get_company_sector())
                            database.insert_company(competitor)
                        database.insert_competitor(competitor_name, company)
                database.insert_job(job)
            logging.info(f"Succeed to collect all data from page: {current_page}")

            try:
                next_button = self.browser.find_element_by_xpath(cst.NEXT_XPATH)
                next_button.click()
                logging.info("Succeed to click on next button for next page")
            except NoSuchElementException:
                logging.error(cst.ERROR_NEXT)
            time.sleep(cst.SLEEP_TIME)
            current_page += cst.SECOND_ELEMENT
