"""
This program is part of our learning in ITC Campus for Data Mining Project
Authors: May Steinfeld & Sheryl Sitruk
"""

import time
from dateutil.relativedelta import relativedelta
from datetime import date
import pandas as pd
from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

# Global variables
SLEEP_TIME = 5  # Random number for time sleep, depends on computers- in our we meed minimum 5
EXE_PATH = r'/Users/Sheryl/PycharmProjects/Itc_data_mining/webDrivers/geckodriver'
jobs_list = []


def create_csv_file(dict_list):
    """
    This function create a .csv file with a list of dictionaries as an input
    :param dict_list: list of dictionaries
    :return: .csv file
    """
    dataset = pd.DataFrame(jobs_list).drop_duplicates()  # remove duplicates
    dataset.to_csv('\dataset_glassdoor.csv', index=False)  # save this to csv file


def collecting_data(job_title_input, location_input):
    options = webdriver.FirefoxOptions()
    options.add_argument('headless')  # scrape without a new Firefox window every time
    browser = webdriver.Firefox(firefox_options=options, executable_path=EXE_PATH)
    browser.maximize_window()
    url = f'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0 '
    browser.get(url)

    time.sleep(SLEEP_TIME)

    job_title = browser.find_element_by_id("sc.keyword")
    job_title.send_keys(job_title_input)
    location = browser.find_element_by_id("sc.location")
    location.clear()
    location.send_keys(location_input)

    try:
        browser.find_element_by_xpath("//div[contains(@class,'modal_main')]//span["
                                      "@class='SVGInline modal_closeIcon']").click()
    except NoSuchElementException:
        pass

    browser.find_element_by_id("HeroSearchButton").click()

    time.sleep(SLEEP_TIME)  # Wait until the page load

    #catch number of pages
    try:
        # take the number of all open positions in Israel over the site
        num_of_available_pages = browser.find_element_by_xpath("//div[@class='cell middle hideMob padVertSm']").text
        num_of_available_pages = int(num_of_available_pages.split(' ')[-1])
        print(num_of_available_pages)
    except ElementClickInterceptedException:
        num_of_available_pages = 1  # default value, most of the time there are 30 pages
        print(f'Their is a problem trying to get the number of available pages of jobs post, by default the number of '
              f'available pages of jobs post to scrap will be {num_of_available_pages}')

    time.sleep(SLEEP_TIME)


    # Click to the X to close popups
    try:
        browser.find_element_by_xpath("//div[contains(@class,'modal_main')]//span["
                                      "@class='SVGInline modal_closeIcon']").click()
    except NoSuchElementException:
        pass


    try:
        browser.find_element_by_xpath("//li[contains(@class, 'selected')]").click()
    except ElementClickInterceptedException:
        pass

    time.sleep(SLEEP_TIME)

    current_page = 1

    # Take all the buttons of each job in this page we want to click on


    while current_page < num_of_available_pages:

        try:
            browser.find_element_by_xpath("//div[contains(@class,'modal_main')]//span["
                                          "@class='SVGInline modal_closeIcon']").click()
        except NoSuchElementException:
            pass

        job_click_button = browser.find_elements_by_xpath("//li[contains(@class, 'job-listing')]")

        for button_job in job_click_button:
            button_job.click()

        # start collect job data

        # Catch the publication date
            job_age = browser.find_element_by_xpath("//li[contains(@class,'selected')]//div["
                                                "@class='jobContainer']//div[@data-test='job-age']").text
        # if the job has been published this day print the day of today
            if 'h' in job_age and '24' not in job_age:
                job_age = date.today().strftime("%Y-%m-%d")
            elif 'h' in job_age and '24' in job_age:
                job_age = (date.today() - relativedelta(days=1)).strftime("%Y-%m-%d")
            elif 'd' in job_age:
                job_age = (date.today() - relativedelta(days=int(job_age.split('d')[0]))).strftime("%Y-%m-%d")
            elif 'm' in job_age:
                job_age = (date.today() - relativedelta(months=int(job_age.split('m')[0]))).strftime("%Y-%m-%d")
            else:
                job_age = None

            time.sleep(SLEEP_TIME)

        # Collect mandatory information
            collect_mandatory = False
            while not collect_mandatory:
                try:
                # Collect Company Name from a post
                    company_name = browser.find_element_by_xpath('//div[@class="employerName"]').text
                # Collect Job Title from a post
                    job_title = browser.find_element_by_xpath('//div[@class="title"]').text
                # Collect Job Location from a post
                    job_location = browser.find_element_by_xpath('//div[@class="location"]').text
                # Collect Job Description
                    job_description = browser.find_element_by_xpath('//div[@class="jobDescriptionContent desc"]').text

                # Sometimes, company name and rating are join, we need to split them into Company Name and Rating
                # information.

                    if '\n' in company_name:  # We have a rating
                        rating = company_name.split('\n')[1]
                        company_name = company_name.split('\n')[0]
                    else:  # No rating
                        rating = None

                    collect_mandatory = True
                except NoSuchElementException:
                # button_job.click() #TODO: check if we need this
                    time.sleep(SLEEP_TIME)

            # Collect optional information
                try:
                # Click on company in the hyper details
                    browser.find_element_by_xpath('//div[@class="tab" and @data-tab-type="overview"]').click()

                    time.sleep(SLEEP_TIME)

                # Catch company size information
                    try:
                        company_size = browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_size = None

                # Catch founded year of company
                    try:
                        company_founded = browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_founded = None

                # Catch company industry
                    try:
                        company_industry = browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_industry = None

                # Catch company sector
                    try:
                        company_sector = browser.find_element_by_xpath(
                            '//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_sector = None

                # Catch company type
                    try:
                        company_type = browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
                                                                 ')="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_type = None

                # Catch competitors
                    try:
                        company_competitors = browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
                                                                        ')="Competitors"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_competitors = None

                # Catch company revenue
                    try:
                        company_revenue = browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
                                                                    ')="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        company_revenue = None

                # Catch company headquarters
                    try:
                        company_headquarters = browser.find_element_by_xpath('//div[@class="infoEntity"]//label[text('
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

            # Add all information in a dictionary to the list of jobs
                jobs_list.append({"company name": company_name, "job title": job_title, "job description": job_description,
                              "job location": job_location, "publication date": job_age,
                              "company size": company_size, "founded": company_founded, "industry": company_industry,
                              "sector": company_sector, "type": company_type, "rating": rating,
                              "competitors": company_competitors, "revenue": company_revenue,
                              "Headquarters": company_headquarters})


        # save each page to the csv file in case glassdoor block us
            create_csv_file(jobs_list)
            # click on next button

        if current_page == 1:
            try:
                next = browser.find_element_by_xpath('//li[@class="next"]//a[@data-test="pagination-next"]').click()
            except NoSuchElementException:
                print(f"Not succeed to click on next")

            time.sleep(10)
            current_url = browser.current_url
            print(current_url)

        current_page += 1

        URL = current_url.split('IP')[0] + 'IP' + str(current_page) + '.htm'
        print(URL)
        browser.get(URL)
        time.sleep(SLEEP_TIME)



    browser.quit()


if __name__ == "__main__":
    job_title_input = input('Enter a job title')
    location_input = input('Enter a location')
    collecting_data(job_title_input, location_input)

