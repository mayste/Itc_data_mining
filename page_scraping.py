from scraper import Scraper
from job import Job
from company import Company
import time
from constants import SLEEP_TIME
from path import pop_up_xpath
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from dateutil.relativedelta import relativedelta
from datetime import date


# from command_args import args

# FIRST_INSTANCE_TO_SCRAP = args.first_user

class PageScraping(Scraper):
    def __init__(self, page_url):
        Scraper.__init__(self)
        self.current_url = page_url
        self.jobs_page_list = []
        self.companies_page_list = []


    def collecting_data_from_page(self):
        self.browser.get(self.current_url)
        time.sleep(SLEEP_TIME)

        try:
            pop_up = self.browser.find_element_by_xpath(pop_up_xpath)
            pop_up.click()
        except NoSuchElementException:
            pass

        try:
            self.browser.find_element_by_xpath("//li[contains(@class, 'selected')]").click()
        except ElementClickInterceptedException: #NoSuchElementException TODO: check the error
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
            button_job.click()

            # start collect job data

            # Catch the publication date
            job_publication_date = self.browser.find_element_by_xpath("//li[contains(@class,'selected')]//div["
                                                                      "@class='jobContainer']//div[@data-test='job-age']").text
            # if the job has been published this day print the day of today
            if 'h' in job_publication_date and '24' not in job_publication_date:
                job_publication_date = date.today().strftime("%Y-%m-%d")
            elif 'h' in job_publication_date and '24' in job_publication_date:
                job_publication_date = (date.today() - relativedelta(days=1)).strftime("%Y-%m-%d")
            elif 'd' in job_publication_date:
                job_publication_date = (
                            date.today() - relativedelta(days=int(job_publication_date.split('d')[0]))).strftime(
                    "%Y-%m-%d")
            elif 'm' in job_publication_date:
                job_publication_date = (
                            date.today() - relativedelta(months=int(job_publication_date.split('m')[0]))).strftime(
                    "%Y-%m-%d")
            else:
                job_publication_date = None

            time.sleep(SLEEP_TIME)

            # Collect mandatory information
            collect_mandatory = False
            while not collect_mandatory:
                try:
                    # Collect Company Name from a post
                    company_name = self.browser.find_element_by_xpath('//div[@class="employerName"]').text
                    # Collect Job Title from a post
                    job_title = self.browser.find_element_by_xpath('//div[@class="title"]').text
                    # Collect Job Location from a post
                    job_location = self.browser.find_element_by_xpath('//div[@class="location"]').text
                    # Collect Job Description
                    job_description = self.browser.find_element_by_xpath(
                        '//div[@class="jobDescriptionContent desc"]').text

                    # Sometimes, company name and rating are join, we need to split them into Company Name and Rating
                    # information.

                    if '\n' in company_name:  # We have a rating
                        company_rating = company_name.split('\n')[1]
                        company_name = company_name.split('\n')[0]
                    else:  # No rating
                        company_rating = None

                    collect_mandatory = True
                except NoSuchElementException:
                    # button_job.click() #TODO: check if we need this
                    time.sleep(SLEEP_TIME)

                # Collect optional information
                try:
                    # Click on company in the hyper details
                    self.browser.find_element_by_xpath('//div[@class="tab" and @data-tab-type="overview"]').click()

                    time.sleep(SLEEP_TIME)

                    # Catch company size information
                    try:
                        company_size = self.browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_size = None

                    # Catch founded year of company
                    try:
                        company_founded = self.browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_founded = None

                    # Catch company industry
                    try:
                        company_industry = self.browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_industry = None

                        # Catch company sector
                    try:
                        company_sector = self.browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_sector = None

                    # Catch company type
                    try:
                        company_type = self.browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
                                                                          ')="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_type = None

                    # Catch competitors
                    try:
                        company_competitors = self.browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text('
                            ')="Competitors"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_competitors = None

                    # Catch company revenue
                    try:
                        company_revenue = self.browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
                                                                             ')="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_revenue = None

                    # Catch company headquarters
                    try:
                        company_headquarters = self.browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text('
                            ')="Headquarters"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_headquarters = None

                # If there there is no overview page(company tab)
                except NoSuchElementException:
                    company_size = None
                    company_founded = None
                    company_industry = None
                    company_sector = None
                    company_type = None
                    company_competitors = None
                    company_revenue = None
                    company_headquarters = None

            job = Job(job_title, job_description, job_location, job_publication_date, company_name)
            company = Company(company_name, company_size, company_founded, company_industry, company_sector,
                              company_type,
                              company_rating, company_competitors, company_revenue, company_headquarters)
            self.jobs_page_list.append(job)
            self.companies_page_list.append(company)
        self.browser.quit()
        # this class will get a url for page and scrap the data inside then create a list of job objects and company objects
        # in the end of this class we have a list with all the jobs and company for this page that we can return to glassdor class

    def get_jobs_page_list(self):
        return self.jobs_page_list

    def get_companies_page_list(self):
        return self.companies_page_list
