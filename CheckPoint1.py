import time
import pandas as pd
from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

# Global variables
URL = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword' \
      '=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0 '
browser = webdriver.Chrome()
browser.get(URL)
jobs_list = []


def create_csv_file(dict_list):
    """
    This function create a .csv file with a list of dictionaries as an input
    :param dict: list of dictionaries
    :return: .csv file
    """
    dataset = pd.DataFrame(jobs_list)
    dataset.to_csv('\dataset_glassdoor.csv', index=False)  # save this to csv file


def get_number_of_jobs():
    """
    This function catch the number of job post in Israel
    :return: integer
    """
    time.sleep(3)  # Wait until the page load
    try:
        # take the number of all open positions in Israel over the site
        num_of_available_jobs = browser.find_element_by_xpath("//div[@class='hideHH css-19rczgc ez6uq160']").text
        num_of_available_jobs = int(num_of_available_jobs.split(' ')[0])
        num_of_available_jobs = 400 #TODO: Delete this
    except ElementClickInterceptedException:
        num_of_available_jobs = 1000
        print(f'Their is a problem trying to get the number of available jobs post, by default the number of '
              f'available jobs post to scrap will be {num_of_available_jobs}')
    return num_of_available_jobs


def collecting_data(num_of_jobs):
    """
    This function get a number of available jobs and collect information about them : Company name, Job Title,
    Job Location, Company Size, Founded, Industry, Sector, Type, Rating, Competitors, Revenue, Headquarters
    :param num_of_jobs: integer
    :return: list of dictionaries
    """

    while len(jobs_list) < num_of_jobs:

        time.sleep(5)  # Wait until the page load

        try:
            # TODO: Check the item selected what is it
            browser.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(2)

        # Click to the X to close popups
        try:
            browser.find_element_by_xpath("//div[@class='modal_main jaCreateAccountModalWrapper']//span["
                                          "@class='SVGInline modal_closeIcon']").click()
        except NoSuchElementException:
            pass

        # TODO: Check class name  #job_click_button = browser.find_elements_by_class_name("jl react-job-listing gdGrid ")

        # Take all the buttons of each job we want to click on
        job_click_button = browser.find_elements_by_class_name("jl")

        for button_job in job_click_button:

            # If the program finished to collect all of the records
            if len(jobs_list) >= num_of_jobs:
                break

            button_job.click()
            time.sleep(4)

            # TODO : browser.find_elements_by_class_name("employerName")
            # TODO : see if we need try and catch for this part

            # Collect mandatory information

            # Collect Company Name from a post
            company_name = browser.find_element_by_xpath('//div[@class="employerName"]').text

            # Sometimes, company name and rating are join, we need to split them into Company Name and Rating informations.

            if '\n' in company_name:  # We have a rating
                rating = company_name.split('\n')[1]
                company_name = company_name.split('\n')[0]
            else:  # No rating
                rating = None

            # Collect Job Title from a post
            job_title = browser.find_element_by_xpath('//div[@class="title"]').text

            # Collect Job Location from a post
            job_location = browser.find_element_by_xpath('//div[@class="location"]').text

            #Collect Job Description
            job_description = browser.find_element_by_xpath('//div[@class="jobDescriptionContent desc"]').text

            # Collect optional information

            try:
                # Click on company in the hyper details
                browser.find_element_by_xpath('//div[@class="tab" and @data-tab-type="overview"]').click()
                # TODO: browser.find_element_by_xpath(".//div[@class=‘scrollableTabs’]//div[@class=‘tab’]").click()

                time.sleep(3)

                # Catch company size information
                try:
                    # TODO: Check following-sibling::*
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
            jobs_list.append({"company name": company_name, "job title": job_title,"job description":job_description, "job location": job_location,
                              "company size": company_size, "founded": company_founded, "industry": company_industry,
                              "sector": company_sector, "type": company_type, "rating": rating,
                              "competitors": company_competitors, "revenue": company_revenue,
                              "Headquarters": company_headquarters})
        create_csv_file(jobs_list)
        # Clicking on the "next page" button if finished collected all jobs post from current page
        # TODO: Check why it's jumping over jobs and continue to next page.he do next anyway
        if len(jobs_list) < num_of_jobs:
            try:
                browser.find_element_by_xpath('.//li[@class="next"]//a').click()
            except NoSuchElementException:
                print(f"Finished, no more jobs than{len(jobs_list)} in the website")
                break

    return jobs_list


if __name__ == "__main__":
    num_of_jobs = get_number_of_jobs()
    dict_list = collecting_data(num_of_jobs)
    create_csv_file(dict_list)
