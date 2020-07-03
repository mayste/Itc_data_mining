from scraper import Scraper
from job import Job
from company import Company
import time
from constants import SLEEP_TIME
from constants import pop_up_xpath
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
        if 'h' in publication_date and '24' not in publication_date:
            return date.today().strftime("%Y-%m-%d")
        elif 'h' in publication_date and '24' in publication_date:
            return (date.today() - relativedelta(days=1)).strftime("%Y-%m-%d")
        elif 'd' in publication_date:
            return (date.today() - relativedelta(days=int(publication_date.split('d')[0]))).strftime("%Y-%m-%d")
        elif 'm' in publication_date:
            return (date.today() - relativedelta(months=int(publication_date.split('m')[0]))).strftime("%Y-%m-%d")
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
                job_publication_date = self.browser.find_element_by_xpath(
                    "//li[contains(@class,'selected')]//div[@class='jobContainer']//div[@data-test='job-age']").text
                time.sleep(SLEEP_TIME)
                # Collect Company Name from a post
                company_name = self.browser.find_element_by_xpath('//div[@class="employerName"]').text
                # Collect Job Title from a post
                job_title = self.browser.find_element_by_xpath('//div[@class="title"]').text
                # Collect Job Location from a post
                job_location = self.browser.find_element_by_xpath('//div[@class="location"]').text
                # Collect Job Description
                job_description = self.browser.find_element_by_xpath('//div[@class="jobDescriptionContent desc"]').text

                # call function to convert publication date
                job_publication_date = self.convert_publication_date(job_publication_date)

                # Sometimes, company name and rating are join, we need to split them into Company Name and Rating
                if '\n' in company_name:  # We have a rating
                    company_rating = company_name.split('\n')[1]
                    company_name = company_name.split('\n')[0]
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
            self.browser.find_element_by_xpath('//div[@class="tab" and @data-tab-type="overview"]').click()

            time.sleep(SLEEP_TIME)

            # Catch company size information
            company.set_company_size(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*'))
            # Catch founded year of company
            company.set_company_founded(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*'))
            # Catch company industry
            company.set_company_industry(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*'))
            # Catch company sector
            company.set_company_sector(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*'))
            # Catch company type
            company.set_company_type(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*'))
            # Catch competitors
            company.set_company_competitors(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*'))
            # Catch company revenue
            company.set_company_revenue(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*'))
            # Catch company headquarters
            company.set_company_headquarters(self.catch_optional_text_value_by_xpath(
                '//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*'))

        # If there is no overview page(company tab)
        except NoSuchElementException:
            print("There is no optional data for this company on this job")
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
            self.browser.find_element_by_xpath("//li[contains(@class, 'selected')]").click()
        except ElementClickInterceptedException:  # NoSuchElementException TODO: check the error
            pass

        time.sleep(SLEEP_TIME)

        # Take all the buttons of each job in this page we want to click on
        job_click_button = self.browser.find_elements_by_xpath("//li[contains(@class, 'job-listing')]")

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
