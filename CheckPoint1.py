import time
import pandas as pd
from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

URL = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword' \
      '=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0 '
browser = webdriver.Chrome()
browser.get(URL)
jobs_list = []


def collecting_data(num_of_jobs):
    while len(jobs_list) < num_of_jobs:

        time.sleep(3)  # Wait until the page load

        try:
            # TODO: Check the item selected what is it
            browser.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(5)
        try:
            browser.find_element_by_xpath("//div[@class='modal_main jaCreateAccountModalWrapper']//span["
                                          "@class='SVGInline modal_closeIcon']").click()  # clicking to the X.
        except NoSuchElementException:
            pass

        # TODO: Check class name
        job_click_button = browser.find_elements_by_class_name("jl")  # Button on each job we want to click on
        # #job_click_button = browser.find_elements_by_class_name("jl react-job-listing gdGrid ")

        for button_job in job_click_button:
            if len(jobs_list) >= num_of_jobs:
                break
            button_job.click()
            time.sleep(4)

            # collect Data for one job
            company_name = browser.find_element_by_xpath(
                '//div[@class="employerName"]').text  # browser.find_elements_by_class_name("employerName")

            # TODO: Taking rating
            # To split the company name to: name and rating
            if '\n' in company_name:
                rating = company_name.split('\n')[1]
                company_name = company_name.split('\n')[0]
            else:
                rating = None
            job_title = browser.find_element_by_xpath('.//div[@class="title"]').text
            job_location = browser.find_element_by_xpath('.//div[@class="location"]').text

            # click on company in the hyper details
            browser.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
            # browser.find_element_by_xpath(".//div[@class=‘scrollableTabs’]//div[@class=‘tab’]").click()

            time.sleep(3)
            try:
                # TODO: Check following-sibling::*
                company_size = browser.find_element_by_xpath(
                    '//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
            except NoSuchElementException:
                company_size = None
            try:
                company_founded = browser.find_element_by_xpath(
                    '//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
            except NoSuchElementException:
                company_founded = None
            try:
                company_industry = browser.find_element_by_xpath(
                    '//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
            except NoSuchElementException:
                company_industry = None
            try:
                company_sector = browser.find_element_by_xpath(
                    '//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
            except NoSuchElementException:
                company_sector = None
            try:
                company_type = browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
                                                             ')="Type"]//following-sibling::*').text
            except NoSuchElementException:
                company_type = None

            # add to the list of jobs
            jobs_list.append({"company name": company_name, "job title": job_title, "job location": job_location,
                              "company size": company_size, "founded": company_founded, "industry": company_industry,
                              "sector": company_sector, "type": company_type, "rating": rating})

        # Clicking on the "next page" button
        # TODO: Check why it's jumping over jobs and continue to next page.he do next anyway
        if len(jobs_list) < num_of_jobs:
            try:
                browser.find_element_by_xpath('.//li[@class="next"]//a').click()
            except NoSuchElementException:
                print(
                    "Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_of_jobs,
                                                                                                           len(
                                                                                                               jobs_list)))
                break

    print(jobs_list)
    dataset = pd.DataFrame(jobs_list)
    dataset.to_csv('\dataset_glassdoor.csv')  # save this to csv file


time.sleep(3)  # Wait until the page load

try:
    # take the number of all open positions over the site in Israel
    num_of_jobs = browser.find_element_by_xpath("//div[@class='hideHH css-19rczgc ez6uq160']").text
    num_of_jobs = int(num_of_jobs.split(' ')[0])
    num_of_jobs = 10  # TODO: Delete this
    print(num_of_jobs)

# TODO: Check all of our exceptions name
except ElementClickInterceptedException:
    # TODO: Change the number to a bigger one
    num_of_jobs = 3

collecting_data(num_of_jobs)
