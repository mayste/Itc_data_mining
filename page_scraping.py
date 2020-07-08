from scraper import Scraper
from job import Job
from company import Company
import time
import constants as cst
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from dateutil.relativedelta import relativedelta
from datetime import date


class PageScraping(Scraper):
    # this class will get a url for page and scrap the data inside then create a list of job objects and company objects
    # in the end of this class we have a list with all the jobs and company for this page that we can return to glassdor class

    def __init__(self, page_url):
        Scraper.__init__(self)
        self.current_url = page_url
        self.jobs_page_list = []
        self.companies_page_list = []

    def catch_optional_text_value_by_xpath(self, x_path):
        try:
            text_value = self.browser.find_element_by_xpath(x_path).text
            return text_value
        except NoSuchElementException:
            return None

    def convert_publication_date(self, publication_date):
        # if the job has been published this day print the day of today
        if cst.HOUR in publication_date and cst.ALL_DAY not in publication_date:
            return date.today().strftime(cst.DATE_FORMAT)
        elif cst.HOUR in publication_date and cst.ALL_DAY in publication_date:
            return (date.today() - relativedelta(days=1)).strftime(cst.DATE_FORMAT)
        elif cst.DAY in publication_date:
            return (date.today() - relativedelta(days=int(publication_date.split(cst.DAY)[cst.FIRST_ELEMENT]))).strftime(
                cst.DATE_FORMAT)
        elif cst.MONTH in publication_date:
            return (date.today() - relativedelta(months=int(publication_date.split(cst.MONTH)[cst.FIRST_ELEMENT]))).strftime(
                cst.DATE_FORMAT)
        # else:
        #    return None

    def catch_mandatory_data_and_rating(self, button_job):  # TODO: not sure about the loop
        # Collect mandatory information
        time.sleep(cst.SLEEP_TIME)
        collect_mandatory = False
        while not collect_mandatory:
            # click the job button
            button_job.click()
            try:
                # Catch the publication date
                job_publication_date = self.browser.find_element_by_xpath(cst.PUBLICATION_DATE_XPATH).text
                time.sleep(cst.SLEEP_TIME)

                # Collect Company Name from a post
                company_name = self.browser.find_element_by_xpath(cst.COMPANY_NAME_XPATH).text

                # Collect Job Title from a post
                job_title = self.browser.find_element_by_xpath(cst.JOB_TITLE_XPATH).text

                # Collect Job Location from a post
                job_location = self.browser.find_element_by_xpath(cst.JOB_LOCATION_XPATH).text

                # Collect Job Description
                job_description = self.browser.find_element_by_xpath(cst.JOB_DESCRIPTION_XPATH).text

                # call function to convert publication date
                job_publication_date = self.convert_publication_date(job_publication_date)

                # Sometimes, company name and rating are join, we need to split them into Company Name and Rating
                if '\n' in company_name:  # We have a rating
                    # TODO: Cheack its float
                    company_rating = company_name.split('\n')[cst.SECOND_ELEMENT]
                    company_name = company_name.split('\n')[cst.FIRST_ELEMENT]
                else:  # No rating
                    company_rating = None

                # finish collect mandatory fields + rating if the company has in the name
                collect_mandatory = True
                job = Job(job_title, job_description, job_location, job_publication_date, company_name)
                company = Company(company_name, company_rating)
                return job, company

            except NoSuchElementException:
                # button_job.click() #TODO: check if its not succeed to load we need to click again
                time.sleep(cst.SLEEP_TIME)

    def catch_optional_data(self, company):
        # TODO: Check if value = Unknown put None
        # Collect optional information
        try:
            # Click on company in the hyper details
            self.browser.find_element_by_xpath(cst.OVERVIEW_XPATH).click()

            time.sleep(cst.SLEEP_TIME)

            # Catch company size information
            company.set_company_size(self.catch_optional_text_value_by_xpath(cst.COMPANY_SIZE_XPATH))
            # Catch founded year of company
            # TODO: check that it a number
            company.set_company_founded(self.catch_optional_text_value_by_xpath(cst.COMPANY_FOUNDED_XPATH))
            # Catch company industry
            company.set_company_industry(self.catch_optional_text_value_by_xpath(cst.COMPANY_INDUSTRY_XPATH))
            # Catch company sector
            company.set_company_sector(self.catch_optional_text_value_by_xpath(cst.COMPANY_SECTOR_XPATH))
            # Catch company type
            type = self.catch_optional_text_value_by_xpath(cst.COMPANY_TYPE_XPATH)

            # TODO: check if work
            if type is not None:
                type.split('-').strip()
            company.set_company_type(type[cst.SECOND_ELEMENT])

            # Catch competitors and convert to list
            competitors = self.catch_optional_text_value_by_xpath(cst.COMPANY_COMPETITORS_XPATH)
            if competitors is not None:
                competitors.split(',').strip()

            print(f'competitors: {competitors}')
            # TODO: Check if it put list and append to previous one
            company.set_company_competitors(competitors)
            # Catch company revenue
            company.set_company_revenue(self.catch_optional_text_value_by_xpath(cst.COMPANY_REVENUE_XPATH))
            # Catch company headquarters
            company.set_company_headquarters(self.catch_optional_text_value_by_xpath(cst.COMPANY_HEADQUARTER_XPATH))

        # If there is no overview page(company tab)
        except NoSuchElementException:
            print(cst.ERROR_OPTIONAL_DATA)
            # company_size = None
            # company_founded = None
            # company_industry = None
            # company_sector = None
            # company_type = None
            # company_competitors = None
            # company_revenue = None
            # company_headquarters = None
        finally:
            return company

    def collecting_data_from_page(self, database):
        print(self.current_url)
        self.browser.get(self.current_url)
        time.sleep(cst.SLEEP_TIME)
        try:
            pop_up = self.browser.find_element_by_xpath(cst.POP_UP_XPATH)
            pop_up.click()
        except NoSuchElementException:
            pass

        try:
            self.browser.find_element_by_xpath(cst.SELECTED_XPATH).click()
        except ElementClickInterceptedException:  # NoSuchElementException TODO: check the error
            pass

        time.sleep(cst.SLEEP_TIME)

        # Take all the buttons of each job in this page we want to click on
        job_click_button = self.browser.find_elements_by_xpath(cst.JOB_CLICK_BUTTON_XPATH)

        try:
            pop_up = self.browser.find_element_by_xpath(cst.POP_UP_XPATH)
            pop_up.click()
        except NoSuchElementException:
            pass

        for button_job in job_click_button:
            # start collect job data
            job, company = self.catch_mandatory_data_and_rating(button_job)
            self.jobs_page_list.append(job)
            company = self.catch_optional_data(company)
            database.insert_company(company)
            self.companies_page_list.append(company)
        database.insert_company(flag_finish_page=True)
        self.browser.quit()

    def get_jobs_page_list(self):
        return self.jobs_page_list

    def get_companies_page_list(self):
        return self.companies_page_list
