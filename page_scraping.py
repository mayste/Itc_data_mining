from scraper import Scraper
from job import Job
from company import Company
import time
from constants import SLEEP_TIME, pop_up_xpath, HOUR, DAY, MONTH, \
    FIRST_ELEMENT, ALL_DAY, DATE_FORMAT, FIRST, publication_date_xpath, company_name_xpath, job_title_xpath, \
    job_location_xpath, job_description_xpath, company_size_xpath, overview_xpath, company_founded_xpath, \
    company_industry_xpath, company_sector_xpath, company_type_xpath, company_competitors_xpath, \
    company_revenue_xpath, company_headquarters_xpath, ERROR_OPTIONAL_DATA, selected_xpath, job_click_button_xpath
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from dateutil.relativedelta import relativedelta
from datetime import date


# from command_args import args

# FIRST_INSTANCE_TO_SCRAP = args.first_user

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
        if HOUR in publication_date and ALL_DAY not in publication_date:
            return date.today().strftime(DATE_FORMAT)
        elif HOUR in publication_date and ALL_DAY in publication_date:
            return (date.today() - relativedelta(days=FIRST)).strftime(DATE_FORMAT)
        elif DAY in publication_date:
            return (date.today() - relativedelta(days=int(publication_date.split(DAY)[FIRST_ELEMENT]))).strftime(DATE_FORMAT)
        elif MONTH in publication_date:
            return (date.today() - relativedelta(months=int(publication_date.split(MONTH)[FIRST_ELEMENT]))).strftime(DATE_FORMAT)
        # else:
        #    return None

    def catch_mandatory_data_and_rating(self, button_job):  # TODO: not sure about the loop
        # Collect mandatory information
        time.sleep(SLEEP_TIME)
        collect_mandatory = False
        while not collect_mandatory:
            # click the job button
            button_job.click()
            try:
                # Catch the publication date
                job_publication_date = self.browser.find_element_by_xpath(publication_date_xpath).text
                time.sleep(SLEEP_TIME)

                # Collect Company Name from a post
                company_name = self.browser.find_element_by_xpath(company_name_xpath).text

                # Collect Job Title from a post
                job_title = self.browser.find_element_by_xpath(job_title_xpath).text

                # Collect Job Location from a post
                job_location = self.browser.find_element_by_xpath(job_location_xpath).text

                # Collect Job Description
                job_description = self.browser.find_element_by_xpath(job_description_xpath).text

                # call function to convert publication date
                job_publication_date = self.convert_publication_date(job_publication_date)

                # Sometimes, company name and rating are join, we need to split them into Company Name and Rating
                if '\n' in company_name:  # We have a rating
                    company_rating = company_name.split('\n')[FIRST]
                    company_name = company_name.split('\n')[FIRST_ELEMENT]
                else:  # No rating
                    company_rating = None

                # finish collect mandatory fields + rating if the company has in the name
                collect_mandatory = True
                job = Job(job_title, job_description, job_location, job_publication_date, company_name)
                company = Company(company_name, company_rating)
                return job, company

            except NoSuchElementException:
                #button_job.click() #TODO: check if its not succeed to load we need to click again
                time.sleep(SLEEP_TIME)

    def catch_optional_data(self, company):
        # Collect optional information
        try:
            # Click on company in the hyper details
            self.browser.find_element_by_xpath(overview_xpath).click()

            time.sleep(SLEEP_TIME)

            # Catch company size information
            company.set_company_size(self.catch_optional_text_value_by_xpath(company_size_xpath))
            # Catch founded year of company
            company.set_company_founded(self.catch_optional_text_value_by_xpath(company_founded_xpath))
            # Catch company industry
            company.set_company_industry(self.catch_optional_text_value_by_xpath(company_industry_xpath))
            # Catch company sector
            company.set_company_sector(self.catch_optional_text_value_by_xpath(company_sector_xpath))
            # Catch company type
            company.set_company_type(self.catch_optional_text_value_by_xpath(company_type_xpath))
            # Catch competitors
            company.set_company_competitors(self.catch_optional_text_value_by_xpath(company_competitors_xpath))
            # Catch company revenue
            company.set_company_revenue(self.catch_optional_text_value_by_xpath(company_revenue_xpath))
            # Catch company headquarters
            company.set_company_headquarters(self.catch_optional_text_value_by_xpath(company_headquarters_xpath))

        # If there is no overview page(company tab)
        except NoSuchElementException:
            print(ERROR_OPTIONAL_DATA)
            #company_size = None
            #company_founded = None
            #company_industry = None
            #company_sector = None
            #company_type = None
            #company_competitors = None
            #company_revenue = None
            #company_headquarters = None
        finally:
            return company

    def collecting_data_from_page(self):
        self.browser.get(self.current_url)
        print(self.current_url)
        time.sleep(SLEEP_TIME)
        try:
            pop_up = self.browser.find_element_by_xpath(pop_up_xpath)
            pop_up.click()
        except NoSuchElementException:
            pass

        try:
            self.browser.find_element_by_xpath(selected_xpath).click()
        except ElementClickInterceptedException:  # NoSuchElementException TODO: check the error
            pass

        time.sleep(SLEEP_TIME)

        # Take all the buttons of each job in this page we want to click on
        job_click_button = self.browser.find_elements_by_xpath(job_click_button_xpath)

        try:
            pop_up = self.browser.find_element_by_xpath(pop_up_xpath)
            pop_up.click()
        except NoSuchElementException:
            pass

        for button_job in job_click_button:
            # start collect job data
            job, company = self.catch_mandatory_data_and_rating(button_job)
            self.jobs_page_list.append(job)
            company = self.catch_optional_data(company)
            self.companies_page_list.append(company)
        self.browser.quit()

    def get_jobs_page_list(self):
        return self.jobs_page_list

    def get_companies_page_list(self):
        return self.companies_page_list
